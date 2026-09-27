---
license: apache-2.0
language: zh
---
# 双线性打分头（教学示意）

## 公式

`score = e_s^T W e_a`，其中 W ∈ R^(d×d)。

## 特点

- 捕捉 state 与 action 维度间的二阶交互
- 参数量 O(d²)，d 小时开销可忽略
- 默认打分头
