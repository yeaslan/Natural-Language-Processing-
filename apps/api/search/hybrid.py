from typing import List

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer


class HybridSearch:
    def __init__(self, es_uri: str, embedding_model: str):
        self._client = Elasticsearch(es_uri)
        self._encoder = SentenceTransformer(embedding_model)

    def close(self) -> None:
        self._client.transport.close()

    def search_documents(self, query: str, k: int = 20, num_candidates: int = 100) -> List[dict]:
        vector = self._encoder.encode([query], normalize_embeddings=True)[0]
        response = self._client.search(
            index="documents",
            size=k,
            query={"match": {"content": query}},
            knn={
                "field": "vector",
                "query_vector": vector.tolist(),
                "k": k,
                "num_candidates": num_candidates,
            },
        )
        return response.get("hits", {}).get("hits", [])
