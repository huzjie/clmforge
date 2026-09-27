# 基准评测说明

## 内置基准

| 基准 | 任务 | 动作数 |
|---|---|---|
| bfcl | 工具调用 | 6 |
| ranking | 候选排序 | 10 |
| verification | 二值校验 | 2 |
| gaming | 游戏动作 | 8 |
| wikiracing | 链接选择 | 10 |

## 指标

- `accuracy`：正确选择占比
- `avg_latency_ms`：平均决策延迟
- `fast_ratio`：走快路径的占比
- `cache_hit_rate`：动作缓存命中率

## 延迟基准

`bench/latency.py` 对比「对比式快路径」与「模拟生成式基线」，输出加速比。
