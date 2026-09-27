# Examples

每个示例都是可直接运行的独立脚本，无需额外依赖：

```bash
python examples/demo_basic.py          # 快速路径基础决策
python examples/demo_cache.py          # 动作嵌入缓存加速
python examples/demo_router.py         # 快/慢路径路由
python examples/demo_train.py          # 训练提升准确率
python examples/demo_serve.py          # HTTP 服务端到端
python examples/demo_tool_routing.py   # 工具路由
python examples/demo_benchmark.py      # 完整基准评测
```

所有示例都使用确定性 mock 后端，跨平台、跨运行可复现。
