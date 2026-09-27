# -*- coding: utf-8 -*-
"""Text preprocessing helpers for state/action strings."""
from __future__ import annotations

import re

_WS = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Collapse whitespace and strip."""
    return _WS.sub(" ", text).strip()


def truncate(text: str, max_len: int = 512) -> str:
    return text if len(text) <= max_len else text[: max_len - 3] + "..."
