# -*- coding: utf-8 -*-
"""MCP (Model Context Protocol) tool-routing adapter."""
from __future__ import annotations

from typing import List

from ..models.clm_model import CLMModel
from ..engine.decision_engine import DecisionEngine
from ..types import Action, Decision


class MCPToolRouter:
    """Route an incoming MCP tool call to the best clmforge-scored tool."""

    def __init__(self, model: CLMModel = None):
        self.model = model or CLMModel()
        self.engine = DecisionEngine(self.model)

    def route(self, prompt: str, tools: List[dict]) -> str:
        actions = [Action(t.get("name", f"t{i}"), t.get("name", ""),
                          t.get("description", "")) for i, t in enumerate(tools)]
        res = self.engine.decide(Decision(state=prompt, actions=actions))
        return res.selected
