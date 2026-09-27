# -*- coding: utf-8 -*-
import unittest

from clmforge.models.clm_model import CLMModel
from clmforge.integrations.mcp import MCPToolRouter
from clmforge.integrations.function_calling import route_functions
from clmforge.integrations.retrieval_rerank import rerank


class TestIntegrations(unittest.TestCase):
    def test_mcp_router(self):
        r = MCPToolRouter(CLMModel(embed_dim=16))
        tools = [{"name": "calc", "description": "arithmetic"},
                 {"name": "search", "description": "web search"}]
        self.assertIn(r.route("2+3", tools), ["calc", "search"])

    def test_function_calling(self):
        model = CLMModel(embed_dim=16)
        fns = [{"name": "calc", "description": "arithmetic"},
               {"name": "search", "description": "web search"}]
        self.assertIn(route_functions(model, "2+3", fns), ["calc", "search"])

    def test_rerank(self):
        model = CLMModel(embed_dim=16)
        docs = ["a", "b", "c", "d"]
        out = rerank(model, "q", docs, top_n=2)
        self.assertEqual(len(out), 2)


if __name__ == "__main__":
    unittest.main()
