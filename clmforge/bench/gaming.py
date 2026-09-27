# -*- coding: utf-8 -*-
"""Gaming benchmark (pick next move among discrete actions)."""
from __future__ import annotations

from typing import Dict, List

from ..types import Action, Decision
from .base import Benchmark


def build(router, n: int = 200) -> Benchmark:
    from ..backends.mock import world_answer
    moves = ["up", "down", "left", "right", "jump", "fire", "use", "drop"]
    actions = [Action(key=m, name=m) for m in moves]
    decisions: List[Decision] = []
    correct_map: Dict[str, str] = {}
    for i in range(n):
        state = f"game-state-{i}: frame={i} enemies=near"
        decisions.append(Decision(state=state, actions=actions))
        correct_map[state] = world_answer(state, actions)
    b = Benchmark(router, decisions, correct_map)
    b.name = "gaming"
    return b
