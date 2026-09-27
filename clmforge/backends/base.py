# -*- coding: utf-8 -*-
"""Backend contract."""
from __future__ import annotations

from typing import List, Tuple

from ..types import Action


class BaseBackend:
    kind = "base"
    supports_training = False

    def encode_state(self, state: str) -> List[float]:
        raise NotImplementedError

    def encode_actions(self, actions: List[Action]) -> List[List[float]]:
        raise NotImplementedError

    def generate(self, state: str, actions: List[Action]) -> str:
        """Slow-path generative answer; returns the selected action key."""
        raise NotImplementedError

    def train_step(self, delta: float, lr: float = 0.05) -> None:
        raise NotImplementedError
