# -*- coding: utf-8 -*-
"""Contrastive training for the score head."""
from .trainer import Trainer
from .contrastive_loss import infonce_loss, margin_loss
from .data import ContrastiveDataset, Example

__all__ = ["Trainer", "infonce_loss", "margin_loss", "ContrastiveDataset", "Example"]
