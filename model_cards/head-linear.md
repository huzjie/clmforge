---
license: apache-2.0
language: zh
---

# 线性打分头（教学示意）

## 公式

`score = w · (e_s ⊙ e_a)`（逐元素相乘后加权求和）。

## 特点

- 参数量 O(d)，最轻量
- 适合高维嵌入 + 快速打分
