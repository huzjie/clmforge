# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.config import load_config, CLMConfig
from clmforge.utils.yamlish import parse


class TestYamlish(unittest.TestCase):
    def test_scalars(self):
        d = parse("a: 1\nb: true\nc: hello\nd: 3.14\ne: [1, 2, 3]")
        self.assertEqual(d["a"], 1)
        self.assertIs(d["b"], True)
        self.assertEqual(d["c"], "hello")
        self.assertAlmostEqual(d["d"], 3.14)
        self.assertEqual(d["e"], [1, 2, 3])

    def test_nested(self):
        d = parse("model:\n  embed_dim: 128\n  head_type: mlp\nrouter:\n  mode: margin")
        self.assertEqual(d["model"]["embed_dim"], 128)
        self.assertEqual(d["model"]["head_type"], "mlp")
        self.assertEqual(d["router"]["mode"], "margin")

    def test_block_list(self):
        d = parse("keywords:\n  - alpha\n  - beta\n")
        self.assertIn("alpha", d["keywords"])


class TestConfig(unittest.TestCase):
    def test_default(self):
        cfg = load_config(None)
        self.assertIsInstance(cfg, CLMConfig)
        self.assertEqual(cfg.model.head_type, "bilinear")

    def test_override(self):
        cfg = load_config(None, {"model": {"embed_dim": 32}, "top_k": 3})
        self.assertEqual(cfg.model.embed_dim, 32)
        self.assertEqual(cfg.top_k, 3)


if __name__ == "__main__":
    unittest.main()
