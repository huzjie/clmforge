# -*- coding: utf-8 -*-
"""DecisionEngine: the core fast-path scorer.

Scores a state against a candidate action set via the contrastive model and
returns a ranked DecisionResult.  Action embeddings are pulled from the cache
(independent, reusable).
"""
from __future__ import annotations

import time
from typing import List, Optional

from .. import constants as C
from ..models.clm_model import CLMModel
from ..types import Action, Decision, DecisionResult, ScoreResult


class DecisionEngine:
    def __init__(self, model: CLMModel, top_k: int = C.DEFAULT_TOP_K):
        self.model = model
        self.top_k = top_k

    def decide(self, decision: Decision, temperature: float = 1.0) -> DecisionResult:
        start = time.perf_counter()
        scores, hits = self.model.score(decision.state, decision.actions)
        results = []
        for i, a in enumerate(decision.actions):
            results.append(ScoreResult(key=a.key, score=scores[i], logit=scores[i]))
        ranked = sorted(results, key=lambda r: r.score, reverse=True)
        for rank, r in enumerate(ranked):
            r.rank = rank
        selected = ranked[0].key if ranked else None
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        from .confidence import confidence_margin
        margin = confidence_margin([r.score for r in results])
        return DecisionResult(
            state=decision.state,
            selected=selected,
            scores=results,
            path=C.FAST_PATH,
            confidence=margin,
            latency_ms=elapsed_ms,
            cache_hits=hits,
            meta={"temperature": temperature, "top_k": self.top_k},
        )
