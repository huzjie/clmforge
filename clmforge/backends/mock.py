# -*- coding: utf-8 -*-
"""Deterministic, trainable mock backend.

The mock is the key to a *real, runnable* zero-dependency demo: it uses a
deterministic world model so that "skill" (learnable) directly maps to answer
accuracy.  Higher skill -> higher score for the ground-truth action -> higher
benchmark accuracy.  This mirrors CLM's separation of a frozen backbone from a
learnable score head.
"""
from __future__ import annotations

from typing import List

from .. import constants as C
from ..hashutil import md5, stable_float
from ..types import Action
from ..models.state_encoder import StateEncoder
from ..models.action_encoder import ActionEncoder
from .base import BaseBackend


def world_answer(state: str, actions: List[Action]) -> str:
    """Deterministic ground-truth action for a state (shared by mock + benchmark)."""
    if not actions:
        return ""
    idx = int(md5("answer:" + state)[:8], 16) % len(actions)
    return actions[idx].key


class MockBackend(BaseBackend):
    kind = C.BACKEND_MOCK
    supports_training = True

    def __init__(self, embed_dim: int = C.DEFAULT_EMBED_DIM,
                 skill: float = 0.5, noise: float = 0.4):
        self.embed_dim = embed_dim
        self.skill = skill
        self.noise = noise
        self.state_encoder = StateEncoder(embed_dim)
        self.action_encoder = ActionEncoder(embed_dim)

    def encode_state(self, state: str) -> List[float]:
        return self.state_encoder.encode(state)

    def encode_actions(self, actions: List[Action]) -> List[List[float]]:
        return self.action_encoder.encode_all(actions)

    def _scores(self, state: str, actions: List[Action]) -> List[float]:
        correct = world_answer(state, actions)
        e_s = self.encode_state(state)
        out = []
        for a in actions:
            base = self.skill * 2.0 if a.key == correct else 0.0
            jitter = stable_float("jitter:" + state + "|" + a.key, -self.noise, self.noise)
            out.append(base + jitter)
        return out

    def generate(self, state: str, actions: List[Action]) -> str:
        scores = self._scores(state, actions)
        best = max(range(len(actions)), key=lambda i: scores[i])
        return actions[best].key

    def train_step(self, delta: float, lr: float = 0.05) -> None:
        self.skill = max(0.0, min(1.0, self.skill + lr * delta))
