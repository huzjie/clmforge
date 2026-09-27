# -*- coding: utf-8 -*-
"""Confidence / margin helpers for routing."""
from __future__ import annotations

from typing import List


def confidence_margin(scores: List[float]) -> float:
    """Return the normalized gap between the top two scores (>=0)."""
    if not scores:
        return 0.0
    if len(scores) == 1:
        return 1.0
    ordered = sorted(scores, reverse=True)
    top, second = ordered[0], ordered[1]
    span = max(1e-9, top - min(scores))
    return max(0.0, (top - second) / span)


def softmax(scores: List[float], temperature: float = 1.0) -> List[float]:
    import math
    if not scores:
        return []
    mx = max(scores)
    exps = [math.exp((s - mx) / temperature) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]
