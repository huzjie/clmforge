# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from clmforge.scoring import make_head
from clmforge import constants as C


class TestScoring(unittest.TestCase):
    def test_linear(self):
        h = make_head(C.HEAD_LINEAR, 4, weight=[1, 1, 1, 1])
        s = h.score([1, 2, 3, 4], [1, 1, 1, 1])
        self.assertAlmostEqual(s, 10.0)

    def test_bilinear_identity(self):
        h = make_head(C.HEAD_BILINEAR, 4)
        s = h.score([1, 2, 3, 4], [1, 2, 3, 4])
        self.assertAlmostEqual(s, 30.0)

    def test_mlp(self):
        h = make_head(C.HEAD_MLP, 8, hidden=16)
        s = h.score([1.0] * 8, [1.0] * 8)
        self.assertIsInstance(s, float)


if __name__ == "__main__":
    unittest.main()
