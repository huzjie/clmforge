# 高级：零依赖设计

clmforge 核心不 import 任何第三方库。要点：

1. 嵌入用 MD5 派生确定性向量
2. YAML 用内置子集解析器 `yamlish`
3. HTTP 服务用 `http.server`，客户端用 `urllib`
4. 训练用无梯度信号，不依赖 torch

这使得项目在最小环境（裸 Python 3.9+）即可跑通全部功能。
