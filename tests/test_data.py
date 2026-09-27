# -*- coding: utf-8 -*-
import unittest

from clmforge.data.generators import tool_choice_data, ranking_data
from clmforge.data.dataset import DatasetBuilder
from clmforge.data.sampling import deterministic_split
from clmforge.types import Action


class TestData(unittest.TestCase):
    def test_tool_choice_data(self):
        decisions, correct_map = tool_choice_data(10)
        self.assertEqual(len(decisions), 10)
        self.assertEqual(len(correct_map), 10)

    def test_dataset_builder(self):
        b = DatasetBuilder().add("s", [Action("a", "a"), Action("b", "b")], "a")
        ds = b.build()
        self.assertEqual(len(ds), 1)

    def test_split(self):
        mask = deterministic_split(100, 0.8)
        self.assertEqual(len(mask), 100)
        self.assertEqual(set(mask), {0, 1})


if __name__ == "__main__":
    unittest.main()
