# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from clmforge.models.clm_model import CLMModel
from clmforge.train.data import ContrastiveDataset, Example
from clmforge.train.trainer import Trainer
from clmforge.train.contrastive_loss import infonce_loss, margin_loss
from clmforge.types import Action


class TestTrain(unittest.TestCase):
    def test_losses(self):
        self.assertLess(infonce_loss([1.0, 0.0], 0), infonce_loss([0.5, 0.5], 0))
        self.assertAlmostEqual(margin_loss([1.0, 0.0], 0), 0.0)

    def test_trainer_improves(self):
        model = CLMModel(embed_dim=16, skill=0.3)
        actions = [Action(f"a{i}", f"a{i}") for i in range(4)]
        ds = ContrastiveDataset()
        for i in range(40):
            ds.examples.append(Example(state=f"s{i}", actions=actions, correct_key=f"a{i % 4}"))
        before = model.head.skill
        Trainer(model).fit(ds, epochs=3)
        self.assertGreaterEqual(model.head.skill, before)


if __name__ == "__main__":
    unittest.main()
