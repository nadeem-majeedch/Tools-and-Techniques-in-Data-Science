# Course Learning Outcomes (CLOs)

The three CLOs below are the official outcomes of this course. This document
expands each CLO into the cognitive level, covered topics, and assessment
methods used to verify it.

## CLO definitions

| # | CLO | Cognitive level* |
|---|---|---|
| CLO-1 | Apply Python and standard data science libraries to acquire, clean, manipulate, visualize and explore datasets. | Apply |
| CLO-2 | Apply appropriate data science tools and basic machine learning techniques to solve introductory data-driven problems. | Apply / Analyze |
| CLO-3 | Develop simple AI-assisted data science workflows using LLMs, local models, automation tools and basic AI agents while considering reproducibility, ethics and responsible AI use. | Apply / Create |

\* Based on Bloom's revised taxonomy.

## CLO-1 — Data handling with Python

**What students can do:** work end-to-end with tabular and structured data —
read data from files and APIs, clean and reshape it, and explore it with summary
statistics and visualizations.

**Enabling topics:** Python fundamentals; Jupyter notebooks; Git/GitHub; NumPy
arrays and operations; Pandas Series/DataFrames, I/O, indexing, filtering;
missing values, duplicates, dtype conversion; string operations, `apply`/`map`,
`melt`/`pivot`; `concat`/`merge`/`join`; Matplotlib and Seaborn plotting; EDA
workflow (distributions, correlations, grouping).

**Assessed by:** Labs 1–16, Quiz 1, Assignments 1–2, Midterm exam (practical
notebook task), Final exam (reproducibility items), Final project (data
acquisition, cleaning, and EDA components).

## CLO-2 — Tools and basic machine learning

**What students can do:** frame a simple data-driven problem, choose an
appropriate basic model, train and evaluate it, and interpret the results.

**Enabling topics:** supervised vs. unsupervised learning; train/test split;
linear regression (MSE, R²); classification with k-NN, logistic regression, and
decision trees (confusion matrix, precision, recall, accuracy); k-means
clustering (elbow method, feature scaling); cross-validation and scikit-learn
pipelines.

**Assessed by:** Labs 17–22, Quiz 2, Midterm exam (entry-level
item), Final exam, Final project (modeling component).

## CLO-3 — AI-assisted data science workflows

**What students can do:** use LLM-based tools (PandasAI, Ollama local models,
simple AI agents) and automation (n8n) to accelerate data tasks, and critically
reflect on reproducibility, ethics, and responsible AI use — including when **not**
to rely on AI output.

**Enabling topics:** LLM basics and prompting for data analysis; PandasAI
natural-language queries; Ollama installation and local model inference;
tool-calling and simple agent loops; n8n workflow automation; reproducibility
(seeds, environments, version control, documenting AI-assisted steps); bias,
privacy, data provenance, and transparency.

**Assessed by:** Labs 24–32, Quiz 2, Assignment 2 (reproducibility,
documentation, responsible data use), Final exam, Final project (AI-assisted
component + ethics/reproducibility reflection).

## CLO coverage matrix

| Assessment | CLO-1 | CLO-2 | CLO-3 |
|---|---|---|---|
| Labs 1–16 | ✓ | | |
| Labs 17–22 | | ✓ | |
| Labs 24–32 | | | ✓ |
| Quiz 1 | ✓ | | |
| Quiz 2 | | ✓ | ✓ |
| Assignment 1 | ✓ | | |
| Assignment 2 | ✓ | | ✓ |
| Midterm exam | ✓ | ✓ | |
| Final exam | ✓ | ✓ | ✓ |
| Final project | ✓ | ✓ | ✓ |

## Alignment note

The CLOs are fixed course requirements. Program-level alignment (e.g., mapping to
BS Data Science program outcomes) is maintained by the program coordinator and is
outside the scope of this repository.