# Contributing

欢迎贡献。请：

1. 保持核心零依赖（`clmforge/core`、`clmforge/models`、`clmforge/engine`）
2. 新后端继承 `BaseBackend` 并在 `factory.py` 注册
3. 新基准继承 `Benchmark` 并在 `runner.py` 挂载
4. 跑 `python -m unittest discover -s tests -t .` 保证全绿
5. 提交信息用 `feat:` / `fix:` / `docs:` 前缀
