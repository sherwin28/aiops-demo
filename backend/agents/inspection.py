"""Inspection Agent - performs deep-dive on traces."""

from typing import TypedDict
from agent.llm.provider_router import get_llm


class TraceSummary(TypedDict):
    anomaly_type: str
    affected_spans: list[str]
    patterns: list[str]


INSPECTION_PROMPT = """You are the Inspection Agent in an AIOps platform.

Given a batch of trace spans, identify:
1. Anomaly type (slow query, error spike, retry storm, timeout cascade, etc.)
2. Most affected spans (top 5 by impact)
3. Patterns suggesting root cause

Output JSON."""


class InspectionAgent:
    def __init__(self, provider: str = None):
        self.llm = get_llm(provider)

    def inspect(self, spans: list[dict]) -> TraceSummary:
        prompt = f"Analyze {len(spans)} trace spans:\n\n{spans[:10]}"
        response = self.llm.invoke([
            {"role": "system", "content": INSPECTION_PROMPT},
            {"role": "user", "content": prompt},
        ])
        import json
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"anomaly_type": "unknown", "affected_spans": [], "patterns": [], "raw": response.content}
