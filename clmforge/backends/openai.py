# -*- coding: utf-8 -*-
"""OpenAI-compatible backend for the slow (generative) path."""
from __future__ import annotations

import json
import os
import urllib.request
from typing import List

from .. import constants as C
from ..types import Action
from .base import BaseBackend


class OpenAICompatibleBackend(BaseBackend):
    kind = C.BACKEND_OPENAI

    def __init__(self, base_url: str = None, api_key: str = None, model: str = None):
        self.base_url = (base_url or os.environ.get("CLM_OPENAI_BASE_URL")
                         or "https://api.openai.com/v1")
        self.api_key = api_key or os.environ.get("CLM_OPENAI_API_KEY", "")
        self.model = model or os.environ.get("CLM_OPENAI_MODEL", "gpt-4o-mini")

    def encode_state(self, state: str) -> List[float]:
        return []

    def encode_actions(self, actions: List[Action]) -> List[List[float]]:
        return []

    def generate(self, state: str, actions: List[Action]) -> str:
        options = "\n".join(f"{i+1}. {a.to_text()}" for i, a in enumerate(actions))
        prompt = (f"Choose the best action for the following state. "
                  f"Reply with only the number.\nState: {state}\nOptions:\n{options}")
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        answer = data["choices"][0]["message"]["content"].strip()
        # extract first integer
        for tok in answer.replace(",", " ").split():
            try:
                idx = int(tok) - 1
                if 0 <= idx < len(actions):
                    return actions[idx].key
            except ValueError:
                continue
        return actions[0].key if actions else ""
