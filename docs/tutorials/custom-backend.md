# 教程：接你自己的后端

接 OpenAI 兼容服务（如 vLLM）：

```yaml
# config.yaml
backend: openai
backend_kwargs:
  base_url: http://localhost:8000/v1
  model: Qwen/Qwen3-8B
```

接 HF Transformers：

```python
from clmforge.backends.factory import make_backend
b = make_backend("transformers", model="Qwen/Qwen3-8B")
b.generate(state, actions)
```

自定义：继承 `BaseBackend` 实现 `generate` 即可。
