# -*- coding: utf-8 -*-
"""Trainer: fits the score head on contrastive (state, action) pairs."""
from __future__ import annotations

from typing import List, Optional

from ..models.clm_model import CLMModel
from .data import ContrastiveDataset
from .contrastive_loss import infonce_loss, margin_loss


class Trainer:
    def __init__(self, model: CLMModel, loss: str = "infonce",
                 temperature: float = 0.07, lr: float = 0.05):
        self.model = model
        self.loss = loss
        self.temperature = temperature
        self.lr = lr
        self.history: List[dict] = []

    def step(self, dataset: ContrastiveDataset, i: int) -> float:
        ex = dataset[i]
        scores, _ = self.model.score(ex.state, ex.actions)
        pos = dataset.positive_index(ex)
        if self.loss == "margin":
            loss_val = margin_loss(scores, pos)
        else:
            loss_val = infonce_loss(scores, pos, self.temperature)
        correct = ex.actions[pos].key
        best = max(range(len(ex.actions)), key=lambda j: scores[j])
        correct_wins = ex.actions[best].key == correct
        # The learnable "skill" climbs toward 1.0; take a bigger step when the
        # model still gets it wrong (more room to improve).  In the zero-dep
        # mock this is the entire "gradient"; a real head would backprop here.
        delta = 1.0 if not correct_wins else 0.5
        self.model.train_step(delta, self.lr)
        self.history.append({"step": i, "loss": loss_val, "delta": delta,
                             "correct": correct_wins})
        return loss_val

    def fit(self, dataset: ContrastiveDataset, epochs: int = 10) -> List[dict]:
        for epoch in range(epochs):
            for i in range(len(dataset)):
                self.step(dataset, i)
        return self.history
