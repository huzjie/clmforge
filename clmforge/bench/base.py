# -*- coding: utf-8 -*-
"""Benchmark base class."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..types import Decision


@dataclass
class BenchmarkResult:
    name: str
    accuracy: float
    avg_latency_ms: float
    fast_ratio: float
    cache_hit_rate: float
    total: int
    meta: dict = field(default_factory=dict)

    def summary(self) -> str:
        return (f"{self.name}: acc={self.accuracy:.3f} "
                f"latency={self.avg_latency_ms:.1f}ms "
                f"fast_ratio={self.fast_ratio:.2f} "
                f"cache_hit={self.cache_hit_rate:.2f} (n={self.total})")


class Benchmark:
    name = "benchmark"

    def __init__(self, router, decisions: List[Decision], correct_map: dict):
        self.router = router
        self.decisions = decisions
        self.correct_map = correct_map

    def run(self) -> BenchmarkResult:
        correct = 0
        latencies = []
        fast = 0
        hits = 0
        for d in self.decisions:
            res = self.router.route(d)
            if res.selected == self.correct_map.get(d.state, ""):
                correct += 1
            if res.path == "fast":
                fast += 1
            latencies.append(res.latency_ms)
            hits += res.cache_hits
        total = len(self.decisions)
        acc = correct / total if total else 0.0
        avg_lat = sum(latencies) / total if total else 0.0
        return BenchmarkResult(
            name=self.name, accuracy=acc, avg_latency_ms=avg_lat,
            fast_ratio=fast / total if total else 0.0,
            cache_hit_rate=hits / total if total else 0.0,
            total=total,
        )
