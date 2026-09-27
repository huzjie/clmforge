# -*- coding: utf-8 -*-
"""clmforge — Contrastive Language Model for fast decision-making.

A decision engine that scores candidate (state, action) pairs through a shared
embedding space instead of autoregressively generating text.  Action embeddings
are independently cacheable, yielding up to 9x lower latency than generative
decision models (e.g. Jev) on bounded-choice tasks: tool routing, candidate
ranking, verification, and gaming.

Reference: CLM-8B (Stanford x NVIDIA, Apache 2.0) — frozen Qwen3-8B embeddings
+ lightweight trainable score heads.
"""

__version__ = "1.0.0"
__author__ = "clmforge contributors"

from .config import CLMConfig, load_config
from .types import Action, Decision, DecisionResult, ScoreResult
from .engine.decision_engine import DecisionEngine
from .engine.router import Router
from .models.clm_model import CLMModel

__all__ = [
    "__version__",
    "CLMConfig",
    "load_config",
    "Action",
    "Decision",
    "DecisionResult",
    "ScoreResult",
    "DecisionEngine",
    "Router",
    "CLMModel",
]
