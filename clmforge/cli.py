# -*- coding: utf-8 -*-
"""Command-line interface: doctor / train / bench / decide / serve / speedup."""
from __future__ import annotations

import argparse
import sys

from . import __version__


def _build_router(args, mode=None, skill=None):
    from .config import load_config
    from .models.clm_model import CLMModel
    from .engine.decision_engine import DecisionEngine
    from .engine.router import Router
    from .backends.factory import make_backend

    cfg = load_config(args.config)
    model = CLMModel(
        embed_dim=cfg.model.embed_dim,
        head_type=cfg.model.head_type,
        normalize=cfg.model.normalize,
        cache_max=cfg.cache.max_entries,
        cache_persist=cfg.cache.persist,
        cache_path=cfg.cache.path,
        skill=0.5 if skill is None else skill,
    )
    engine = DecisionEngine(model, top_k=cfg.top_k)
    slow = make_backend(cfg.router.slow_backend, **cfg.backend_kwargs)
    router_mode = mode if mode is not None else cfg.router.mode
    return Router(engine, mode=router_mode,
                  margin_threshold=cfg.router.margin_threshold, slow_backend=slow), model


def cmd_doctor(args) -> int:
    from .models.clm_model import CLMModel
    from .embeddings import available_backends
    m = CLMModel()
    from .types import Action, Decision
    actions = [Action(key="a", name="alpha"), Action(key="b", name="beta")]
    res = None
    from .engine.decision_engine import DecisionEngine
    res = DecisionEngine(m).decide(Decision(state="doctor-check", actions=actions))
    print(f"clmforge v{__version__} OK", flush=True)
    print(f"  embed_dim={m.embed_dim} head={m.head.head.kind} "
          f"embed_backends={available_backends()}", flush=True)
    print(f"  smoke decision: selected={res.selected} "
          f"scores={[round(s.score, 3) for s in res.scores]}", flush=True)
    return 0


def _fast_accuracy(model, actions, states):
    """Accuracy of the fast (contrastive) path over a set of states."""
    from .types import Decision
    from .engine.decision_engine import DecisionEngine
    from .backends.mock import world_answer
    engine = DecisionEngine(model)
    correct = 0
    for s in states:
        res = engine.decide(Decision(state=s, actions=actions))
        if res.selected == world_answer(s, actions):
            correct += 1
    return correct / len(states) if states else 0.0


def cmd_train(args) -> int:
    router, model = _build_router(args, mode="always_fast", skill=0.2)
    from .bench.datasets import tool_actions
    from .train.data import ContrastiveDataset, Example
    from .train.trainer import Trainer
    from .backends.mock import world_answer

    actions = tool_actions()
    states = [f"train-task-{i}" for i in range(300)]
    before = _fast_accuracy(model, actions, states)

    ds = ContrastiveDataset()
    for s in states:
        ds.examples.append(Example(state=s, actions=actions, correct_key=world_answer(s, actions)))
    trainer = Trainer(model, loss=args.loss, temperature=0.07, lr=0.05)
    print(f"training {len(ds)} examples x {args.epochs} epochs (lr=0.05)...", flush=True)
    trainer.fit(ds, epochs=args.epochs)
    after = _fast_accuracy(model, actions, states)

    print(f"fast-path accuracy: {before:.3f} -> {after:.3f}  (skill {model.head.skill:.3f})", flush=True)

    print("--- full benchmark (fast path) ---", flush=True)
    from .bench.runner import run_all
    run_all(router, n=200)
    return 0


def cmd_bench(args) -> int:
    router, _ = _build_router(args, mode="always_fast")
    from .bench.runner import run_all
    run_all(router, n=args.n)
    return 0


def cmd_speedup(args) -> int:
    router, _ = _build_router(args)
    from .bench.latency import build_report
    from .bench.datasets import tool_actions
    print(build_report(router, tool_actions(), n=args.n), flush=True)
    return 0


def cmd_decide(args) -> int:
    router, _ = _build_router(args)
    from .types import Action, Decision
    actions = [Action(key=k, name=k) for k in args.actions.split(",") if k]
    res = router.route(Decision(state=args.state, actions=actions))
    print(f"selected={res.selected} path={res.path} "
          f"confidence={res.confidence:.3f} latency={res.latency_ms:.2f}ms", flush=True)
    for s in sorted(res.scores, key=lambda x: x.score, reverse=True):
        print(f"  {s.key:<20} score={s.score:.4f}", flush=True)
    return 0


def cmd_serve(args) -> int:
    router, _ = _build_router(args)
    from .serving.server import run_server
    run_server(router, host=args.host, port=args.port, token=args.token)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="clmforge", description="Contrastive Language Model decision engine")
    p.add_argument("--config", default="config.yaml", help="path to config (yaml/json)")
    p.add_argument("--version", action="version", version=f"clmforge {__version__}")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("doctor")
    t = sub.add_parser("train"); t.add_argument("--epochs", type=int, default=10); t.add_argument("--loss", default="infonce")
    b = sub.add_parser("bench"); b.add_argument("--n", type=int, default=200)
    s = sub.add_parser("speedup"); s.add_argument("--n", type=int, default=500)
    d = sub.add_parser("decide"); d.add_argument("--state", required=True); d.add_argument("--actions", required=True)
    sv = sub.add_parser("serve"); sv.add_argument("--host", default="127.0.0.1"); sv.add_argument("--port", type=int, default=8765); sv.add_argument("--token", default="")

    args = p.parse_args(argv)
    if args.cmd is None:
        p.print_help()
        return 0
    return {
        "doctor": cmd_doctor,
        "train": cmd_train,
        "bench": cmd_bench,
        "speedup": cmd_speedup,
        "decide": cmd_decide,
        "serve": cmd_serve,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
