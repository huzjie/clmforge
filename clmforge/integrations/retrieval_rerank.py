# -*- coding: utf-8 -*-
"""Retrieval re-ranking: score (query, document) pairs contrastively."""
from __future__ import annotations

from typing import List, Tuple

from ..models.clm_model import CLMModel
from ..types import Action


def rerank(model: CLMModel, query: str, documents: List[str], top_n: int = 5) -> List[Tuple[str, float]]:
    """Return top_n (document, score) pairs for *query*."""
    actions = [Action(str(i), doc[:80]) for i, doc in enumerate(documents)]
    scores, _ = model.score(query, actions)
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]
