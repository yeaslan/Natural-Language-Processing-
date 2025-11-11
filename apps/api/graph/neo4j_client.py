from typing import Any, Dict, Iterable, Optional

from neo4j import GraphDatabase


class KG:
    def __init__(self, uri: str, user: str, password: str, database: Optional[str] = None):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database

    def close(self) -> None:
        self._driver.close()

    def upsert_person_topic(self, person_id: str, topic_id: str, score: float, source: str) -> None:
        query = """
        MERGE (p:Person {id: $person_id})
        MERGE (t:Topic {id: $topic_id})
        MERGE (p)-[r:HAS_EXPERTISE_IN]->(t)
        ON CREATE SET
            r.score = $score,
            r.source = $source,
            r.updated_at = timestamp()
        ON MATCH SET
            r.score = CASE WHEN $score > r.score THEN $score ELSE r.score END,
            r.updated_at = timestamp()
        """
        self._run(query, person_id=person_id, topic_id=topic_id, score=score, source=source)

    def upsert_nodes(self, label: str, nodes: Iterable[Dict[str, Any]]) -> None:
        query = f"""
        UNWIND $nodes AS node
        MERGE (n:{label} {{id: node.id}})
        SET n += node.props
        """
        formatted = [{"id": node["id"], "props": {k: v for k, v in node.items() if k != "id"}} for node in nodes]
        self._run(query, nodes=formatted)

    def upsert_edge(self, start_label: str, end_label: str, rel_type: str, data: Dict[str, Any]) -> None:
        query = f"""
        MERGE (s:{start_label} {{id: $start_id}})
        MERGE (e:{end_label} {{id: $end_id}})
        MERGE (s)-[r:{rel_type}]->(e)
        SET r += $props,
            r.updated_at = timestamp()
        """
        props = {k: v for k, v in data.items() if k not in {"start_id", "end_id"}}
        self._run(query, start_id=data["start_id"], end_id=data["end_id"], props=props)

    def _run(self, query: str, **params: Any) -> None:
        if self._database:
            with self._driver.session(database=self._database) as session:
                session.run(query, **params)
        else:
            with self._driver.session() as session:
                session.run(query, **params)
