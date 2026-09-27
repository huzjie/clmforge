# -*- coding: utf-8 -*-
"""A minimal YAML-subset parser (no external dependency).

Supports nested mappings via indentation, inline lists, inline scalars,
line-end comments, and block lists (lines starting with ``- ``).
"""
from __future__ import annotations

from typing import Any, List


def _strip_comment(line: str) -> str:
    for i, ch in enumerate(line):
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def _parse_scalar(token: str) -> Any:
    token = token.strip()
    if token == "":
        return ""
    if token.startswith('"') and token.endswith('"') and len(token) >= 2:
        return token[1:-1]
    if token.startswith("'") and token.endswith("'") and len(token) >= 2:
        return token[1:-1]
    low = token.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "none", "~"):
        return None
    try:
        if token.startswith("0x") or token.startswith("0X"):
            return int(token, 16)
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    return token


def _split_inline_list(text: str) -> List[str]:
    out: List[str] = []
    depth = 0
    quote = None
    cur = []
    for ch in text:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            cur.append(ch)
        elif ch in "[({":
            depth += 1
            cur.append(ch)
        elif ch in "])}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur))
    return out


def _parse_inline(token: str) -> Any:
    token = token.strip()
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        if not inner:
            return []
        return [_parse_inline(t) for t in _split_inline_list(inner)]
    if token.startswith("{") and token.endswith("}"):
        inner = token[1:-1].strip()
        result = {}
        for part in _split_inline_list(inner):
            if ":" in part:
                k, v = part.split(":", 1)
                result[_parse_scalar(k)] = _parse_inline(v)
        return result
    return _parse_scalar(token)


def parse(text: str) -> dict:
    """Parse a YAML-subset string into nested dicts/lists."""
    root: dict = {}
    # stack entries: [indent, container, parent, key_in_parent]
    stack: List[list] = [[-1, root, None, None]]

    for raw in text.splitlines():
        s = raw.rstrip()
        if not s.strip():
            continue
        if _strip_comment(s).strip() == "":
            continue
        indent = len(s) - len(s.lstrip())
        line = _strip_comment(s).strip()

        # pop back to enclosing level (same indent -> sibling, pop)
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        top = stack[-1]
        container = top[1]

        if line.startswith("- "):
            item = line[2:].strip()
            val = _parse_inline(item)
            if isinstance(container, list):
                container.append(val)
            else:
                parent, key = top[2], top[3]
                if key is not None:
                    existing = parent.get(key)
                    if isinstance(existing, list):
                        existing.append(val)
                    else:
                        lst = [val]
                        parent[key] = lst
                        top[1] = lst  # subsequent items append here
                else:
                    parent.setdefault("_items", []).append(val)
            continue

        if ":" in line:
            k, v = line.split(":", 1)
            key = _parse_scalar(k)
            val_raw = v.strip()
            if val_raw == "":
                child: dict = {}
                container[key] = child
                stack.append([indent, child, container, key])
            else:
                container[key] = _parse_inline(val_raw)
        else:
            container[line] = None

    return root
