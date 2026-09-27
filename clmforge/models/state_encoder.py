# -*- coding: utf-8 -*-
"""State encoder: turn a context string into a reusable state embedding."""
from __future__ import annotations

from typing import List, Optional

from ..embeddings import hash_embed, normalize


class StateEncoder:
    """Encodes states (contexts) into dense vectors.

    The frozen-backbone path uses hash embeddings as a deterministic stand-in
    for a frozen transformer encoder; plugging in a real backbone (Qwen3-8B)
    only requires overriding ``encode``.
    """

    def __init__(self, dim: int, normalize_output: bool = True):
        self.dim = dim
        self.normalize_output = normalize_output

    def encode(self, state: str) -> List[float]:
        vec = hash_embed(state, self.dim)
        if self.normalize_output:
            vec = normalize(vec)
        return vec

    def encode_batch(self, states: List[str]) -> List[List[float]]:
        return [self.encode(s) for s in states]
