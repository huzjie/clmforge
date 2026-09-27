# -*- coding: utf-8 -*-
"""Action selection strategies (greedy, temperature sampling, top-k)."""
from __future__ import annotations

import random
from typing import List, Optional

from ..types import ScoreResult
from .confidence import softmax


def greedy(results: List[ScoreResult]) -> Optional[str]:
    if not results:
        return None
    return max(results, key=lambda r: r.score).key


def sample(results: List[ScoreResult], temperature: float = 1.0, seed: Optional[int] = None) -> Optional[str]:
    if not results:
        return None
    probs = softmax([r.score for r in results], temperature)
    rng = random.Random(seed)
    r = rng.random()
    acc = 0.0
    for res, p in zip(results, probs):
        acc += p
        if r <= acc:
            return res.key
    return results[-1].key


def top_k(results: List[ScoreResult], k: int) -> List[str]:
    return [r.key for r in sorted(results, key=lambda x: x.score, reverse=True)[:k]]
