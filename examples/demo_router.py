# -*- coding: utf-8 -*-
"""Example: fast/slow routing by margin."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.backends.mock import MockBackend
from clmforge.types import Action, Decision


def main():
    model = CLMModel()
    engine = DecisionEngine(model)
    slow = MockBackend(skill=0.9, noise=0.1)
    router = Router(engine, mode="margin", margin_threshold=0.2, slow_backend=slow)

    actions = [Action("yes", "yes"), Action("no", "no")]
    for state in ["approve", "reject", "hold", "escalate"]:
        res = router.route(Decision(state=state, actions=actions))
        print(f"{state} -> {res.selected} via {res.path} (conf={res.confidence:.2f})")
    print("router stats:", router.stats)


if __name__ == "__main__":
    main()
