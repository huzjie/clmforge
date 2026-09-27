# 快/慢路由设计

## 三种模式

- `always_fast`：永远走对比打分
- `always_slow`：永远走生成式后端
- `margin`：按置信度 margin 动态路由（默认）

## 路由逻辑

```
result = engine.decide(decision)
if result.confidence >= margin_threshold:  return result   # fast
else:                                      return slow(decision)  # slow
```

## 统计

`Router.stats` 记录 `{"fast": N, "slow": M}`，`ratio()` 返回快路径占比。
