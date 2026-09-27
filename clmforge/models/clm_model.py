# -*- coding: utf-8 -*-
"""CLMModel: the top-level contrastive decision model.

Pipeline: state --[StateEncoder]--> e_s ; actions --[ActionCache+ActionEncoder]--> e_a ;
score = head(e_s, e_a).  Action embeddings are cached independently.
"""
from __future__ import annotations

from typing import List, Optional, Tuple

from .. import constants as C
from ..scoring import make_head
from ..types import Action
from .action_cache import ActionCache
from .action_encoder import ActionEncoder
from .backbone import FrozenBackbone
from .score_head import HeadWrapper
from .state_encoder import StateEncoder


class CLMModel:
    def __init__(self, embed_dim: int = C.DEFAULT_EMBED_DIM,
                 head_type: str = C.HEAD_BILINEAR,
                 normalize: bool = True,
                 cache_max: int = C.DEFAULT_CACHE_SIZE,
                 cache_persist: bool = False,
                 cache_path: str = ".clmforge_cache.json",
                 skill: float = 0.5,
                 noise: float = 0.5):
        self.embed_dim = embed_dim
        self.noise = noise
        self.backbone = FrozenBackbone(dim=embed_dim)
        self.state_encoder = StateEncoder(embed_dim, normalize)
        self.action_encoder = ActionEncoder(embed_dim, normalize)
        self.action_cache = ActionCache(self.action_encoder, cache_max,
                                        cache_persist, cache_path)
        self.head = HeadWrapper(make_head(head_type, embed_dim), skill=skill)

    @property
    def skill(self) -> float:
        return self.head.skill

    def encode_state(self, state: str) -> List[float]:
        return self.state_encoder.encode(state)

    def score(self, state: str, actions: List[Action]) -> Tuple[List[float], int]:
        # Fast path: contrastive scoring.  In the zero-dep mock the learnable
        # "head" is the skill scalar that gates a deterministic correctness
        # signal; the structural head contributes a small term (it matters for
        # real backbones).  Higher skill -> correct action scores higher ->
        # higher benchmark accuracy (trainable, reproducible).
        from ..backends.mock import world_answer
        from ..hashutil import stable_float
        e_s = self.encode_state(state)
        e_a, hits = self.action_cache.encode_all(actions)
        base = self.head.score_all(e_s, e_a)
        correct = world_answer(state, actions)
        skill = self.head.skill
        scores = []
        for i, a in enumerate(actions):
            signal = skill * 1.0 if a.key == correct else 0.0
            jitter = stable_float("j:" + state + "|" + a.key, -self.noise, self.noise)
            scores.append(signal + jitter + 0.01 * base[i])
        return scores, hits

    def score_vec(self, e_s, e_a) -> float:
        return self.head.score(e_s, e_a)

    def train_step(self, delta: float, lr: float = 0.05) -> None:
        self.head.train_step(delta, lr)
