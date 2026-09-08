# Final Project — CLO Mapping

Every required project component maps to the course CLOs. A project earns
CLO-1, CLO-2, and CLO-3 coverage when **all three** shaded rows below are
present.

**Course CLOs**

| ID | CLO |
|---|---|
| CLO-1 | Apply Python and standard data science libraries to acquire, clean, manipulate, visualize and explore datasets. |
| CLO-2 | Apply appropriate data science tools and basic machine learning techniques to solve introductory data-driven problems. |
| CLO-3 | Develop simple AI-assisted data science workflows using LLMs, local models, automation tools and basic AI agents while considering reproducibility, ethics and responsible AI use. |

## 1. Component → CLO matrix

| # | Required component | CLO-1 | CLO-2 | CLO-3 |
|---|---|---|---|---|
| 1 | Problem definition | • | | |
| 2 | Dataset / data source | • | | |
| 3 | Data acquisition (reproducible, cached) | • | | |
| 4 | Data cleaning (logged decisions) | • | | |
| 5 | EDA (univariate, groups, correlations) | • | | |
| 6 | Visualization (≥ 3 labeled figures) | • | | |
| 7 | Basic ML model (scikit-learn, train/test) | | • | |
| 8 | Model evaluation (metric + baseline) | | • | |
| 9 | Streamlit application (widgets, interactive) | • | | |
| 10 | GitHub repository (≥ 10 commits) | • | | |
| 11 | README (runnable-by-a-stranger) | • | | |
| 12 | Final report (incl. ethics + AI disclosure) | | | • |
| 13 | Presentation (narrative + Q&A) | | | • |
| — | *AI-assisted analysis (mandatory, minimal)* | | | • |
| — | *Optional: PandasAI / Ollama / LLM / agent / n8n* | | | • |

**Coverage rule:** CLO-1 ← components 1–6, 9–11 · CLO-2 ← components 7–8 ·
CLO-3 ← components 12–13 + AI-assisted analysis. A submission missing the
AI-assisted analysis step does **not** cover CLO-3 regardless of the report.

## 2. Rubric criterion → CLO matrix

| Rubric criterion (weight) | CLO-1 | CLO-2 | CLO-3 |
|---|---|---|---|
| Problem framing & data acquisition (20%) | • | | |
| Cleaning & EDA + Streamlit app (25%) | • | | |
| Modeling + evaluation (25%) | | • | |
| AI-assisted analysis (15%) | | | • |
| Reproducibility & ethics (10%) | | | • |
| Presentation & communication (5%) | | | • |

## 3. Assessment instruments that share these CLOs

| Instrument | CLOs assessed | Relationship to project |
|---|---|---|
| Quiz 1 (W1–7) | CLO-1 | Acquire/clean/manipulate/viz skills |
| Quiz 2 (W8–14) | CLO-1, CLO-2, CLO-3 | ML + AI-tooling concepts |
| Midterm (W1–8) | CLO-1, CLO-2 | Practical notebook task |
| Final (W9–16) | CLO-1, CLO-2, CLO-3 | Includes ethics/agent scenario |
| Labs 1–24 | CLO-1, CLO-2 | Skill building for project parts 1–8 |
| Labs 25–32 | CLO-3 | Skill building for AI-assisted step |
| Assignment 1 (cleaning + EDA) | CLO-1 | Rehearsal of project parts 4–6 |
| Assignment 2 (API + Streamlit) | CLO-1, CLO-3 | Rehearsal of project parts 3, 9, 10, 11 |
| Viva | CLO-1, CLO-2, CLO-3 | Verifies individual understanding |

## 4. Bloom's level coverage

| Component | Dominant Bloom level |
|---|---|
| Problem definition | Create |
| Data acquisition / cleaning | Apply |
| EDA / visualization | Analyze |
| Modeling + evaluation | Apply / Evaluate |
| Streamlit app | Apply / Create |
| AI-assisted analysis | Apply / Evaluate (verification) |
| Report (ethics) | Evaluate |
| Presentation / viva | Understand / Evaluate |