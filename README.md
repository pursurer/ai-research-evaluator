# AI Research Direction Evaluator

> 基于 P-F-C 模型的 AI 研究方向自动评估系统  
> Automated AI Research Direction Evaluation System based on P-F-C Model

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/pursurer/ai-research-evaluator/actions/workflows/tests.yml/badge.svg)](https://github.com/pursurer/ai-research-evaluator/actions)

---

## Overview / 概述

本系统通过融合顶会论文数据与行业动态，基于 **P-F-C 评估模型**（Potential-Feasibility-Competition），为研究者提供：

- **研究方向量化评分** — 7 项二级指标综合评估
- **趋势分析** — 基于 NeurIPS/ICLR/ICML 等 9 大顶会数据
- **决策建议** — 战略重点 / 差异化突围 / 快速捡漏 / 审慎避开

### P-F-C Model / 评估模型

```
ROI Score = 0.35 × P_avg + 0.40 × F_min + 0.25 × C_avg

P (Potential 35%):   P1 趋势红利 + P2 叙事深度 + P3 SOTA 渗透率
F (Feasibility 40%): min(F1 算力, F2 数据, F3 周期) ← 短板计分
C (Competition 25%): C1 巨头避让度 + C2 研究空白区

🚨 熔断机制: F_min < 3 → 直接判定"不可行"
```

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
