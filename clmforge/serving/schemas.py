# -*- coding: utf-8 -*-
"""Request/response schemas for the HTTP API (plain dicts)."""


def decision_request(state, actions):
    return {"state": state, "actions": [a.to_text() for a in actions],
            "keys": [a.key for a in actions]}


def decision_response(result):
    return {
        "selected": result.selected,
        "confidence": result.confidence,
        "path": result.path,
        "latency_ms": result.latency_ms,
        "cache_hits": result.cache_hits,
        "ranking": result.ranking(),
    }
