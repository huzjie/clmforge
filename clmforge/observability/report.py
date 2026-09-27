# -*- coding: utf-8 -*-
"""Render a markdown report from DecisionMetrics."""
from __future__ import annotations


def render_report(metrics) -> str:
    s = metrics.summary()
    return (
        f"# clmforge 决策报告\n\n"
        f"- 总决策数: {s['total']}\n"
        f"- 平均延迟: {s['avg_latency_ms']:.3f} ms\n"
        f"- P99 延迟: {s['p99_latency_ms']:.3f} ms\n"
        f"- 平均缓存命中: {s['avg_cache_hits']:.2f}\n"
        f"- 快路径占比: {s['fast_ratio']:.2%}\n"
    )
