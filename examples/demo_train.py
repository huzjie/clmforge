# -*- coding: utf-8 -*-
"""Example: training improves accuracy."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.backends.mock import MockBackend, world_answer
from clmforge.types import Action, Decision
from clmforge.train.data import ContrastiveDataset, Example
from clmforge.train.trainer import Trainer


def main():
    model = CLMModel(skill=0.3)
    engine = DecisionEngine(model)
    slow = MockBackend(skill=0.9)
    router = Router(engine, mode="always_fast", slow_backend=slow)

    actions = [Action(f"a{i}", f"action_{i}") for i in range(8)]
    states = [f"task-{i}" for i in range(120)]

    def accuracy():
        correct = 0
        for s in states:
            res = engine.decide(Decision(state=s, actions=actions))
            if res.selected == world_answer(s, actions):
                correct += 1
        return correct / len(states)

    print(f"accuracy before training: {accuracy():.3f}")

    ds = ContrastiveDataset()
    for s in states:
        ds.examples.append(Example(state=s, actions=actions, correct_key=world_answer(s, actions)))
    Trainer(model, loss="infonce", lr=0.05).fit(ds, epochs=8)

    print(f"accuracy after training:  {accuracy():.3f}")
    print(f"skill: {model.head.skill:.3f}")


if __name__ == "__main__":
    main()
