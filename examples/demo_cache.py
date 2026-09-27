# -*- coding: utf-8 -*-
"""Example: action-embedding cache speedup."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.types import Action, Decision


def main():
    model = CLMModel()
    engine = DecisionEngine(model)
    actions = [Action(f"tool_{i}", f"tool_{i}", f"tool number {i}") for i in range(50)]

    # first pass: cold cache (all misses)
    for i in range(20):
        engine.decide(Decision(state=f"req-{i}", actions=actions))
    print("after cold pass:", model.action_cache.stats())

    # second pass: warm cache (same action set -> hits)
    for i in range(20, 40):
        engine.decide(Decision(state=f"req-{i}", actions=actions))
    print("after warm pass:", model.action_cache.stats())


if __name__ == "__main__":
    main()
