# -*- coding: utf-8 -*-
"""JSON serialization helpers for dataclass-heavy payloads."""
import json
from dataclasses import asdict, is_dataclass
from typing import Any


def _convert(obj: Any) -> Any:
    if is_dataclass(obj):
        return {k: _convert(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _convert(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_convert(v) for v in obj]
    return obj


def to_json(obj: Any, pretty: bool = False) -> str:
    kwargs = {"ensure_ascii": False}
    if pretty:
        kwargs["indent"] = 2
    return json.dumps(_convert(obj), **kwargs)


def from_json(text: str) -> Any:
    return json.loads(text)
