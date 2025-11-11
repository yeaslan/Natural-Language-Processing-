"""
Quick script to exercise the extraction and linking pipeline without running the API.

Usage:
    python scripts/demo_extract.py "John built a new embedding model for customer feedback using PyTorch."
"""

import sys

from ml.el.linker import TopicLinker
from ml.ner.predict import NERExtractor

TOPICS = [
    {"id": "t_machine_learning", "canonical_name": "Machine Learning"},
    {"id": "t_pytorch", "canonical_name": "PyTorch"},
    {"id": "t_customer_feedback", "canonical_name": "Customer Feedback Analysis"},
]


def main(text: str) -> None:
    print(f"Input text: {text}\n")
    ner = NERExtractor()
    entities = ner.extract(text)
    for ent in entities:
        print(f"Entity: {ent['text']:<30} Label: {ent['label']:<10} Score: {ent['score']:.3f}")

    linker = TopicLinker(topics=TOPICS)
    print("\nEntity linking suggestions:")
    for ent in entities:
        if ent["label"] in {"TOPIC", "ORG", "DOMAIN"}:
            link = linker.link(ent["text"])
            print(f"- {ent['text']} -> {link}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Please provide a text string to analyze.")
    main(sys.argv[1])
