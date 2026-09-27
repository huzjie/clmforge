# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from clmforge.backends.factory import make_backend
from clmforge.backends.mock import world_answer
from clmforge.types import Action


class TestBackends(unittest.TestCase):
    def test_mock_factory(self):
        b = make_backend("mock", embed_dim=16)
        self.assertEqual(b.kind, "mock")
        self.assertTrue(b.supports_training)

    def test_mock_generate_in_set(self):
        b = make_backend("mock")
        actions = [Action("a", "a"), Action("b", "b")]
        self.assertIn(b.generate("state", actions), ["a", "b"])

    def test_unknown_backend(self):
        from clmforge.exceptions import BackendError
        with self.assertRaises(BackendError):
            make_backend("nope")


if __name__ == "__main__":
    unittest.main()
