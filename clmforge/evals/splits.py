# -*- coding: utf-8 -*-
"""Train/eval split utilities."""
from __future__ import annotations

from typing import List

from ..data.sampling import deterministic_split


def split_indices(n: int, train_ratio: float = 0.8) -> tuple:
    mask = deterministic_split(n, train_ratio)
    train = [i for i, m in enumerate(mask) if m]
    eval_idx = [i for i, m in enumerate(mask) if not m]
    return train, eval_idx
