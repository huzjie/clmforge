# 高级：确定性保证

所有随机行为都用 MD5（`hashutil.py`）派生，不依赖 `hash()`（受 PYTHONHASHSEED
影响）与 `random`（除非显式传 seed）。因此同一输入在任何平台、任何运行都得到
相同结果，基准与演示完全可复现。
