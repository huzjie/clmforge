# -*- coding: utf-8 -*-
"""Example: batch decision."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.integrations.batch import decide_batch
from clmforge.types import Action, Decision


def main():
    model = CLMModel()
    engine = DecisionEngine(model)
    actions = [Action("accept", "accept"), Action("reject", "reject")]
    decisions = [Decision(state=f"case-{i}", actions=actions) for i in range(50)]
    results = decide_batch(engine, decisions)
    accepts = sum(1 for r in results if r.selected == "accept")
    print(f"50 cases: accept={accepts} reject={50 - accepts}")


if __name__ == "__main__":
    main()
