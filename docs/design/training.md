# 训练设计

## 损失函数

- InfoNCE：`-log(exp(s_p/τ)/Σexp(s_j/τ))`
- Margin：`Σ_j max(0, margin - (s_p - s_j))`

## 训练器

`train/trainer.py` 的 `Trainer` 是无梯度（gradient-free）实现：每步判断正样本是否
胜出，据此上下调 skill。适用于 mock 后端；接真实打分头时替换为 torch 反向传播。

## 数据

`ContrastiveDataset` 由 `(state, actions, correct_key)` 组成，`Example` 是单条样本。
