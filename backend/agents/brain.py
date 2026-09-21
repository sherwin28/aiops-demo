"""Brain Agent - orchestrates incident analysis."""

from typing import TypedDict
from agent.llm.provider_router import get_llm


class IncidentContext(TypedDict):
    service: str
    symptoms: list[str]
    recent_traces: list[dict]
    recent_metrics: dict


class Diagnosis(TypedDict):
    root_cause: str
    confidence: float
    recommendations: list[str]
    next_steps: list[str]


BRAIN_SYSTEM_PROMPT = """You are the Brain Agent in an AIOps platform.

Given an incident context (service, symptoms, recent traces, recent metrics),
determine the root cause and provide recommendations.

Output as JSON:
{
  "root_cause": "<one-line summary>",
  "confidence": <0.0-1.0>,
  "recommendations": ["action 1", "action 2", ...],
  "next_steps": ["step 1", "step 2", ...]
}

Be specific. Reference actual trace IDs, metric values, or log patterns."""


class BrainAgent:
    def __init__(self, provider: str = None):
        self.llm = get_llm(provider)

    def analyze(self, context: IncidentContext) -> Diagnosis:
        """Analyze incident and return root cause."""
        prompt = f"""Incident Context:
- Service: {context['service']}
- Symptoms: {context['symptoms']}
- Recent Traces: {len(context['recent_traces'])} spans
- Recent Metrics: {context['recent_metrics']}

Provide diagnosis as JSON:"""

        response = self.llm.invoke([
            {"role": "system", "content": BRAIN_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])

        import json
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "root_cause": "Unable to parse LLM response",
                "confidence": 0.0,
                "recommendations": ["Check raw response"],
                "next_steps": [],
                "raw": response.content,
            }
