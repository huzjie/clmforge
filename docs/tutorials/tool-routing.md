# 教程：用 clmforge 做工具路由

场景：给一个用户请求，从一组工具里选最合适的那个。

```python
from clmforge.models.clm_model import CLMModel
from clmforge.engine.decision_engine import DecisionEngine
from clmforge.types import Action, Decision

model = CLMModel()
engine = DecisionEngine(model)
tools = [Action("search", "search_web"), Action("calc", "calc"), Action("mail", "send_email")]

result = engine.decide(Decision(state="2+3等于几", actions=tools))
print(result.selected)   # -> calc
```

复用同一个 `tools` 列表即可享受动作嵌入缓存。
