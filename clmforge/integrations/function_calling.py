# -*- coding: utf-8 -*-
"""Function-calling style router (OpenAI tools schema)."""
from __future__ import annotations

from typing import List

from ..models.clm_model import CLMModel
from ..engine.decision_engine import DecisionEngine
from ..types import Action, Decision


def route_functions(model: CLMModel, prompt: str, functions: List[dict]) -> str:
    """Pick the best function for *prompt* from OpenAI-style function schemas."""
    engine = DecisionEngine(model)
    actions = [Action(f.get("name", f"fn{i}"), f.get("name", ""),
                      f.get("description", "")) for i, f in enumerate(functions)]
    return engine.decide(Decision(state=prompt, actions=actions)).selected
