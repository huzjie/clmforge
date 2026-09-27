---
license: apache-2.0
language: zh
---
# 冻结主干（教学示意）

## 设计

- 只负责编码，参数冻结
- 零依赖实现用 MD5 派生确定性向量替代真实 transformer 编码
- 接入真实 encoder 只需覆写 `encode`

## 意义

把「编码」与「打分」解耦，编码可离线预计算并缓存。
