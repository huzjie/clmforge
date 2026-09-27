# DecisionEngine / Router API

```python
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.engine.router import Router

engine = DecisionEngine(model, top_k=1)
result = engine.decide(decision)             # DecisionResult

router = Router(engine, mode="margin", margin_threshold=0.2, slow_backend=slow)
result = router.route(decision)              # 自动快/慢
print(router.stats)                          # {"fast": N, "slow": M}
```

`DecisionResult` 字段：`selected`、`scores`、`path`、`confidence`、`latency_ms`、
`cache_hits`、`meta`。
