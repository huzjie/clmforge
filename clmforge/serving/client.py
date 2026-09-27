# -*- coding: utf-8 -*-
"""Stdlib HTTP client for the clmforge server."""
from __future__ import annotations

import json
import urllib.request
from typing import List


class CLMClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765", token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def health(self) -> dict:
        return self._get("/health")

    def decide(self, state: str, keys: List[str]) -> dict:
        return self._post("/decide", {"state": state, "keys": keys})

    def stats(self) -> dict:
        return self._get("/stats")

    def _get(self, path: str) -> dict:
        req = urllib.request.Request(self.base_url + path)
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))

    def _post(self, path: str, payload: dict) -> dict:
        req = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
