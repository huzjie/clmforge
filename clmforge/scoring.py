# -*- coding: utf-8 -*-
"""Score heads: turn (state_embedding, action_embedding) into a scalar score."""
from __future__ import annotations

from typing import List, Optional

from . import constants as C
from .embeddings import dot
from .exceptions import ScoringError


class ScoreHead:
    """Base score head.  Subclasses implement ``score``."""

    kind: str = "base"

    def __init__(self, dim: int):
        self.dim = dim

    def score(self, state_vec, action_vec) -> float:
        raise NotImplementedError

    def score_all(self, state_vec, action_vecs: List[List[float]]) -> List[float]:
        return [self.score(state_vec, a) for a in action_vecs]


class LinearHead(ScoreHead):
    kind = C.HEAD_LINEAR

    def __init__(self, dim: int, weight: Optional[List[float]] = None):
        super().__init__(dim)
        self.weight = list(weight) if weight is not None else [1.0] * dim

    def score(self, state_vec, action_vec) -> float:
        combined = [s * w for s, w in zip(state_vec, self.weight)]
        return dot(combined, action_vec)


class BilinearHead(ScoreHead):
    kind = C.HEAD_BILINEAR

    def __init__(self, dim: int, matrix: Optional[List[List[float]]] = None):
        super().__init__(dim)
        if matrix is None:
            self.matrix = [[1.0 if i == j else 0.0 for j in range(dim)] for i in range(dim)]
        else:
            self.matrix = matrix

    def score(self, state_vec, action_vec) -> float:
        # s^T W a
        total = 0.0
        for i, sv in enumerate(state_vec):
            row = self.matrix[i]
            total += sv * sum(w * a for w, a in zip(row, action_vec))
        return total


class MLPHead(ScoreHead):
    kind = C.HEAD_MLP

    def __init__(self, dim: int, hidden: int = 32, weights: Optional[dict] = None):
        super().__init__(dim)
        self.hidden = hidden
        self.weights = weights or {}

    def score(self, state_vec, action_vec) -> float:
        # single-hidden-layer MLP on the concatenation
        x = list(state_vec) + list(action_vec)
        w1 = self.weights.get("w1", [1.0 / max(1, len(x))] * (len(x) * self.hidden))
        b1 = self.weights.get("b1", [0.0] * self.hidden)
        w2 = self.weights.get("w2", [1.0 / max(1, self.hidden)] * self.hidden)
        b2 = self.weights.get("b2", 0.0)
        hidden = []
        for j in range(self.hidden):
            acc = b1[j]
            for i, xi in enumerate(x):
                acc += xi * w1[i * self.hidden + j]
            hidden.append(max(0.0, acc))
        return b2 + sum(h * w for h, w in zip(hidden, w2))


def make_head(kind: str, dim: int, **kwargs) -> ScoreHead:
    if kind == C.HEAD_LINEAR:
        return LinearHead(dim, kwargs.get("weight"))
    if kind == C.HEAD_BILINEAR:
        return BilinearHead(dim, kwargs.get("matrix"))
    if kind == C.HEAD_MLP:
        return MLPHead(dim, kwargs.get("hidden", 32), kwargs.get("weights"))
    raise ScoringError(f"unknown head type {kind!r}")
