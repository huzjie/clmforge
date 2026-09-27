# -*- coding: utf-8 -*-
"""Tiny logging facade (stdlib only)."""
import logging
import sys

_LOGGERS = {}


def get_logger(name: str = "clmforge") -> logging.Logger:
    if name in _LOGGERS:
        return _LOGGERS[name]
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        ))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    _LOGGERS[name] = logger
    return logger
