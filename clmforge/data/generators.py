# -*- coding: utf-8 -*-
"""Deterministic synthetic data generators."""
from __future__ import annotations

from typing import Dict, List, Tuple

from ..backends.mock import world_answer
from ..types import Action, Decision


def tool_choice_data(n: int, seed: str = "data") -> Tuple[List[Decision], Dict[str, str]]:
    """Return (decisions, correct_map) for tool-choice tasks."""
    tools = [
        Action("search", "search_web"), Action("calc", "calc"),
        Action("mail", "send_email"), Action("file", "read_file"),
        Action("sql", "query_db"), Action("deploy", "deploy"),
    ]
    decisions, correct_map = [], {}
    for i in range(n):
        state = f"{seed}-tool-{i}"
        decisions.append(Decision(state=state, actions=tools))
        correct_map[state] = world_answer(state, tools)
    return decisions, correct_map


def ranking_data(n: int, seed: str = "rank") -> Tuple[List[Decision], Dict[str, str]]:
    """Return (decisions, correct_map) for ranking tasks with 10 candidates."""
    candidates = [Action(f"c{i}", f"candidate_{i}") for i in range(10)]
    decisions, correct_map = [], {}
    for i in range(n):
        state = f"{seed}-{i}"
        decisions.append(Decision(state=state, actions=candidates))
        correct_map[state] = world_answer(state, candidates)
    return decisions, correct_map
