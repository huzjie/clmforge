# -*- coding: utf-8 -*-
import unittest

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.serving.schemas import decision_request, decision_response
from clmforge.types import Action, Decision


class TestServing(unittest.TestCase):
    def test_schemas(self):
        model = CLMModel(embed_dim=16)
        engine = DecisionEngine(model)
        router = Router(engine, mode="always_fast")
        actions = [Action("a", "a"), Action("b", "b")]
        res = router.route(Decision(state="s", actions=actions))
        resp = decision_response(res)
        self.assertIn(resp["selected"], ["a", "b"])
        self.assertEqual(resp["path"], "fast")


if __name__ == "__main__":
    unittest.main()
