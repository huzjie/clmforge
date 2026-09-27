# -*- coding: utf-8 -*-
"""Frozen-embeddings backend: uses the deterministic backbone directly (fast path)."""
from __future__ import annotations

from typing import List

from .. import constants as C
from ..models.backbone import FrozenBackbone
from ..models.action_encoder import ActionEncoder
from ..types import Action
from .base import BaseBackend


class FrozenEmbeddingsBackend(BaseBackend):
    kind = C.BACKEND_FROZEN

    def __init__(self, embed_dim: int = C.DEFAULT_EMBED_DIM):
        self.backbone = FrozenBackbone(dim=embed_dim)
        self.action_encoder = ActionEncoder(embed_dim)

    def encode_state(self, state: str) -> List[float]:
        return self.backbone.encode(state)

    def encode_actions(self, actions: List[Action]) -> List[List[float]]:
        return self.action_encoder.encode_all(actions)

    def generate(self, state: str, actions: List[Action]) -> str:
        return actions[0].key if actions else ""
