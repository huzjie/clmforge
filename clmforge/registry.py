# -*- coding: utf-8 -*-
"""A tiny generic registry."""
from __future__ import annotations

from typing import Any, Callable, Dict, Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self, name: str = "registry"):
        self.name = name
        self._items: Dict[str, T] = {}

    def register(self, key: str, obj: T) -> T:
        self._items[key] = obj
        return obj

    def get(self, key: str) -> T:
        if key not in self._items:
            raise KeyError(f"{self.name}: unknown key {key!r} (have {sorted(self._items)})")
        return self._items[key]

    def has(self, key: str) -> bool:
        return key in self._items

    def keys(self):
        return list(self._items.keys())

    def decorator(self, key: str) -> Callable:
        def wrap(obj: T) -> T:
            self.register(key, obj)
            return obj
        return wrap
