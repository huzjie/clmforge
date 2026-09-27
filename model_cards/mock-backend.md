---
license: apache-2.0
language: zh
---
# 确定性 Mock 后端（教学示意）

## 设计

- ground-truth 由 `world_answer(state, actions)` 用 MD5 派生
- 打分 = `skill·2·[is_correct] + noise`
- `train_step` 上调 skill

## 用途

零依赖演示「训练 → 准确率上升」的可复现曲线，以及全部基准评测。
