from typing import Dict, List

from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline


class NERExtractor:
    def __init__(self, model_name: str = "dslim/bert-base-NER"):
        self._pipeline = pipeline(
            "ner",
            model=AutoModelForTokenClassification.from_pretrained(model_name),
            tokenizer=AutoTokenizer.from_pretrained(model_name),
            aggregation_strategy="simple",
        )
        self._label_map = {"ORG": "ORG", "PER": "PERSON", "LOC": "DOMAIN", "MISC": "TOPIC"}

    def extract(self, text: str) -> List[Dict[str, object]]:
        entities = self._pipeline(text)
        results: List[Dict[str, object]] = []
        for ent in entities:
            label = self._label_map.get(ent["entity_group"], "MISC")
            results.append(
                {
                    "text": ent["word"],
                    "label": label,
                    "start": int(ent["start"]),
                    "end": int(ent["end"]),
                    "score": float(ent["score"]),
                }
            )
        return results
