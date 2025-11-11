from typing import Dict, List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer, util


class TopicLinker:
    def __init__(
        self,
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
        topics: Optional[List[Dict[str, str]]] = None,
        accept: float = 0.72,
        cand: float = 0.60,
    ):
        self._encoder = SentenceTransformer(model)
        self._topics = topics or []
        self._accept = accept
        self._candidate = cand
        self._topic_embeddings = (
            self._encoder.encode(
                [t["canonical_name"] for t in self._topics],
                normalize_embeddings=True,
            )
            if self._topics
            else np.zeros((0, self._encoder.get_sentence_embedding_dimension()))
        )

    def update_topics(self, topics: List[Dict[str, str]]) -> None:
        self._topics = topics
        self._topic_embeddings = self._encoder.encode(
            [t["canonical_name"] for t in self._topics],
            normalize_embeddings=True,
        )

    def link(self, mention: str) -> Dict[str, object]:
        if not self._topics:
            return {"target": None, "score": 0.0, "status": "unknown"}
        mention_emb = self._encoder.encode([mention], normalize_embeddings=True)
        sims = util.cos_sim(mention_emb, self._topic_embeddings).cpu().numpy()[0]
        best_idx = int(np.argmax(sims))
        score = float(sims[best_idx])
        status = "reject"
        if score >= self._accept:
            status = "accept"
        elif score >= self._candidate:
            status = "candidate"
        return {"target": self._topics[best_idx], "score": score, "status": status}
