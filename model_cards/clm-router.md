---
license: apache-2.0
language: zh
---

# 快慢路由器（教学示意）

## 设计

- 快路径：对比式打分（微秒级）
- 慢路径：生成式后端（质量兜底）
- 触发：confidence margin 低于阈值时回退

## 统计

`Router.stats` 与 `Router.ratio()` 提供快慢占比。
