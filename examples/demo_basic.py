# -*- coding: utf-8 -*-
"""Example: basic fast-path decision."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.types import Action, Decision


def main():
    model = CLMModel()
    engine = DecisionEngine(model)
    actions = [
        Action("search", "search_web", "look up current info"),
        Action("calc", "calc", "do arithmetic"),
        Action("mail", "send_email", "email someone"),
        Action("db", "query_db", "run SQL"),
    ]
    for state in ["what is 2+2?", "find latest news", "email bob the report", "count rows in users"]:
        res = engine.decide(Decision(state=state, actions=actions))
        print(f"{state!r} -> {res.selected}  (conf={res.confidence:.2f})")


if __name__ == "__main__":
    main()
