# -*- coding: utf-8 -*-
"""Accumulate decision metrics (latency, cache hits, path split)."""
from __future__ import annotations

from typing import List


class DecisionMetrics:
    def __init__(self):
        self.latencies: List[float] = []
        self.cache_hits: List[int] = []
        self.paths: dict = {"fast": 0, "slow": 0}
        self.total = 0

    def record(self, result) -> None:
        self.total += 1
        self.latencies.append(result.latency_ms)
        self.cache_hits.append(result.cache_hits)
        self.paths[result.path] = self.paths.get(result.path, 0) + 1

    def summary(self) -> dict:
        n = max(1, self.total)
        return {
            "total": self.total,
            "avg_latency_ms": sum(self.latencies) / n,
            "p99_latency_ms": sorted(self.latencies)[int(n * 0.99) - 1] if self.total else 0.0,
            "avg_cache_hits": sum(self.cache_hits) / n,
            "fast_ratio": self.paths.get("fast", 0) / n,
        }
