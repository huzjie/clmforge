# -*- coding: utf-8 -*-
"""Example: HTTP server end-to-end."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import threading

from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router
from clmforge.serving.server import run_server
from clmforge.serving.client import CLMClient


def main():
    model = CLMModel()
    engine = DecisionEngine(model)
    router = Router(engine, mode="always_fast")

    t = threading.Thread(target=run_server, args=(router, "127.0.0.1", 8765, "secret"),
                         daemon=True)
    t.start()
    import time
    time.sleep(0.5)

    client = CLMClient(base_url="http://127.0.0.1:8765", token="secret")
    print("health:", client.health())
    print("decide:", client.decide("what is the weather?", ["search", "calc", "mail"]))
    print("stats:", client.stats())


if __name__ == "__main__":
    main()
