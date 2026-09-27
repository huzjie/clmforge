# 教程：训练打分头

```bash
python -m clmforge train --epochs 10
```

输出训练后的 skill 与「训练后基准准确率」。用 `--config` 指定配置，用 `--loss`
选 `infonce` 或 `margin`。

mock 后端演示的是「训练 → 准确率上升」的确定性曲线；接真实打分头时替换为 torch
反向传播（见 `docs/design/training.md`）。
