# -*- coding: utf-8 -*-
"""Simple decision tracer that logs each decision."""
from __future__ import annotations

import json
import time


class Tracer:
    def __init__(self, path: str = "decisions.jsonl"):
        self.path = path
        self._f = open(path, "a", encoding="utf-8")

    def trace(self, decision, result) -> None:
        rec = {
            "ts": time.time(),
            "state": decision.state,
            "selected": result.selected,
            "path": result.path,
            "confidence": result.confidence,
            "latency_ms": result.latency_ms,
        }
        self._f.write(json.dumps(rec) + "\n")
        self._f.flush()

    def close(self) -> None:
        self._f.close()
