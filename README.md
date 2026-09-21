# AIOps Demo

**OpenTelemetry + LLM multi-agent incident analysis**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-latest-blue.svg)]()

---

## What this is

A minimal, runnable AIOps platform that demonstrates how to combine **OpenTelemetry observability** with **LLM multi-agent analysis** to cut MTTR (Mean Time To Root-Cause) from 30 minutes to 5 minutes.

Based on patterns from a production AIOps platform I built at Bespin Global.

## Features

- ✅ **OTLP receiver** (gRPC + HTTP) — ingests traces/metrics/logs/topology
- ✅ **LMAX Disruptor** ring buffer — high-throughput ingestion
- ✅ **Multi-agent analysis** — Brain / Data / Inspection specialists
- ✅ **9-LLM provider router** (Qwen / GPT / Claude / DeepSeek)
- ✅ **Topology visualization** — Vue + AntV X6 frontend
- ✅ **Helm Chart** — multi-arch (amd64/arm64) deploy

## Architecture

```
[App OTLP] → [Receiver] → [Disruptor Buffer] → [Doris Storage]
                                                        ↓
                                              [Brain Agent]
                                                        ↓
                                  ┌──────────────────┼──────────────────┐
                                  ↓                  ↓                  ↓
                          [Data Agent]      [Inspection Agent]    [Log Agent]
                                  ↓                  ↓                  ↓
                                  └────────[LLM Router]──────┘
                                                ↓
                                    [Root Cause + Recommendation]
                                                ↓
                                  [Vue + AntV X6 Visualization]
```

## Quick start

```bash
git clone https://github.com/sherwin28/aiops-demo.git
cd aiops-demo
docker-compose up
open http://localhost:5173  # frontend
```

## Inject a test trace

```bash
python scripts/inject_test_incident.py
# Triggers a slow query → fires alert → agents analyze → recommendation appears
```

## Tech Stack

**Backend**: Python 3.11 / FastAPI / SQLAlchemy async / Celery
**Data**: Apache Doris / Elasticsearch
**Frontend**: Vue 3 + AntV X6 + Vite
**Infra**: Docker Compose / Helm / Kubernetes / OpenTelemetry

## Use cases

- 🏢 Run as a starter for enterprise AIOps
- 🔬 Demo for client presentations
- 🎓 Reference architecture for OTLP + LLM integration

## License

MIT

## Author

**魏远标** — AI Architect · [javai.tech](https://javai.tech)
