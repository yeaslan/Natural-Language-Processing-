from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from fastapi import Body, Depends, FastAPI, HTTPException
from pydantic import BaseModel

from apps.api.graph.neo4j_client import KG
from apps.api.search.hybrid import HybridSearch
from ml.el.linker import TopicLinker
from ml.ner.predict import NERExtractor
from ml.re.predict import REL_LABELS, REModel

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "config.yaml"


class ExtractionRequest(BaseModel):
    text: str


class Config(BaseModel):
    storage: Dict[str, str]
    models: Dict[str, str]
    thresholds: Dict[str, float]
    chunking: Dict[str, int]
    security: Dict[str, str]


def load_config(path: Optional[str]) -> Config:
    cfg_path = Path(path or DEFAULT_CONFIG_PATH)
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found at {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Config(**data)


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = load_config(app.state.config_path)
    app.state.config = config

    ner_model = NERExtractor(model_name=config.models["ner"])
    app.state.ner = ner_model

    topic_linker = TopicLinker(
        model=config.models["embedding"],
        topics=[],
        accept=config.thresholds["el_accept"],
        cand=config.thresholds["el_candidate"],
    )
    app.state.topic_linker = topic_linker

    graph = KG(
        uri=config.storage["neo4j_uri"],
        user=config.storage["neo4j_user"],
        password=config.storage["neo4j_pass"],
    )
    app.state.graph = graph

    search = HybridSearch(config.storage["es_uri"], config.models["embedding"])
    app.state.hybrid_search = search

    re_model = REModel()
    app.state.re_model = re_model

    yield

    graph.close()
    search.close()


def get_config() -> Config:
    return app.state.config


def get_ner() -> NERExtractor:
    return app.state.ner


def get_linker() -> TopicLinker:
    return app.state.topic_linker


def get_graph() -> KG:
    return app.state.graph


def get_search() -> HybridSearch:
    return app.state.hybrid_search


def get_re_model() -> REModel:
    return app.state.re_model


app = FastAPI(
    title="Starmind NLP Case Study API",
    version="0.1.0",
    lifespan=lifespan,
)
app.state.config_path = Path(
    Path.cwd() / "configs" / "config.yaml"
)  # default overwritten in lifespan


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/nlp/extract")
def extract_entities(
    payload: ExtractionRequest,
    ner: NERExtractor = Depends(get_ner),
    linker: TopicLinker = Depends(get_linker),
):
    entities = ner.extract(payload.text)
    links: List[Dict[str, object]] = []
    for ent in entities:
        if ent["label"] in {"TOPIC", "ORG", "PERSON", "DOMAIN"}:
            links.append({"mention": ent["text"], "link": linker.link(ent["text"])})
    return {"entities": entities, "links": links}


@app.post("/kg/person-topic")
def upsert_person_topic(
    payload: Dict[str, object],
    graph: KG = Depends(get_graph),
):
    required = {"person_id", "topic_id", "score", "source"}
    if not required.issubset(payload.keys()):
        raise HTTPException(status_code=400, detail=f"Missing fields: {required - payload.keys()}")
    graph.upsert_person_topic(
        person_id=str(payload["person_id"]),
        topic_id=str(payload["topic_id"]),
        score=float(payload["score"]),
        source=str(payload["source"]),
    )
    return {"status": "ok"}


@app.get("/search/experts")
def search_experts(
    q: str,
    search: HybridSearch = Depends(get_search),
):
    results = search.search_documents(q)
    return {"query": q, "results": results}


@app.post("/nlp/relation")
def predict_relation(
    payload: Dict[str, str] = Body(...),
    re_model: REModel = Depends(get_re_model),
):
    sentence = payload.get("sentence")
    if not sentence:
        raise HTTPException(status_code=400, detail="`sentence` is required.")
    result = re_model.predict(sentence)
    return {"label": result["label"], "score": result["score"], "classes": REL_LABELS}
