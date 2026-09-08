# Labs

Thirty-two practical lab exercises — **one per course session** — that build
up week by week from beginner to intermediate. Students write substantial
code themselves; the student version ships **starter code and expected
outputs, never complete solutions**. Complete worked solutions live in
[`instructor-solutions/`](instructor-solutions/README.md).

## Lab index

| Lab | Session | CLO | Topic | Difficulty |
|---|---|---|---|---|
| 01 | W1 S1 | 1 | What is data science & environment setup | Beginner |
| 02 | W1 S2 | 1 | Python refresher | Beginner |
| 03 | W2 S3 | 1 | Jupyter in depth | Beginner |
| 04 | W2 S4 | 1 | Git & GitHub workflow | Beginner |
| 05 | W3 S5 | 1 | NumPy I — arrays & operations | Beginner |
| 06 | W3 S6 | 1 | NumPy II — masks, aggregation, random | Beginner |
| 07 | W4 S7 | 1 | Pandas I — Series, DataFrame, selection | Beginner |
| 08 | W4 S8 | 1 | Pandas II — files, filtering, sorting | Beginner |
| 09 | W5 S9 | 1 | Data cleaning I — missing values, duplicates | Beginner |
| 10 | W5 S10 | 1 | Data cleaning II — strings, dates, outliers | Intermediate |
| 11 | W6 S11 | 1 | Data acquisition — APIs & caching | Intermediate |
| 12 | W6 S12 | 1 | Combining data — concat & merge | Intermediate |
| 13 | W7 S13 | 1 | Matplotlib — figures that communicate | Intermediate |
| 14 | W7 S14 | 1 | Seaborn — statistical plots | Intermediate |
| 15 | W8 S15 | 1 | EDA workflow — one full analysis | Intermediate |
| 16 | W8 S16 | 1 | Midterm review — cumulative practical | Intermediate |
| 17 | W9 S17 | 2 | Intro to ML — split, fit, baseline | Intermediate |
| 18 | W9 S18 | 2 | Linear regression & evaluation | Intermediate |
| 19 | W10 S19 | 2 | Classification I — k-NN, logistic regression | Intermediate |
| 20 | W10 S20 | 2 | Classification II — decision trees & overfitting | Intermediate |
| 21 | W11 S21 | 2 | Clustering — k-means & the elbow | Intermediate |
| 22 | W11 S22 | 2 | Pipelines & cross-validation | Intermediate |
| 23 | W12 S23 | 2 | Project kickoff — proposal workbook | Intermediate |
| 24 | W12 S24 | 3 | Reproducible workflows | Intermediate |
| 25 | W13 S25 | 3 | LLMs for data science | Advanced |
| 26 | W13 S26 | 3 | PandasAI — natural-language queries | Advanced |
| 27 | W14 S27 | 3 | Ollama — local models from Python | Advanced |
| 28 | W14 S28 | 3 | Tool calling & AI agents | Advanced |
| 29 | W15 S29 | 3 | n8n workflows & idempotency | Advanced |
| 30 | W15 S30 | 3 | Ethics & responsible AI | Advanced |
| 31 | W16 S31 | 3 | Project presentations — prep & peer review | Advanced |
| 32 | W16 S32 | 1+2+3 | Final submission & exam review | Advanced |

## Conventions

- One file per lab: `lab-NN-topic.md`. Solutions mirror them exactly in
  `instructor-solutions/`.
- Each lab contains: learning objectives, problem statement, dataset
  requirements, step-by-step tasks, starter code, expected output, questions,
  a challenge task, CLO mapping, and a marking rubric.
- Datasets are the course built-ins (seaborn/sklearn) or small
  reproducible DataFrames generated inline — no downloads needed.
- Labs 25–30 degrade gracefully: if Ollama/pandasai are unavailable, mock
  paths keep the lab completable.
- Submitted via Git before the start of the next session (see
  `../assessment-plan.md` for weights and policy).