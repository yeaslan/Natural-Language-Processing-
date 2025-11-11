# NLP Portfolio Study

Automated expertise extraction and knowledge-graph enrichment pipeline inspired to map human knowledge. This repository provides an end-to-end scaffold covering ingestion, NLP, storage, serving, and MLOps concerns to able to demonstrate production-grade thinking.

## Overview
- **Ingestion & preprocessing** adapters to clean and normalize text from Q&A, documents, and transcripts.
- **NLP/ML** components for named entity recognition, entity linking, relation extraction, embeddings, and reranking.
- **Graph + search storage** using Neo4j, PostgreSQL, and OpenSearch/pgvector for hybrid retrieval.
- **FastAPI service** exposing extraction, search, and feedback endpoints.
- **MLOps & infra** scaffolding with Docker Compose, CI, evaluation harness, and feedback loops.

## Quick Start
1. Install Python 3.11+ and Docker.
2. `make setup` to create a virtual environment and install dependencies.
3. `make docker-up` to launch Neo4j, PostgreSQL, and OpenSearch locally.
4. `make run-api` to start the FastAPI service at `http://localhost:8000`.

### Sample Extraction Request
```bash
curl -X POST http://localhost:8000/nlp/extract \
  -H 'Content-Type: application/json' \
  -d '{"text": "John built a new embedding model for customer feedback using PyTorch."}'
```

## Repository Layout
```
apps/
  api/                # FastAPI microservice
  workers/            # Background worker entry points
ml/
  ner/                # Named entity recognition
  re/                 # Relation extraction
  el/                 # Entity linking
  embed/              # Embeddings + similarity
  evaluation/         # Metrics and evaluation harness
data/
  raw/                # Source datasets
  processed/          # Cleaned/annotated data
infra/
  docker/             # Container definitions
  k8s/                # Kubernetes manifests
  terraform/          # Optional IaC placeholders
notebooks/            # Exploratory analysis and demos
scripts/              # Utilities and jobs
tests/                # Unit/integration tests
configs/              # YAML/JSON configs
```

## Next Steps
- Populate datasets in `data/raw` and notebooks with exploratory workflows.
- Fine-tune relation extraction and entity linking models using organization-specific annotations.
- Expand tests under `tests/` and wire CI/CD pipelines described in `.github/workflows/`.
- Integrate feedback processing jobs in `apps/workers`.
