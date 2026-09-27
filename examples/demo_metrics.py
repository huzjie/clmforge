# -*- coding: utf-8 -*-
"""Example: observability metrics."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.observability.metrics import DecisionMetrics
from clmforge.types import Action, Decision


def main():
    model = CLMModel(skill=0.8)
    engine = DecisionEngine(model)
    router = Router(engine, mode="always_fast")
    actions = [Action(f"a{i}", f"a{i}") for i in range(6)]
    metrics = DecisionMetrics()
    for i in range(200):
        res = router.route(Decision(state=f"req-{i}", actions=actions))
        metrics.record(res)
    print(metrics.summary())


if __name__ == "__main__":
    main()
