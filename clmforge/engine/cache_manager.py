# -*- coding: utf-8 -*-
"""Convenience wrapper exposing action-cache statistics."""
from __future__ import annotations

from ..models.action_cache import ActionCache


class CacheManager:
    def __init__(self, cache: ActionCache):
        self.cache = cache

    def stats(self) -> dict:
        return self.cache.stats()

    def warm(self, actions) -> None:
        self.cache.encode_all(actions)

    def clear(self) -> None:
        self.cache.clear()
