# -*- coding: utf-8 -*-
"""Action embedding cache — the core latency win of CLM.

Action embeddings are computed once and reused across many decisions.  When an
action set repeats (or shares members) with a previous request, the cache
avoids re-encoding, which is where the 1.6x-9x speedups come from.
"""
from __future__ import annotations

import json
import threading
from typing import Dict, List, Optional, Tuple

from ..types import Action
from .action_encoder import ActionEncoder


class ActionCache:
    def __init__(self, encoder: ActionEncoder, max_entries: int = 65536,
                 persist: bool = False, path: str = ".clmforge_cache.json"):
        self.encoder = encoder
        self.max_entries = max_entries
        self.persist = persist
        self.path = path
        self._store: Dict[str, List[float]] = {}
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0
        if persist:
            self._load()

    def _cache_key(self, action: Action) -> str:
        return action.to_text()

    def encode_all(self, actions: List[Action]) -> Tuple[List[List[float]], int]:
        """Return (embeddings, cache_hits) for the action list."""
        vecs = []
        hits = 0
        with self._lock:
            for a in actions:
                key = self._cache_key(a)
                if key in self._store:
                    vecs.append(self._store[key])
                    hits += 1
                    self._hits += 1
                else:
                    vec = self.encoder.encode(a)
                    self._store[key] = vec
                    vecs.append(vec)
                    self._misses += 1
        self._evict()
        if self.persist:
            self._save()
        return vecs, hits

    def _evict(self) -> None:
        if len(self._store) <= self.max_entries:
            return
        overflow = len(self._store) - self.max_entries
        # simple FIFO eviction over insertion order (dict preserves order)
        for key in list(self._store.keys())[:overflow]:
            del self._store[key]

    def stats(self) -> dict:
        return {
            "entries": len(self._store),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self._hits / max(1, self._hits + self._misses),
        }

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def _save(self) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._store, f)
        except OSError:
            pass

    def _load(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self._store = json.load(f)
        except (OSError, ValueError):
            self._store = {}
