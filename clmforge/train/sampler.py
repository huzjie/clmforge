# -*- coding: utf-8 -*-
"""In-batch negative sampler for contrastive training."""
from __future__ import annotations

from typing import List

from ..hashutil import stable_ints
from .data import ContrastiveDataset


def sample_negatives(dataset: ContrastiveDataset, example_index: int,
                     n: int, seed: str = "neg") -> List[int]:
    """Pick *n* negative example indices (other examples) deterministically."""
    total = len(dataset)
    if total <= 1:
        return []
    idxs = stable_ints(seed + ":" + str(example_index), n * 2, 0, total - 1)
    out = []
    for i in idxs:
        if i != example_index and i not in out:
            out.append(i)
        if len(out) >= n:
            break
    return out
