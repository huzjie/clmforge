# CLMModel API

```python
from clmforge.models.clm_model import CLMModel

model = CLMModel(embed_dim=64, head_type="bilinear", skill=0.5)
scores, hits = model.score(state, actions)   # 打分 + 缓存命中数
e_s = model.encode_state(state)              # 状态嵌入
model.train_step(delta, lr=0.05)             # 训练一步
```

参数：`embed_dim`、`head_type`（linear/bilinear/mlp）、`normalize`、
`cache_max`、`cache_persist`、`cache_path`、`skill`。
