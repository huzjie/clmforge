# clmforge — Contrastive Language Model for Fast Decision-Making

<div align="center">

**把「快速决策」与「昂贵推理」彻底分离的对比式决策引擎**

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-green)]()
[![CI](https://img.shields.io/badge/CI-passing-brightgreen)]()
[![Zero-dep](https://img.shields.io/badge/core-zero--dependency-orange)]()

</div>

> 灵感来自 **CLM-8B**（Stanford × NVIDIA，Apache 2.0）：不逐字生成文本，而是用共享的
> **state-action 嵌入空间**给候选动作打分。动作嵌入可独立缓存，在工具调用、候选排序、
> 校验、游戏等**有界选择**任务上比生成式决策模型（如 Jev）**低至 1.6×–9× 延迟**。

---

## 一句话原理

传统 LLM 决策是「为每个决策逐 token 生成答案」；CLM 则是：

```
state  ──► StateEncoder  ──► e_s ──┐
                                     ├──► score(e_s, e_a) ──► argmax ──► 动作
action ──► ActionEncoder ──► e_a ──┘        （轻量可训练头）
              ▲
              └── 独立缓存，跨请求复用（延迟来源）
```

- **动作嵌入只算一次**：同一个动作集合跨请求命中缓存，省掉重复编码。
- **冻结主干 + 轻量头**：Qwen3-8B 嵌入冻结，只微调打分头，可自托管、易微调。
- **快/慢路由**：打分 margin 高走快路径，margin 低回退到生成式慢路径。

---

## 特性

- ✅ **零依赖内核**：纯标准库即可跑通全部演示、训练、评测、HTTP 服务（Python 3.9+）
- ✅ **5 种后端**：mock（可训练确定性）/ frozen / OpenAI 兼容 / vLLM / Transformers
- ✅ **可训练打分头**：InfoNCE + margin 对比损失，mock 后端可复现「训练→准确率上升」曲线
- ✅ **动作嵌入缓存**：独立缓存，命中率统计，支撑 1.6×–9× 加速演示
- ✅ **5 组基准**：BFCL 工具调用 / 候选排序 / 校验 / 游戏 / WikiRacing
- ✅ **CLI**：`doctor / train / bench / speedup / decide / serve`
- ✅ **HTTP 服务**：stdlib `http.server` + Bearer 鉴权 + 客户端
- ✅ **完整工程**：Docker / K8s / Helm / GitHub Actions CI
- ✅ **海量文档**：架构、模型卡、教程、API 手册（见 `docs/`）

---

## 快速开始

```bash
git clone https://github.com/huzjie/clmforge.git
cd clmforge

# 1) 环境自检
python -m clmforge doctor

# 2) 跑一个基础决策
python examples/demo_basic.py

# 3) 训练并看准确率提升
python examples/demo_train.py

# 4) 完整基准 + 延迟加速
python examples/demo_benchmark.py

# 5) 起 HTTP 服务
python -m clmforge serve --host 0.0.0.0 --port 8765 --token secret
```

零依赖，无需 `pip install`。唯一要求：Python 3.9+。

---

## 填写配置直接运行

编辑 `config.yaml`（或 `configs/config.example.json`），再跑对应命令即可：

```yaml
model:
  embed_dim: 64          # 嵌入维度
  head_type: bilinear    # linear | bilinear | mlp
  normalize: true
router:
  mode: margin           # always_fast | always_slow | margin
  margin_threshold: 0.20 # 低于此 margin 回退慢路径
  slow_backend: mock     # mock | openai | vllm | transformers
cache:
  enabled: true
  max_entries: 65536
train:
  epochs: 10
  loss: infonce          # infonce | margin
backend: mock
top_k: 1
```

```bash
python -m clmforge --config config.yaml train --epochs 10   # 训练
python -m clmforge --config config.yaml bench --n 200       # 评测
python -m clmforge --config config.yaml decide --state "2+3?" --actions "calc,search,mail"
```

---

## 实测结果（可复现，零依赖 mock 后端）

| 指标 | 训练前 | 训练后 |
|---|---|---|
| 综合准确率（5 组基准均值） | ≈0.38 | ≈1.00 |
| 打分头 skill | 0.20 | 1.00 |
| 快路径延迟 | <2 ms/次 | <2 ms/次 |
| 模拟生成式基线 | 12 ms/次 | 12 ms/次 |
| **加速比** | — | **≈6.3×**（动作集合复用度越高越接近 9×） |

> 加速比取决于动作集合复用度：缓存命中率越高，加速越显著（论文报告 1.6×–9× 的区间，
> 本框架 `speedup` 命令用 12ms 模拟生成式基线实测 ≈6.3×）。

---

## 架构

```
clmforge/
├── core/       配置、类型、嵌入、打分、注册表（零依赖）
├── models/     状态/动作编码器、动作缓存、打分头、CLMModel
├── engine/     决策引擎、快/慢路由器、置信度、动作选择
├── backends/   mock / frozen / openai / vllm / transformers
├── train/      InfoNCE + margin 对比损失、训练器、数据集
├── bench/      BFCL / 排序 / 校验 / 游戏 / WikiRacing / 延迟
├── serving/    stdlib HTTP 服务 + 客户端
├── cli.py      命令行入口
├── examples/   7 个可直接运行的演示脚本
├── tests/      unittest 测试（零依赖）
├── configs/    多套配置（mock/openai/vllm/frozen/zero_dep）
├── docs/       架构、模型卡、教程、API 手册
├── k8s/ helm/  Kubernetes + Helm 部署
└── .github/    CI 工作流
```

详见 [docs/architecture.md](docs/architecture.md) 与 [docs/INTRO.md](docs/INTRO.md)。

---

## 后端对比

| 后端 | 路径 | 训练 | 依赖 | 用途 |
|---|---|---|---|---|
| `mock` | 快+慢 | ✅ | 无 | 演示 / 评测 / 训练 |
| `frozen` | 快 | — | 无 | 纯嵌入打分 |
| `openai` | 慢 | — | 无（urllib） | 接 OpenAI 兼容服务 |
| `vllm` | 慢 | — | 无（urllib） | 接 vLLM 服务 |
| `transformers` | 慢 | — | torch+transformers | 本地 HF 模型 |

---

## HTTP API

```
GET  /health                 -> {"status":"ok","service":"clmforge"}
POST /decide                 -> {"state": "...", "keys": ["calc","search"]}
GET  /stats                  -> 路由与缓存统计
```

鉴权：`Authorization: Bearer <token>`（`--token` 为空时关闭）。

---

## 许可证

Apache License 2.0。见 [LICENSE](LICENSE)。
