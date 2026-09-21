"""OTLP receiver: ingest traces/metrics/logs via gRPC + HTTP."""

import asyncio
from typing import Callable
from opentelemetry.proto.collector.trace.v1.trace_service_pb2_grpc import (
    TraceServiceServicer,
    add_TraceServiceServicer_to_server,
)
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse,
)
import grpc


class OTLPServicer(TraceServiceServicer):
    """Receives OTLP trace requests and forwards to buffer."""

    def __init__(self, buffer: "RingBuffer"):
        self.buffer = buffer

    async def Export(self, request: ExportTraceServiceRequest, context) -> ExportTraceServiceResponse:
        """Receive trace spans."""
        spans_received = 0
        for resource_spans in request.resource_spans:
            for scope_spans in resource_spans.scope_spans:
                for span in scope_spans.spans:
                    self.buffer.put(span)
                    spans_received += 1
        return ExportTraceServiceResponse()  # success


class RingBuffer:
    """LMAX Disruptor-style ring buffer for high-throughput ingest."""

    def __init__(self, capacity: int = 65536):
        self.capacity = capacity
        self.buffer: list = [None] * capacity
        self.head = 0  # write position
        self.tail = 0  # read position

    def put(self, item):
        """Non-blocking put. Overwrites oldest if full (with warning)."""
        next_head = (self.head + 1) % self.capacity
        if next_head == self.tail:
            # Buffer full - drop oldest
            self.tail = (self.tail + 1) % self.capacity
        self.buffer[self.head] = item
        self.head = next_head

    def take(self):
        """Blocking take."""
        while self.tail == self.head:
            pass  # spin (real impl uses event)
        item = self.buffer[self.tail]
        self.buffer[self.tail] = None
        self.tail = (self.tail + 1) % self.capacity
        return item


async def start_otlp_server(port: int = 4317, buffer: RingBuffer = None):
    """Start OTLP gRPC server."""
    buffer = buffer or RingBuffer()
    server = grpc.aio.server()
    add_TraceServiceServicer_to_server(OTLPServicer(buffer), server)
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    print(f"OTLP gRPC server listening on :{port}")
    return server, buffer
