# -*- coding: utf-8 -*-
"""HuggingFace Transformers backend (slow path).  Lazy-imports torch+transformers."""
from __future__ import annotations

from typing import List

from .. import constants as C
from ..types import Action
from .base import BaseBackend


class TransformersBackend(BaseBackend):
    kind = C.BACKEND_TRANSFORMERS

    def __init__(self, model_name: str = "Qwen/Qwen3-8B"):
        self.model_name = model_name
        self._pipe = None

    def _load(self):
        if self._pipe is None:
            from transformers import pipeline  # type: ignore
            self._pipe = pipeline("text-generation", model=self.model_name, max_new_tokens=16)
        return self._pipe

    def encode_state(self, state: str) -> List[float]:
        return []

    def encode_actions(self, actions: List[Action]) -> List[List[float]]:
        return []

    def generate(self, state: str, actions: List[Action]) -> str:
        pipe = self._load()
        options = " ".join(a.label() for a in actions)
        out = pipe(f"State: {state}\nChoose one action: {options}")[0]["generated_text"]
        for a in actions:
            if a.label() in out:
                return a.key
        return actions[0].key if actions else ""
