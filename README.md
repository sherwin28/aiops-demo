# aiops-demo

**OpenTelemetry ingest + LLM multi-agent incident analysis.**

Based on the AIOps platform I built at Bespin Global. MTTR (Mean Time To Root-Cause) went from 30 minutes to 5 minutes in production.

---

## What this demo does

1. Receives OTLP traces/metrics/logs from your apps
2. Routes them through a ring buffer (LMAX Disruptor pattern)
3. Stores in Apache Doris
4. Triggers multi-agent analysis when alerts fire:
   - **Brain Agent** decides what to investigate
   - **Data Agent** queries metrics
   - **Inspection Agent** reads recent traces
5. Returns root cause + recommendations in JSON

---

## Architecture

```
[App OTLP] → [Receiver] → [Ring Buffer] → [Doris]
                                              ↓
                                     [Brain Agent]
                                              ↓
                       ┌──────────────────────┼──────────────────────┐
                       ↓                      ↓                      ↓
                [Data Agent]       [Inspection Agent]         [Log Agent]
                       ↓                      ↓                      ↓
                       └────────[LLM Router (9 providers)]──────┘
                                              ↓
                                [Root Cause + Recommendations]
                                              ↓
                            [Vue 3 + AntV X6 Visualization]
```

---

## Quick start

```bash
git clone https://github.com/sherwin28/aiops-demo
cd aiops-demo
docker-compose up
open http://localhost:5173

# Inject a test incident
python scripts/inject_test_incident.py
```

You'll see: `checkout-api` slow query → Brain Agent analysis → "Missing index on orders(user_id, created_at)" → recommendation to add index.

---

## Stack

Python 3.11 · FastAPI · gRPC · OpenTelemetry · Apache Doris · LangChain · Vue 3 · AntV X6 · Docker Compose

---

## Layout

```
backend/
├── ingest/otlp_receiver.py    OTLP gRPC + LMAX ring buffer
├── agents/brain.py            Root-cause analysis
├── agents/inspection.py       Trace deep-dive
└── app.py                     FastAPI entry

frontend/
└── src/App.vue                Topology + alert UI

scripts/inject_test_incident.py  Synthetic incident generator
```

---

## Reference

Built from Bespin Global AIOps platform (5 expert agents, 9 LLM providers, multi-arch Helm chart deploy).

---

## License

MIT

---

**Author**: 魏远标 · [javai.tech](https://javai.tech)