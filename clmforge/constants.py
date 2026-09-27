# -*- coding: utf-8 -*-
"""Shared constants for clmforge."""

DEFAULT_EMBED_DIM = 64
DEFAULT_MAX_ACTIONS = 512
DEFAULT_TOP_K = 1
DEFAULT_TEMPERATURE = 1.0
DEFAULT_CONFIDENCE_THRESHOLD = 0.20
DEFAULT_CACHE_SIZE = 65536

# Score-head types
HEAD_LINEAR = "linear"
HEAD_BILINEAR = "bilinear"
HEAD_MLP = "mlp"

# Backend kinds
BACKEND_MOCK = "mock"
BACKEND_OPENAI = "openai"
BACKEND_VLLM = "vllm"
BACKEND_TRANSFORMERS = "transformers"
BACKEND_FROZEN = "frozen"

# Router modes
ROUTER_ALWAYS_FAST = "always_fast"
ROUTER_ALWAYS_SLOW = "always_slow"
ROUTER_MARGIN = "margin"

# Benchmark task kinds
TASK_TOOL_CALLING = "tool_calling"
TASK_RANKING = "ranking"
TASK_VERIFICATION = "verification"
TASK_GAMING = "gaming"
TASK_WIKIRACING = "wikiracing"

# Latency labels
FAST_PATH = "fast"
SLOW_PATH = "slow"
