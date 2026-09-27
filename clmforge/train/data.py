# -*- coding: utf-8 -*-
"""Contrastive dataset primitives."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..types import Action


@dataclass
class Example:
    state: str
    actions: List[Action]
    correct_key: str


@dataclass
class ContrastiveDataset:
    examples: List[Example] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, i: int) -> Example:
        return self.examples[i]

    def positive_index(self, example: Example) -> int:
        for i, a in enumerate(example.actions):
            if a.key == example.correct_key:
                return i
        return 0

    @classmethod
    def from_pairs(cls, state_action_pairs: List[tuple]) -> "ContrastiveDataset":
        """state_action_pairs: [(state, [(action_text, key, is_correct), ...]), ...]"""
        ds = cls()
        for state, entries in state_action_pairs:
            actions = [Action(key=k, name=t) for t, k, _ in entries]
            correct = next(k for t, k, ok in entries if ok)
            ds.examples.append(Example(state=state, actions=actions, correct_key=correct))
        return ds
