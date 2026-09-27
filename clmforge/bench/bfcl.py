# -*- coding: utf-8 -*-
"""BFCL-style tool-calling benchmark (function selection)."""
from __future__ import annotations

from .base import Benchmark, BenchmarkResult
from .datasets import make_dataset, tool_actions


def build(router, n: int = 200) -> Benchmark:
    decisions, correct_map = make_dataset(n, seed="bfcl", actions=tool_actions())
    b = Benchmark(router, decisions, correct_map)
    b.name = "bfcl_tool_calling"
    return b
