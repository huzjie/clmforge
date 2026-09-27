# -*- coding: utf-8 -*-
"""Deterministic synthetic decision datasets (zero-dependency, reproducible)."""
from __future__ import annotations

from typing import Dict, List, Tuple

from ..types import Action, Decision

# A pool of "tools" for tool-calling style tasks.
TOOLS = [
    ("search_web", "Search the web for up-to-date information"),
    ("calc", "Perform an arithmetic calculation"),
    ("send_email", "Send an email to a recipient"),
    ("read_file", "Read a local file from disk"),
    ("write_file", "Write content to a local file"),
    ("browse", "Open a URL in a headless browser"),
    ("query_db", "Run a SQL query against the database"),
    ("deploy", "Deploy the application to staging"),
    ("fetch_weather", "Fetch current weather for a city"),
    ("translate", "Translate text between languages"),
]


def tool_actions(n: int = 6) -> List[Action]:
    return [Action(key=k, name=k, description=d) for k, d in TOOLS[:n]]


def make_dataset(n: int, seed: str = "clm", actions: List[Action] = None) -> Tuple[List[Decision], Dict[str, str]]:
    from ..backends.mock import world_answer
    actions = actions or tool_actions()
    decisions = []
    correct_map = {}
    for i in range(n):
        state = f"{seed}-task-{i}: user request #{i}"
        d = Decision(state=state, actions=actions)
        decisions.append(d)
        correct_map[state] = world_answer(state, actions)
    return decisions, correct_map
