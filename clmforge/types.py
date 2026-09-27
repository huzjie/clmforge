# -*- coding: utf-8 -*-
"""Core dataclasses shared across clmforge."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Action:
    """A candidate action the decision engine can select."""

    key: str
    name: str = ""
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def label(self) -> str:
        return self.name or self.key

    def to_text(self) -> str:
        parts = [self.label()]
        if self.description:
            parts.append(self.description)
        if self.metadata:
            parts.append(str(self.metadata))
        return " | ".join(parts)


@dataclass
class Decision:
    """A single (state, action-set) decision request."""

    state: str
    actions: List[Action]
    state_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def action_keys(self) -> List[str]:
        return [a.key for a in self.actions]


@dataclass
class ScoreResult:
    """Scored outcome for one action."""

    key: str
    score: float
    logit: float = 0.0
    rank: int = -1
    embedding: Optional[List[float]] = None


@dataclass
class DecisionResult:
    """Full result of a decision request."""

    state: str
    selected: Optional[str] = None
    scores: List[ScoreResult] = field(default_factory=list)
    path: str = "fast"           # fast | slow
    confidence: float = 0.0
    latency_ms: float = 0.0
    cache_hits: int = 0
    meta: Dict[str, Any] = field(default_factory=dict)

    def ranking(self) -> List[str]:
        return [s.key for s in sorted(self.scores, key=lambda x: x.score, reverse=True)]

    def best(self) -> Optional[ScoreResult]:
        if not self.scores:
            return None
        return max(self.scores, key=lambda x: x.score)
