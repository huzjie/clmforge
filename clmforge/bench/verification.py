# -*- coding: utf-8 -*-
"""Verification benchmark (accept/reject a proposed action)."""
from __future__ import annotations

from typing import Dict, List

from ..types import Action, Decision
from .base import Benchmark


def build(router, n: int = 200) -> Benchmark:
    from ..backends.mock import world_answer
    decisions: List[Decision] = []
    correct_map: Dict[str, str] = {}
    for i in range(n):
        state = f"verify-task-{i}: is this action correct?"
        # binary-style: candidate + decoy
        actions = [
            Action(key="accept", name="accept", description="the proposal is correct"),
            Action(key="reject", name="reject", description="the proposal is wrong"),
        ]
        decisions.append(Decision(state=state, actions=actions))
        correct_map[state] = world_answer(state, actions)
    b = Benchmark(router, decisions, correct_map)
    b.name = "verification"
    return b
