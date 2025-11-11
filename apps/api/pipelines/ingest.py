from hashlib import sha256
from typing import Dict
import re

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}")
HTML_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    cleaned = HTML_RE.sub(" ", text)
    cleaned = WHITESPACE_RE.sub(" ", cleaned)
    return cleaned.strip()


def scrub_pii(text: str) -> str:
    return EMAIL_RE.sub("[EMAIL]", text)


def hash_email(email: str, salt: str) -> str:
    return sha256((salt + email.lower()).encode("utf-8")).hexdigest()


def prepare_document(payload: Dict[str, str], pii_salt: str) -> Dict[str, str]:
    text = payload.get("text") or ""
    cleaned = scrub_pii(clean_text(text))
    author = payload.get("author")
    author_hash = hash_email(author, pii_salt) if author else None
    return {
        "id": payload.get("id"),
        "title": payload.get("title"),
        "text": cleaned,
        "source": payload.get("source", "unknown"),
        "author_hash": author_hash,
    }
