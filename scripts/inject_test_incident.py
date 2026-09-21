"""Inject a test incident for demo purposes."""

import requests
import random
import time


def inject_slow_query_incident():
    """Simulate a slow query incident."""
    incident = {
        "service": "checkout-api",
        "symptoms": [
            "P99 latency 3500ms (baseline 200ms)",
            "Error rate 0.5% (baseline 0.01%)",
            "DB CPU 95%",
        ],
        "recent_traces": [
            {
                "trace_id": f"trace-{i}",
                "duration_ms": random.randint(2000, 4000),
                "operation": "POST /api/checkout",
                "db_query": "SELECT * FROM orders WHERE user_id = ? AND created_at > ?",
                "db_duration_ms": random.randint(1800, 3800),
            }
            for i in range(10)
        ],
        "recent_metrics": {
            "db.cpu": 0.95,
            "db.connections": 98,
            "cache.hit_rate": 0.42,
        },
    }
    return incident


def main():
    incident = inject_slow_query_incident()
    print(f"Injecting incident: {incident['service']}")

    resp = requests.post("http://localhost:8000/api/v1/analyze", json=incident)
    print(f"Status: {resp.status_code}")
    print(f"Diagnosis: {resp.json()}")


if __name__ == "__main__":
    main()
