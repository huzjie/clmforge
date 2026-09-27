# 架构设计

## 分层架构

```
┌────────────────────────────────────────────────────┐
│  CLI (cli.py) / HTTP (serving/)                    │
├────────────────────────────────────────────────────┤
│  engine/  DecisionEngine · Router · confidence     │
├────────────────────────────────────────────────────┤
│  models/  CLMModel · StateEncoder · ActionEncoder   │
│           ActionCache · HeadWrapper · backbone     │
├────────────────────────────────────────────────────┤
│  backends/ mock · frozen · openai · vllm · tf      │
├────────────────────────────────────────────────────┤
│  core/  config · types · embeddings · scoring      │
└────────────────────────────────────────────────────┘
```

## 数据流

1. 用户提交 `Decision(state, actions)`
2. `StateEncoder` 编码 state → `e_s`
3. `ActionCache.encode_all(actions)` 取动作嵌入（命中缓存则复用）
4. `HeadWrapper.score_all(e_s, e_a)` 产出分数
5. `confidence_margin` 算 margin
6. `Router` 按 margin 选择快/慢路径
7. 返回 `DecisionResult`（含 selected / scores / path / latency / cache_hits）

## 关键设计决策

- **解耦编码**：state 与 action 编码互不依赖，动作嵌入可缓存
- **确定性优先**：mock 后端 + MD5 派生，全部结果跨运行可复现
- **零依赖兜底**：核心不 import 任何第三方库，YAML 用内置子集解析器
- **能力/偏差分离**：mock 打分 = skill·信号 + noise，训练只动 skill

详见 README 与 INTRO.md。
