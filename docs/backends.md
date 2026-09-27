# 后端说明

## mock（默认）

确定性可训练后端。`world_answer(state, actions)` 派生 ground-truth，打分 =
`skill·2·[is_correct] + noise`。用于演示、评测、训练，零依赖。

## frozen

纯嵌入后端，用 `FrozenBackbone`（确定性哈希嵌入）做快路径。

## openai

OpenAI 兼容 chat completions 接口，慢路径，用标准库 `urllib` 调用。

## vllm

复用 openai 后端，指向 vLLM 的 OpenAI 兼容端点。

## transformers

本地 HF pipeline，慢路径，懒加载 `torch`+`transformers`。

## 自定义后端

继承 `BaseBackend`，实现 `generate`（慢路径）与可选 `encode_*`（快路径），在
`factory.py` 注册即可。
