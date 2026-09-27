# -*- coding: utf-8 -*-
"""Frozen backbone abstraction.

In CLM-8B the backbone is a frozen transformer (Qwen3-8B) whose embeddings are
reused; only lightweight heads are trainable.  Here ``FrozenBackbone`` provides
the same contract with a deterministic fallback so the framework runs with zero
heavy dependencies, and can be swapped for a real encoder.
"""
from __future__ import annotations

from typing import List, Optional

from ..embeddings import hash_embed, normalize


class FrozenBackbone:
    def __init__(self, dim: int = 64, name: str = "hash-frozen"):
        self.dim = dim
        self.name = name
        self.frozen = True

    def encode(self, text: str) -> List[float]:
        vec = hash_embed(text, self.dim)
        return normalize(vec)

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.encode(t) for t in texts]

    def trainable_parameters(self) -> int:
        return 0
