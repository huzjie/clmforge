# -*- coding: utf-8 -*-
"""vLLM backend (OpenAI-compatible serving endpoint)."""
from __future__ import annotations

from .. import constants as C
from .openai import OpenAICompatibleBackend


class VLLMBackend(OpenAICompatibleBackend):
    kind = C.BACKEND_VLLM

    def __init__(self, base_url: str = None, model: str = None):
        super().__init__(base_url=base_url or "http://localhost:8000/v1",
                         api_key="EMPTY", model=model or "Qwen/Qwen3-8B")
