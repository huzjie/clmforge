# -*- coding: utf-8 -*-
"""Batch decision helper."""
from __future__ import annotations

from typing import List

from ..engine.decision_engine import DecisionEngine
from ..types import Decision


def decide_batch(engine: DecisionEngine, decisions: List[Decision]) -> List:
    return [engine.decide(d) for d in decisions]
