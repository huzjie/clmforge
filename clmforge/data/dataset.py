# -*- coding: utf-8 -*-
"""DatasetBuilder: assemble contrastive training examples."""
from __future__ import annotations

from typing import List

from ..train.data import ContrastiveDataset, Example
from ..types import Action


class DatasetBuilder:
    def __init__(self):
        self._examples: List[Example] = []

    def add(self, state: str, actions: List[Action], correct_key: str) -> "DatasetBuilder":
        self._examples.append(Example(state=state, actions=actions, correct_key=correct_key))
        return self

    def build(self) -> ContrastiveDataset:
        ds = ContrastiveDataset()
        ds.examples = list(self._examples)
        return ds
