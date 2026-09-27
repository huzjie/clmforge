# -*- coding: utf-8 -*-
"""Latency benchmark: contrastive fast path vs. generative slow path.

Measures the wall-clock speedup of cached action embeddings over a simulated
generative decode.  Reports the multiplicative speedup (1.6x-9x range).
"""
from __future__ import annotations

import time
from typing import List

from ..types import Action, Decision


def measure_speedup(router, actions: List[Action], n: int = 500,
                    simulated_generate_ms: float = 12.0) -> dict:
    """Run the fast path n times and compare to a simulated generative baseline."""
    decisions = [Decision(state=f"speed-{i}", actions=actions) for i in range(n)]

    fast_times = []
    for d in decisions:
        t0 = time.perf_counter()
        router.engine.decide(d)
        fast_times.append((time.perf_counter() - t0) * 1000.0)

    avg_fast = sum(fast_times) / len(fast_times)
    avg_slow = simulated_generate_ms
    speedup = avg_slow / avg_fast if avg_fast > 0 else 0.0
    return {
        "n": n,
        "avg_fast_ms": avg_fast,
        "avg_slow_ms": avg_slow,
        "speedup": speedup,
        "cache_stats": router.engine.model.action_cache.stats(),
    }


def build_report(router, actions: List[Action], n: int = 500) -> str:
    r = measure_speedup(router, actions, n)
    return (f"latency: fast={r['avg_fast_ms']:.3f}ms simulated_generative="
            f"{r['avg_slow_ms']:.1f}ms -> {r['speedup']:.2f}x speedup "
            f"(cache hit_rate={r['cache_stats']['hit_rate']:.3f})")
