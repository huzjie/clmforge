# -*- coding: utf-8 -*-
"""LangChain adapter: route tool calls via clmforge scoring."""
from __future__ import annotations

from typing import List

from ..models.clm_model import CLMModel
from ..engine.decision_engine import DecisionEngine
from ..types import Action, Decision


class LangChainToolRouter:
    """Wrap a CLMModel as a tool router for LangChain agents."""

    def __init__(self, model: CLMModel = None):
        self.model = model or CLMModel()
        self.engine = DecisionEngine(self.model)

    def select_tool(self, state: str, tools) -> str:
        actions = [Action(getattr(t, "name", str(t)), getattr(t, "name", str(t))) for t in tools]
        res = self.engine.decide(Decision(state=state, actions=actions))
        return res.selected

    def as_callable(self):
        return self.select_tool
