# -*- coding: utf-8 -*-
"""Benchmark runner: run all built-in benchmarks and print a table."""
from __future__ import annotations

from typing import List

from . import bfcl, gaming, ranking, verification, wikiracing


def run_all(router, n: int = 200, verbose: bool = True) -> List:
    benchmarks = [
        bfcl.build(router, n),
        ranking.build(router, n),
        verification.build(router, n),
        gaming.build(router, n),
        wikiracing.build(router, n),
    ]
    results = []
    for b in benchmarks:
        r = b.run()
        results.append(r)
        if verbose:
            print(r.summary(), flush=True)
    avg = sum(r.accuracy for r in results) / len(results) if results else 0.0
    if verbose:
        print(f"--- AVG accuracy: {avg:.3f} ---", flush=True)
    return results
