# -*- coding: utf-8 -*-
"""Router: decide between the fast (contrastive) and slow (generative) path.

CLM's whole thesis is separating fast decisions from expensive reasoning.  The
router uses the score margin to decide whether the contrastive answer is
confident enough; low-margin decisions fall back to the slow backend.
"""
from __future__ import annotations

from typing import List, Optional

from .. import constants as C
from ..types import Action, Decision, DecisionResult
from .decision_engine import DecisionEngine
from .confidence import confidence_margin


class Router:
    def __init__(self, engine: DecisionEngine,
                 mode: str = C.ROUTER_MARGIN,
                 margin_threshold: float = C.DEFAULT_CONFIDENCE_THRESHOLD,
                 slow_backend=None):
        self.engine = engine
        self.mode = mode
        self.margin_threshold = margin_threshold
        self.slow_backend = slow_backend
        self.stats = {"fast": 0, "slow": 0}

    def route(self, decision: Decision) -> DecisionResult:
        if self.mode == C.ROUTER_ALWAYS_SLOW:
            return self._slow(decision)
        if self.mode == C.ROUTER_ALWAYS_FAST:
            result = self.engine.decide(decision)
            self.stats["fast"] += 1
            return result

        result = self.engine.decide(decision)
        if result.confidence >= self.margin_threshold or self.slow_backend is None:
            self.stats["fast"] += 1
            return result
        return self._slow(decision)

    def _slow(self, decision: Decision) -> DecisionResult:
        self.stats["slow"] += 1
        key = self.slow_backend.generate(decision.state, decision.actions)
        from ..types import ScoreResult
        res = DecisionResult(state=decision.state, selected=key, path=C.SLOW_PATH,
                             confidence=1.0, meta={"routed": "slow"})
        res.scores = [ScoreResult(key=key, score=1.0, rank=0)]
        return res

    def ratio(self) -> float:
        total = self.stats["fast"] + self.stats["slow"]
        return self.stats["fast"] / total if total else 1.0
