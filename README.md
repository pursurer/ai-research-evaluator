# AI Research Direction Evaluator

> 基于 P-F-C 模型的 AI 研究方向自动评估系统  
> Automated AI Research Direction Evaluation System based on P-F-C Model

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/pursurer/ai-research-evaluator/actions/workflows/tests.yml/badge.svg)](https://github.com/pursurer/ai-research-evaluator/actions)

---

## Overview / 概述

### 解决的问题 / Problem

AI 研究者在选择研究方向时面临三大困境：

1. **信息过载**：每天 arXiv 数十篇新论文，顶会数千篇投稿，无法全面追踪
2. **判断盲区**：不清楚某方向是"蓝海机会"还是"巨头垄断的红海"
3. **资源错配**：投入数月后才发现算力不足、数据难获取，沉没成本巨大

### 系统功能 / What It Does

**输入 / Input**：
- 用户手动输入研究方向关键词（如 "Video Generation"、"RAG"、"Multimodal Alignment"）
- 或系统从顶会论文中自动发现并推荐热点方向

**输出 / Output**：
- 该方向的 **7 项指标量化评分**（1-10 分）
- **综合 ROI 分数**
- **决策建议**（4 级分类）
- **趋势分析**与 **6-12 个月演进预测**
- **潜在风险提示**
- **核心竞争点分析**

---

## P-F-C 评估框架 / Evaluation Framework

### 设计理念 / Design Philosophy

借鉴投资领域的"风险收益评估"思想，将研究方向视为一项"投资"：
- **P (Potential)**：潜在收益有多大？
- **F (Feasibility)**：我有能力实现吗？
- **C (Competition)**：竞争对手是谁？

### P 维度：科研潜力 / Potential（权重 35%）

> 决定了论文是发在顶会 Oral 还是普通 Workshop

| 指标 | 核心问题 | 高分特征 | 低分特征 |
|------|---------|---------|---------|
| **P1 趋势红利** | 该方向在顶会的热度趋势 | 指数爆发期（如 Video Gen、Agent） | 逐年下降，被视为过时 |
| **P2 叙事深度** | 是科学问题还是工程 Trick？ | 能关联第一性原理、Scaling Law | 仅对特定数据集有效 |
| **P3 SOTA 渗透率** | 想被认可需要提升多少？ | 新领域，简单改进即 SOTA | 榜单饱和（99%+），提升极难 |

### F 维度：技术可行性 / Feasibility（权重 40%）— ⚠️ 核心风控项

> 对于非巨头团队，这是能否做出来的**决定性因素**

| 指标 | 核心问题 | 高分特征 | 低分特征 |
|------|---------|---------|---------|
| **F1 算力匹配度** | 你的显卡能支撑吗？ | 单卡 4090 / Colab 即可 | 需 H100 集群从零预训练 |
| **F2 数据获取** | 数据从哪来？ | HuggingFace 现成高质量数据 | 私有数据、需昂贵人工标注 |
| **F3 迭代周期** | 跑一次实验多久？ | < 12 小时（一天验证 2 个 Idea） | > 1 周（Debug 成本极高） |

**关键设计：短板计分法**
```
F 维度得分 = min(F1, F2, F3)
```
> 逻辑：如果算力是 1 分，哪怕数据和周期都是 10 分，整个 F 项也只能得 1 分。避免"眼高手低"。

### C 维度：竞争环境 / Competition（权重 25%）

> 决定了是否会撞车及生存空间

| 指标 | 核心问题 | 高分特征 | 低分特征 |
|------|---------|---------|---------|
| **C1 巨头避让度** | OpenAI/Google/Meta 在做吗？ | 冷门或交叉领域，大厂未涉足 | 主战场，每天 arXiv 几十篇 |
| **C2 研究空白区** | 还有创新空间吗？ | 处女地，可定义新任务 | 缝隙极小，只能做 A+B 缝合 |

### 评分计算 / Scoring Formula

```
ROI Score = 0.35 × P_avg + 0.40 × F_min + 0.25 × C_avg

其中：
- P_avg = (P1 + P2 + P3) / 3
- F_min = min(F1, F2, F3)  ← 短板决定
- C_avg = (C1 + C2) / 2
```

**🚨 熔断机制**：若 `F_min < 3` → 无论总分多高，直接判定"不可行"

### 决策输出 / Decision Output（4 级分类）

| 等级 | 触发条件 | 典型特征 | 建议 |
|------|---------|---------|------|
| **战略重点** | ROI ≥ 7.0 | 高潜易发：热度够、资源够、能落地 | All-in，追求速度 |
| **差异化突围** | 5.5 ≤ ROI < 7.0 且 P_avg > 8 | 高潜高难：潜力极大但有单一短板 | 找合作者补短板，不死磕 |
| **快速捡漏** | 5.5 ≤ ROI < 7.0 且 F_min > 8 | 低潜易行：容易做但创新有限 | 保底策略，适合练手 |
| **审慎避开** | ROI < 5.5 或触发熔断 | 红海或死胡同 | 坚决放弃，不被媒体热度迷惑 |

---

## 信息来源 / Data Sources

### 静态数据：顶会论文 / Conference Papers（当前已集成）

从 **9 个 AI 顶级学术会议** 提取论文数据：

| 会议 | 领域侧重 |
|------|---------|
| **NeurIPS** | 机器学习理论与应用 |
| **ICLR** | 表示学习、深度学习 |
| **ICML** | 机器学习核心算法 |
| **AAAI** | 人工智能综合 |
| **ACL** | 自然语言处理 |
| **EMNLP** | NLP 实证方法 |
| **NAACL** | 北美 NLP |
| **IJCAI** | AI 综合（偏应用） |
| **AISTATS** | AI 与统计交叉 |

**提取字段**：论文 ID、标题、**关键词**（趋势分析）、**摘要**（LLM 分析）、年份、展示类型

### 动态情报：行业动态 / Industry Intelligence（未来模块）

**监控对象**：OpenAI、DeepMind、Meta AI、Anthropic

| 来源 | 权重 | 理由 |
|------|------|------|
| **arXiv 预印本** | 40% | 技术深度最高，学术一手资料 |
| **官方 Blog** | 35% | 代表公司战略方向，信号明确 |
| **X (Twitter)** | 25% | 时效性强但噪声较高 |

**更新频率**：每周汇总

### 外部 API 增强 / External APIs（未来模块）

| API | 用途 |
|-----|------|
| **Google Trends** | 补充 P1 趋势红利的外部数据 |
| **Papers With Code** | 获取 SOTA 榜单，量化 P3 指标 |
| **Semantic Scholar / OpenAlex** | 补全论文引用数，衡量影响力 |

### 实体对齐 / Entity Alignment（动态 ↔ 静态数据关联）

| 层级 | 对齐方式 | 示例 |
|------|---------|------|
| **Layer 1** | 关键词/主题匹配 | "Video Generation" ↔ 含该关键词的论文 |
| **Layer 2** | 方法/模型对齐 | "Sora" ↔ Video Diffusion 相关论文 |
| **Layer 3** | 机构/作者对齐 | OpenAI 动态 ↔ OpenAI 作者的顶会论文 |

---

## Installation / 安装

```bash
# Clone the repository
git clone https://github.com/pursurer/ai-research-evaluator.git
cd ai-research-evaluator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and fill in your API keys
```

---

## Quick Start / 快速开始

```bash
# Evaluate a research direction
python scripts/evaluate.py --direction "Video Generation"

# Discover hot research topics
python scripts/discover.py --top-k 10

# Batch evaluation
python scripts/batch_evaluate.py --input directions.txt
```

### Python API

```python
from src.evaluation import EvaluationEngine
from src.llm import LLMClientFactory

# Initialize
llm = LLMClientFactory.create("openai")
engine = EvaluationEngine(llm=llm)

# Evaluate
result = engine.evaluate(direction="Multimodal Alignment")
print(f"ROI Score: {result.roi_score}")
print(f"Decision: {result.decision.value}")
```

---

## Project Structure / 项目结构

```
ai-research-evaluator/
├── src/
│   ├── data/           # 数据加载与处理
│   ├── evaluation/     # P-F-C 评估引擎
│   ├── llm/            # LLM 抽象层
│   ├── report/         # 报告生成
│   └── utils/          # 通用工具
├── tests/              # 测试用例
├── scripts/            # CLI 脚本
├── config/             # 配置文件
└── reports/            # 生成的报告
```

---

## Supported Data Sources / 支持的数据源

### Conference Papers / 顶会论文 (已集成)
| Conference | Status |
|------------|--------|
| NeurIPS | ✅ |
| ICLR | ✅ |
| ICML | ✅ |
| AAAI | ✅ |
| ACL | ✅ |
| EMNLP | ✅ |
| NAACL | ✅ |
| IJCAI | ✅ |
| AISTATS | ✅ |

---

## Roadmap / 未来模块

> 以下功能将在后续版本中逐步实现

| Module | Description | Priority |
|--------|-------------|----------|
| **External Trends** | Google Trends API 集成 | P1 |
| **Papers With Code** | SOTA 榜单数据获取 | P1 |
| **Citation Data** | Semantic Scholar / OpenAlex API | P2 |
| **X (Twitter) Monitor** | 大厂官方动态监控 | P3 |
| **Blog RSS** | AI 实验室技术博客订阅 | P3 |
| **arXiv Tracker** | 预印本论文追踪 | P3 |
| **Entity Alignment** | 动态情报与论文数据对齐 | P4 |

---

## Configuration / 配置

### Environment Variables / 环境变量

```bash
# LLM Provider (choose one)
LLM_PROVIDER=openai          # openai / anthropic / local
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx

# Data Path
PAPERS_DATA_ROOT=/path/to/顶会论文信息

# GitHub (for auto-sync)
GITHUB_TOKEN=ghp_xxx
```

### LLM Support / 支持的 LLM

- OpenAI GPT-4 / GPT-4o
- Anthropic Claude 3.5
- Local models (Ollama, etc.)

---

## Development / 开发

```bash
# Run tests
pytest

# Code formatting
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Lint
ruff check src/
```

---

## License / 许可证

MIT License - see [LICENSE](LICENSE) for details.

---

## Contributing / 贡献

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request
