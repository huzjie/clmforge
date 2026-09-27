# -*- coding: utf-8 -*-
"""Backend factory."""
from __future__ import annotations

from .. import constants as C
from ..exceptions import BackendError
from .mock import MockBackend
from .frozen import FrozenEmbeddingsBackend


def make_backend(kind: str, **kwargs):
    if kind in (C.BACKEND_MOCK, "mock"):
        return MockBackend(
            embed_dim=kwargs.get("embed_dim", C.DEFAULT_EMBED_DIM),
            skill=kwargs.get("skill", 0.5),
            noise=kwargs.get("noise", 0.4),
        )
    if kind in (C.BACKEND_FROZEN, "frozen"):
        return FrozenEmbeddingsBackend(kwargs.get("embed_dim", C.DEFAULT_EMBED_DIM))
    if kind in (C.BACKEND_OPENAI, "openai"):
        from .openai import OpenAICompatibleBackend
        return OpenAICompatibleBackend(
            base_url=kwargs.get("base_url"),
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model"),
        )
    if kind in (C.BACKEND_VLLM, "vllm"):
        from .vllm import VLLMBackend
        return VLLMBackend(base_url=kwargs.get("base_url"), model=kwargs.get("model"))
    if kind in (C.BACKEND_TRANSFORMERS, "transformers"):
        from .transformers import TransformersBackend
        return TransformersBackend(model_name=kwargs.get("model", "Qwen/Qwen3-8B"))
    raise BackendError(f"unknown backend kind {kind!r}")
