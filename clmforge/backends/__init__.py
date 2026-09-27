# -*- coding: utf-8 -*-
"""Model backends.  A backend exposes ``encode_state``/``encode_actions`` or a
full generative fallback for the slow path."""
from .factory import make_backend
from .base import BaseBackend

__all__ = ["make_backend", "BaseBackend"]
