# -*- coding: utf-8 -*-
"""clmforge exception hierarchy."""


class CLMError(Exception):
    """Base class for all clmforge errors."""


class ConfigError(CLMError):
    """Invalid or missing configuration."""


class BackendError(CLMError):
    """A backend failed to produce embeddings or scores."""


class EmbeddingError(CLMError):
    """Embedding computation failed."""


class ScoringError(CLMError):
    """Scoring pipeline failed."""


class CacheError(CLMError):
    """Action-cache operations failed."""


class TrainingError(CLMError):
    """Training loop failed."""


class RouterError(CLMError):
    """Fast/slow routing failed."""
