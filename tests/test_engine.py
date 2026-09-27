# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.engine.confidence import confidence_margin
from clmforge.backends.mock import MockBackend, world_answer
from clmforge.types import Action, Decision


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.model = CLMModel(embed_dim=16)
        self.engine = DecisionEngine(self.model)
        self.actions = [Action(f"a{i}", f"a{i}") for i in range(5)]

    def test_decide_returns_selected(self):
        res = self.engine.decide(Decision(state="s", actions=self.actions))
        self.assertIn(res.selected, [a.key for a in self.actions])
        self.assertEqual(len(res.scores), 5)

    def test_world_answer_deterministic(self):
        self.assertEqual(world_answer("x", self.actions), world_answer("x", self.actions))

    def test_router_always_fast(self):
        r = Router(self.engine, mode="always_fast")
        res = r.route(Decision(state="s", actions=self.actions))
        self.assertEqual(res.path, "fast")

    def test_router_margin_slow_fallback(self):
        slow = MockBackend(skill=0.9)
        r = Router(self.engine, mode="margin", margin_threshold=1.0, slow_backend=slow)
        res = r.route(Decision(state="s", actions=self.actions))
        self.assertEqual(res.path, "slow")


class TestConfidence(unittest.TestCase):
    def test_margin(self):
        self.assertAlmostEqual(confidence_margin([1.0, 0.0]), 1.0, places=5)
        self.assertAlmostEqual(confidence_margin([0.5, 0.5]), 0.0, places=5)
        self.assertEqual(confidence_margin([]), 0.0)


if __name__ == "__main__":
    unittest.main()
