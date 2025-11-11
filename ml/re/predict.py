from typing import Dict

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

REL_LABELS = [
    "NO_RELATION",
    "HAS_EXPERTISE_IN",
    "COVERS",
    "ANSWERED_BY",
    "USED_FOR",
    "IMPLEMENTS_WITH",
    "RELATED_TO",
]


class REModel:
    def __init__(self, model_name: str = "re-roberta-base-starmind"):
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self._model.eval()

    def predict(self, sentence: str) -> Dict[str, object]:
        encoded = self._tokenizer(sentence, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self._model(**encoded).logits
            probs = torch.softmax(logits, dim=-1)[0]
            idx = int(torch.argmax(probs))
        return {"label": REL_LABELS[idx], "score": float(probs[idx])}
