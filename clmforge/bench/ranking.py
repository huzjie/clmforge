# -*- coding: utf-8 -*-
"""Candidate ranking benchmark (order N candidates correctly)."""
from __future__ import annotations

from .base import Benchmark
from .datasets import make_dataset, tool_actions


def build(router, n: int = 200) -> Benchmark:
    decisions, correct_map = make_dataset(n, seed="ranking", actions=tool_actions(10))
    b = Benchmark(router, decisions, correct_map)
    b.name = "candidate_ranking"
    return b
