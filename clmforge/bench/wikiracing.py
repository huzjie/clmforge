# -*- coding: utf-8 -*-
"""WikiRacing benchmark (choose the next article link toward a target)."""
from __future__ import annotations

from typing import Dict, List

from ..types import Action, Decision
from .base import Benchmark


def build(router, n: int = 200) -> Benchmark:
    from ..backends.mock import world_answer
    links = ["Philosophy", "Science", "History", "Mathematics", "Art",
             "Technology", "Geography", "Biology", "Politics", "Economics"]
    actions = [Action(key=l, name=l) for l in links]
    decisions: List[Decision] = []
    correct_map: Dict[str, str] = {}
    for i in range(n):
        state = f"wiki-start-{i}: target=Philosophy"
        decisions.append(Decision(state=state, actions=actions))
        correct_map[state] = world_answer(state, actions)
    b = Benchmark(router, decisions, correct_map)
    b.name = "wikiracing"
    return b
