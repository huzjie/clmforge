# -*- coding: utf-8 -*-
"""Trainable score-head wrapper (lightweight; the only part that is fine-tuned)."""
from __future__ import annotations

from typing import List, Optional

from ..scoring import make_head, ScoreHead


class HeadWrapper:
    """Wraps a score head and tracks a learnable skill level (for mock training)."""

    def __init__(self, head: ScoreHead, skill: float = 0.5):
        self.head = head
        self.skill = skill

    def score(self, state_vec, action_vec) -> float:
        return self.head.score(state_vec, action_vec)

    def score_all(self, state_vec, action_vecs: List[List[float]]) -> List[float]:
        return self.head.score_all(state_vec, action_vecs)

    def train_step(self, delta: float, lr: float = 0.05) -> None:
        """Adjust skill toward 1.0 (used by the trainable mock backend)."""
        self.skill = max(0.0, min(1.0, self.skill + lr * delta))
