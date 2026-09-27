# -*- coding: utf-8 -*-
"""Embedding primitives: deterministic hash embeddings + optional numpy/torch paths."""
from __future__ import annotations

from typing import List, Optional

from .hashutil import stable_vector
from .exceptions import EmbeddingError

try:
    import numpy as _np  # type: ignore
except Exception:  # pragma: no cover
    _np = None

try:
    import torch as _torch  # type: ignore
except Exception:  # pragma: no cover
    _torch = None


def hash_embed(text: str, dim: int, scale: float = 1.0) -> List[float]:
    """Deterministic bag-of-hash embedding (no model required)."""
    return stable_vector(text, dim, scale)


def normalize(vec) -> list:
    if _np is not None and isinstance(vec, _np.ndarray):
        n = _np.linalg.norm(vec)
        return (vec / n).tolist() if n > 0 else vec.tolist()
    arr = list(vec)
    norm = sum(x * x for x in arr) ** 0.5
    if norm > 0:
        arr = [x / norm for x in arr]
    return arr


def dot(a, b) -> float:
    if _np is not None and isinstance(a, _np.ndarray) and isinstance(b, _np.ndarray):
        return float(_np.dot(a, b))
    return float(sum(x * y for x, y in zip(a, b)))


def cosine(a, b) -> float:
    na, nb = normalize(a), normalize(b)
    return dot(na, nb)


def stack(vectors: List[List[float]]):
    if _np is not None:
        return _np.asarray(vectors, dtype="float32")
    return vectors


def available_backends() -> List[str]:
    out = ["hash"]
    if _np is not None:
        out.append("numpy")
    if _torch is not None:
        out.append("torch")
    return out
