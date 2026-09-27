# -*- coding: utf-8 -*-
"""Lightweight evaluation harness."""
from __future__ import annotations

import time
from typing import List

from ..types import Decision


def eval_accuracy(router, decisions: List[Decision], correct_map: dict) -> float:
    correct = sum(1 for d in decisions
                  if router.route(d).selected == correct_map.get(d.state, ""))
    return correct / len(decisions) if decisions else 0.0


def eval_latency(router, decisions: List[Decision], n: int = 3) -> float:
    times = []
    for _ in range(n):
        for d in decisions:
            t0 = time.perf_counter()
            router.route(d)
            times.append((time.perf_counter() - t0) * 1000.0)
    return sum(times) / len(times) if times else 0.0
