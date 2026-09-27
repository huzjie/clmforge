# -*- coding: utf-8 -*-
"""Example: tool routing with a real tool registry."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.types import Action, Decision

TOOLS = {
    "search_web": lambda q: f"searched: {q}",
    "calc": lambda expr: f"calc: {expr}",
    "send_email": lambda to: f"emailed {to}",
    "read_file": lambda p: f"read {p}",
    "query_db": lambda sql: f"queried: {sql}",
}


def main():
    model = CLMModel()
    engine = DecisionEngine(model)
    actions = [Action(k, k, "") for k in TOOLS]

    # 同一组工具跨请求复用 -> 动作嵌入命中缓存
    requests = [
        "what is the weather today",
        "2 + 3",
        "send mail to alice",
        "select * from users",
        "read the config file",
    ]
    for state in requests:
        res = engine.decide(Decision(state=state, actions=actions))
        fn = TOOLS[res.selected]
        print(f"{state!r} -> {res.selected:<12} | {fn(state)}")

    print("cache stats:", model.action_cache.stats())


if __name__ == "__main__":
    main()
