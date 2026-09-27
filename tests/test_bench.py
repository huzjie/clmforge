# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.backends.mock import MockBackend
from clmforge.bench import bfcl, ranking, verification, gaming, wikiracing


class TestBench(unittest.TestCase):
    def setUp(self):
        model = CLMModel(embed_dim=16, skill=0.8)
        engine = DecisionEngine(model)
        self.router = Router(engine, mode="always_fast", slow_backend=MockBackend(skill=0.9))

    def test_all_benchmarks_run(self):
        for b in [bfcl, ranking, verification, gaming, wikiracing]:
            bench = b.build(self.router, n=20)
            res = bench.run()
            self.assertGreaterEqual(res.accuracy, 0.0)
            self.assertLessEqual(res.accuracy, 1.0)
            self.assertEqual(res.total, 20)


if __name__ == "__main__":
    unittest.main()
