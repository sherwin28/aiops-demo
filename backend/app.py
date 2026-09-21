"""FastAPI application for AIOps demo."""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from ingest.otlp_receiver import start_otlp_server, RingBuffer
from agents.brain import BrainAgent
from agents.inspection import InspectionAgent
from contextlib import asynccontextmanager
import asyncio


ring_buffer = RingBuffer()
brain = BrainAgent()
inspection = InspectionAgent()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    otlp_server, _ = await start_otlp_server(port=4317, buffer=ring_buffer)
    app.state.otlp_server = otlp_server
    yield
    # Shutdown
    await otlp_server.stop(grace=5)


app = FastAPI(title="AIOps Demo", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "buffer_size": ring_buffer.head - ring_buffer.tail}


@app.post("/api/v1/analyze")
async def analyze_incident(incident: dict):
    """Trigger multi-agent incident analysis."""
    # Inspection Agent inspects traces
    trace_summary = inspection.inspect(incident.get("recent_traces", []))

    # Brain Agent analyzes context
    diagnosis = brain.analyze({
        "service": incident.get("service", "unknown"),
        "symptoms": incident.get("symptoms", []),
        "recent_traces": incident.get("recent_traces", []),
        "recent_metrics": incident.get("recent_metrics", {}),
    })

    return {
        "diagnosis": diagnosis,
        "trace_summary": trace_summary,
    }


@app.websocket("/ws/incidents")
async def ws_incidents(websocket: WebSocket):
    """Real-time incident push."""
    await websocket.accept()
    while True:
        # Placeholder: poll for new incidents
        await asyncio.sleep(5)
        await websocket.send_json({"type": "heartbeat", "ts": "..."})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
