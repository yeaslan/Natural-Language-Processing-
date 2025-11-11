"""
Generate a PDF report summarizing the NLP Case Study implementation.

Usage:
    python scripts/generate_report.py
"""

from datetime import datetime
from pathlib import Path
from textwrap import wrap

from fpdf import FPDF

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "docs" / "nlp_case_study_report.pdf"


SECTION_CONTENT = [
    (
        "Executive Summary",
        (
            "This case study presents an end-to-end Natural Language Processing platform that automates "
            "expertise extraction and enriches organizational knowledge graphs. The implementation aligns "
            "with Starmind's mission to map human knowledge by combining entity extraction, relation "
            "discovery, semantic search, and feedback-driven learning in a production-ready architecture."
        ),
    ),
    (
        "Why It Matters",
        (
            "- Employees lose time searching for expertise and relevant documents.\n"
            "- Knowledge graphs become stale without automated enrichment.\n"
            "- Manual tagging does not scale across fast-moving organizations.\n"
            "- A unified NLP pipeline improves retrieval quality and reduces operational overhead."
        ),
    ),
    (
        "System Overview",
        (
            "The solution ingests unstructured text, cleans and anonymizes content, extracts entities and "
            "relations, links them to canonical topics, and stores the results in a Neo4j knowledge graph. "
            "Embeddings power semantic similarity, while OpenSearch and pgvector enable hybrid retrieval. "
            "FastAPI exposes ingestion, extraction, search, and feedback endpoints."
        ),
    ),
    (
        "Architecture Layers",
        (
            "1. Ingestion & Preprocessing: adapters for Q&A logs, documents, tickets, and transcripts; PII scrubbing.\n"
            "2. NLP/ML: named entity recognition, entity linking, relation extraction, sentence embeddings, reranking.\n"
            "3. Storage: Neo4j for graph data, PostgreSQL for metadata, OpenSearch/pgvector for hybrid search indices.\n"
            "4. Serving: FastAPI microservice with health, extraction, knowledge graph upsert, and search endpoints.\n"
            "5. MLOps: Docker Compose, Makefile targets, evaluation harness, and CI hooks for linting/testing."
        ),
    ),
    (
        "Implementation Highlights",
        (
            "- NER pipeline uses `dslim/bert-base-NER` with label remapping to Person, Topic, Org, Domain.\n"
            "- Topic linker leverages sentence-transformer embeddings with configurable thresholds.\n"
            "- Relation model scaffold targets relations like HAS_EXPERTISE_IN and COVERS.\n"
            "- Neo4j client implements idempotent node/edge upserts with timestamp updates.\n"
            "- Hybrid search combines BM25 (OpenSearch) with dense embeddings for semantic ranking.\n"
            "- Docker Compose coordinates Neo4j, PostgreSQL, OpenSearch, Redis, and the API service."
        ),
    ),
    (
        "Evaluation & Feedback Loop",
        (
            "The evaluation harness (placeholder) is prepared for NER precision/recall, entity-link hits@k, and "
            "relation extraction F1. Feedback endpoints capture implicit/explicit signals to adjust edge scores. "
            "Scheduled jobs refresh embeddings and retrain models using MLflow-managed experiments."
        ),
    ),
    (
        "Next Steps",
        (
            "- Populate canonical topic and person datasets, then hydrate the linker index.\n"
            "- Implement feedback persistence, aggregation jobs, and scheduled retraining workflows.\n"
            "- Expand unit/integration tests, add CI configuration, and integrate observability metrics.\n"
            "- Extend serving layer with query explanations and multi-tenant security policies."
        ),
    ),
]


class Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Starmind NLP Case Study Report", ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 8, f"Generated: {datetime.utcnow():%Y-%m-%d %H:%M UTC}", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section(self, title: str, content: str):
        self.set_font("Helvetica", "B", 12)
        self.multi_cell(0, 8, title)
        self.ln(1)
        self.set_font("Helvetica", "", 11)
        for line in content.split("\n"):
            if line.startswith("- ") or line[:2].isdigit():
                self.multi_cell(0, 6, line)
            else:
                wrapped = wrap(line, width=95)
                for wrap_line in wrapped:
                    self.cell(0, 6, wrap_line, ln=True)
            self.ln(0.5)
        self.ln(3)


def generate_pdf():
    pdf = Report()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for title, content in SECTION_CONTENT:
        pdf.add_section(title, content)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT_PATH))
    print(f"Report generated at {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_pdf()
