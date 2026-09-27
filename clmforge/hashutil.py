# -*- coding: utf-8 -*-
"""Deterministic hashing helpers (cross-run reproducible, no PYTHONHASHSEED)."""
import hashlib
import random
import struct


def md5(text: str) -> str:
    """Return the hex MD5 digest of *text* (UTF-8)."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def stable_float(key: str, lo: float = 0.0, hi: float = 1.0) -> float:
    """Map a string key deterministically into [lo, hi]."""
    digest = hashlib.md5(key.encode("utf-8")).digest()
    unit = struct.unpack("<Q", digest[:8])[0] / float(0xFFFFFFFFFFFFFFFF)
    return lo + (hi - lo) * unit


def _seed_of(key: str) -> int:
    return struct.unpack("<Q", hashlib.md5(key.encode("utf-8")).digest()[:8])[0]


def stable_ints(key: str, n: int, lo: int, hi: int) -> list:
    """Return *n* deterministic integers in [lo, hi] derived from *key*.

    Uses a Mersenne-Twister PRNG seeded by the MD5 digest — deterministic across
    runs and platforms (unlike ``hash()``), and fast (unlike per-index MD5).
    """
    rng = random.Random(_seed_of(key))
    return [lo + rng.randint(0, hi - lo) for _ in range(n)]


def stable_vector(key: str, dim: int, scale: float = 1.0) -> list:
    """Return a deterministic pseudo-random float vector of length *dim*."""
    rng = random.Random(_seed_of(key))
    return [(rng.random() * 2.0 - 1.0) * scale for _ in range(dim)]
