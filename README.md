# AI Research Direction Evaluator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/pursurer/ai-research-evaluator/actions/workflows/tests.yml/badge.svg)](https://github.com/pursurer/ai-research-evaluator/actions)

A planned LLM tool that rates an AI research direction before you spend months on it. It scores
**Potential**, **Feasibility** and **Competition** (the P-F-C model: 7 indicators, each 1–10) and
combines them into one ROI score, with feasibility as a hard floor.

> **Early stage.** Only the conference-paper data layer is built. The scoring engine, LLM layer
> and report generator are designed but not written yet.

## Status

| Part | State |
| --- | --- |
| Data layer (`src/data`): load and clean conference-paper CSVs into typed `Paper` objects | Done, 21 tests in CI on Python 3.10–3.12 |
| P-F-C scoring engine (`src/evaluation`) | Planned |
| LLM client (`src/llm`) | Planned |
| Report generator (`src/report`) | Planned |
| CLI (`scripts/evaluate.py`) | Parses arguments, then prints a placeholder |

The full design, with every indicator, the scoring formula and the four decision tiers, is in
[docs/DESIGN.md](docs/DESIGN.md) (Chinese and English).

## What runs today

The data layer reads the CSVs in [top-ai-conference-papers](https://github.com/pursurer/top-ai-conference-papers)
(NeurIPS, ICLR, ICML, AAAI, ACL, EMNLP, NAACL, IJCAI, AISTATS), built with
[paper_scraper](https://github.com/pursurer/paper_scraper).

```bash
git clone https://github.com/pursurer/ai-research-evaluator.git
cd ai-research-evaluator
pip install -r requirements.txt

git clone https://github.com/pursurer/top-ai-conference-papers.git ../top-ai-conference-papers
export PAPERS_DATA_ROOT=../top-ai-conference-papers
```

```python
from src.data import PapersLoader

loader = PapersLoader()                     # reads PAPERS_DATA_ROOT
neurips = loader.load_conference("neurips")
print(neurips.name, neurips.year, neurips.paper_count)   # NeurIPS 2025 5275

video = neurips.get_papers_by_keyword("video generation")
print(len(video))                                         # 65
```

Keyword search only finds papers whose source listed keywords. Of the nine conferences loaded
here, only NeurIPS, ICLR and ICML have them in the 2025 data; the other six load with titles and
abstracts only.

## Tests

```bash
pytest
```

CI also runs mypy, black, isort and ruff.

## License

MIT, see [LICENSE](LICENSE).
