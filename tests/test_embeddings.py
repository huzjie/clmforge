# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from clmforge.embeddings import hash_embed, normalize, cosine, dot
from clmforge.hashutil import stable_float, stable_vector


class TestEmbeddings(unittest.TestCase):
    def test_deterministic(self):
        a = hash_embed("hello", 32)
        b = hash_embed("hello", 32)
        self.assertEqual(a, b)

    def test_dim(self):
        self.assertEqual(len(hash_embed("x", 64)), 64)

    def test_normalize_unit(self):
        v = normalize([3.0, 4.0])
        self.assertAlmostEqual(sum(x * x for x in v), 1.0, places=6)

    def test_cosine_same(self):
        v = hash_embed("abc", 32)
        self.assertAlmostEqual(cosine(v, v), 1.0, places=5)

    def test_stable_float_range(self):
        for key in ["a", "b", "c", "d"]:
            v = stable_float(key, -1.0, 1.0)
            self.assertTrue(-1.0 <= v <= 1.0)


if __name__ == "__main__":
    unittest.main()
