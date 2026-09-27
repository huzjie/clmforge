# -*- coding: utf-8 -*-
"""Action encoder: turn candidate actions into cacheable embeddings."""
from __future__ import annotations

from typing import List

from ..embeddings import hash_embed, normalize
from ..types import Action


class ActionEncoder:
    """Encodes actions independently of state so embeddings can be cached."""

    def __init__(self, dim: int, normalize_output: bool = True):
        self.dim = dim
        self.normalize_output = normalize_output

    def encode(self, action: Action) -> List[float]:
        text = action.to_text()
        vec = hash_embed(text, self.dim)
        if self.normalize_output:
            vec = normalize(vec)
        return vec

    def encode_all(self, actions: List[Action]) -> List[List[float]]:
        return [self.encode(a) for a in actions]
