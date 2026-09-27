# -*- coding: utf-8 -*-
"""Example: full benchmark suite."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.backends.mock import MockBackend
from clmforge.bench.runner import run_all
from clmforge.bench.latency import build_report
from clmforge.bench.datasets import tool_actions


def main():
    model = CLMModel(skill=0.7)
    engine = DecisionEngine(model)
    router = Router(engine, mode="always_fast", slow_backend=MockBackend(skill=0.9))
    run_all(router, n=200)
    print(build_report(router, tool_actions(), n=500))


if __name__ == "__main__":
    main()
