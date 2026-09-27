# -*- coding: utf-8 -*-
"""Configuration loading with a built-in zero-dependency YAML fallback."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional

from .exceptions import ConfigError
from . import constants as C


def _merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


@dataclass
class ModelConfig:
    embed_dim: int = C.DEFAULT_EMBED_DIM
    head_type: str = C.HEAD_BILINEAR
    normalize: bool = True
    temperature: float = C.DEFAULT_TEMPERATURE
    backbone: str = "frozen"
    max_actions: int = C.DEFAULT_MAX_ACTIONS


@dataclass
class RouterConfig:
    mode: str = C.ROUTER_MARGIN
    margin_threshold: float = C.DEFAULT_CONFIDENCE_THRESHOLD
    slow_backend: str = C.BACKEND_MOCK


@dataclass
class CacheConfig:
    enabled: bool = True
    max_entries: int = C.DEFAULT_CACHE_SIZE
    persist: bool = False
    path: str = ".clmforge_cache.json"


@dataclass
class TrainConfig:
    epochs: int = 10
    batch_size: int = 32
    lr: float = 1e-3
    negatives_per_positive: int = 8
    loss: str = "infonce"
    temperature: float = 0.07


@dataclass
class CLMConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    router: RouterConfig = field(default_factory=RouterConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    backend: str = C.BACKEND_MOCK
    backend_kwargs: Dict[str, Any] = field(default_factory=dict)
    top_k: int = C.DEFAULT_TOP_K

    def to_dict(self) -> dict:
        return asdict(self)

    def save_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


def load_config(path: Optional[str] = None, overrides: Optional[dict] = None) -> CLMConfig:
    """Load a CLMConfig from YAML/JSON; falls back to defaults when absent."""
    data: Dict[str, Any] = {}
    if path and os.path.exists(path):
        text = open(path, "r", encoding="utf-8").read()
        if path.endswith(".json"):
            data = json.loads(text)
        else:
            from .utils.yamlish import parse as _yaml_parse
            data = _yaml_parse(text) or {}
    if overrides:
        data = _merge(data, overrides)

    cfg = CLMConfig()
    if not data:
        return cfg

    if "model" in data:
        cfg.model = ModelConfig(**_pick(ModelConfig, data["model"]))
    if "router" in data:
        cfg.router = RouterConfig(**_pick(RouterConfig, data["router"]))
    if "cache" in data:
        cfg.cache = CacheConfig(**_pick(CacheConfig, data["cache"]))
    if "train" in data:
        cfg.train = TrainConfig(**_pick(TrainConfig, data["train"]))
    for k in ("backend", "backend_kwargs", "top_k"):
        if k in data:
            setattr(cfg, k, data[k])
    return cfg


def _pick(cls, mapping: dict) -> dict:
    names = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
    return {k: v for k, v in mapping.items() if k in names}
