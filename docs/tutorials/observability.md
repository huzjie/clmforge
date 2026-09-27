# 教程：可观测性

```python
from clmforge.observability.metrics import DecisionMetrics
from clmforge.observability.tracer import Tracer

metrics = DecisionMetrics()
tracer = Tracer("decisions.jsonl")
# 每个决策后：metrics.record(result); tracer.trace(decision, result)
print(metrics.summary())
```

`Tracer` 落 JSONL，`DecisionMetrics` 给聚合指标。
