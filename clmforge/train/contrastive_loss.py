# -*- coding: utf-8 -*-
"""Contrastive losses for (state, action) score learning."""
from __future__ import annotations

import math
from typing import List


def infonce_loss(scores: List[float], positive_index: int, temperature: float = 0.07) -> float:
    """InfoNCE: -log( exp(s_p/t) / sum_j exp(s_j/t) )."""
    if not scores:
        return 0.0
    mx = max(scores)
    exps = [math.exp((s - mx) / temperature) for s in scores]
    total = sum(exps)
    return -(scores[positive_index] - mx) / temperature + math.log(total)


def margin_loss(scores: List[float], positive_index: int, margin: float = 0.5) -> float:
    """Hinge-style margin loss over the positive vs. all negatives."""
    if not scores:
        return 0.0
    loss = 0.0
    for j, s in enumerate(scores):
        if j == positive_index:
            continue
        loss += max(0.0, margin - (scores[positive_index] - s))
    return loss
