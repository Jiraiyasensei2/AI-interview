"""
Semantic similarity via sentence-transformers.

This is the "not just TF-IDF" piece: instead of comparing bag-of-words
vectors, we embed the resume and job description into a dense vector space
where semantically similar phrases (e.g. "built REST APIs" vs "developed
backend web services") land close together even without exact word overlap.

The model is loaded once at process startup (see main.py's lifespan hook)
and reused across requests — loading it per-request would be very slow.
"""
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import EMBEDDING_MODEL_NAME


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load and cache the embedding model (singleton)."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    denom = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    if denom == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denom)


def semantic_match_score(resume_text: str, job_description: str) -> float:
    """
    Returns a 0-100 score representing semantic similarity between a resume
    and a job description.
    """
    model = get_model()
    embeddings = model.encode([resume_text, job_description], normalize_embeddings=True)
    score = cosine_similarity(embeddings[0], embeddings[1])
    # Cosine similarity on normalized sentence embeddings typically falls in
    # a ~[0, 1] band for related professional text; clip defensively and
    # scale to a friendlier 0-100 range.
    score = max(0.0, min(1.0, score))
    return round(score * 100, 2)
