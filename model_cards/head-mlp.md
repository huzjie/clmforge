---
license: apache-2.0
language: zh
---
# MLP 打分头（教学示意）

## 公式

`score = W2 · ReLU(W1 · [e_s; e_a] + b1) + b2`

## 特点

- 表达能力最强，适合复杂打分
- 参数量 O(d·h)，h 为隐层宽度
