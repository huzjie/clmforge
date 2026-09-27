# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from clmforge.models.clm_model import CLMModel
from clmforge.types import Action


class TestCLMModel(unittest.TestCase):
    def setUp(self):
        self.model = CLMModel(embed_dim=16)
        self.actions = [Action("a", "alpha"), Action("b", "beta"), Action("c", "gamma")]

    def test_score_shape(self):
        scores, hits = self.model.score("state", self.actions)
        self.assertEqual(len(scores), 3)
        self.assertEqual(hits, 0)

    def test_cache_hit(self):
        self.model.score("s", self.actions)
        _, hits = self.model.score("s", self.actions)
        self.assertEqual(hits, 3)

    def test_train_step_bounds(self):
        for _ in range(50):
            self.model.train_step(1.0)
        self.assertLessEqual(self.model.head.skill, 1.0)
        for _ in range(100):
            self.model.train_step(-1.0)
        self.assertGreaterEqual(self.model.head.skill, 0.0)


if __name__ == "__main__":
    unittest.main()
