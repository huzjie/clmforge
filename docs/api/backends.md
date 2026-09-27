# 后端 API

```python
from clmforge.backends.factory import make_backend

backend = make_backend("mock", skill=0.7, noise=0.4)
backend.generate(state, actions)             # 慢路径：返回 action key
backend.train_step(delta)                    # 训练（若支持）
```

支持的 kind：`mock` / `frozen` / `openai` / `vllm` / `transformers`。
