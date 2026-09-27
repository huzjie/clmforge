# -*- coding: utf-8 -*-
"""Sampling helpers."""
from __future__ import annotations

from typing import List

from ..hashutil import stable_ints


def deterministic_split(n: int, train_ratio: float = 0.8, seed: str = "split") -> List[int]:
    """Return a deterministic list of 0/1 (1=train) assignments."""
    idxs = stable_ints(seed, n, 0, 1000)
    cutoff = int(train_ratio * 1000)
    return [1 if v < cutoff else 0 for v in idxs]
