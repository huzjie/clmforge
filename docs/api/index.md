# API 参考

## 顶层

- `CLMModel` — 对比式决策模型（编码 + 打分 + 缓存 + 训练）
- `DecisionEngine` — 快路径打分引擎
- `Router` — 快/慢路由
- `load_config` — 配置加载（YAML/JSON）

## 数据类

- `Action` / `Decision` / `ScoreResult` / `DecisionResult`

## 打分头

- `LinearHead` / `BilinearHead` / `MLPHead` / `make_head`

## 训练

- `Trainer` / `infonce_loss` / `margin_loss` / `ContrastiveDataset` / `Example`

## 后端

- `make_backend` / `MockBackend` / `FrozenEmbeddingsBackend` / `world_answer`
