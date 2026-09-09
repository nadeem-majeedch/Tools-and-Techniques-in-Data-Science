# Weekly Schedule

16 weeks × 2 sessions/week × 90 minutes. Sessions are numbered 1–32.
Module A: Weeks 1–8 (CLO-1) · Module B: Weeks 9–12 (CLO-2) · Module C: Weeks 13–16 (CLO-3).
Sessions 23–24 bridge the modules: the project kickoff spans all three CLOs
and reproducibility (W12 S24) is formally a CLO-3 skill, taught in Week 12 so
the final project can use it from the start. Streamlit has no dedicated
lecture slot — it is a self-paced module (`streamlit/`) started in Week 9
with Assignment 2 and practised through Sessions 28 and 30.

## Key dates

| Event | Session | Date (fill in) |
|---|---|---|
| Quiz 1 (Weeks 1–7: Python → visualization) | 15 | |
| Assignment 1 due | 15 | |
| Midterm exam | 16 | |
| Quiz 2 (Weeks 8–14: EDA → AI agents) | 29 | |
| Assignment 2 released | 17 | |
| Final project kickoff | 23 | |
| Project proposal due | 26 | |
| Assignment 2 due | 30 | |
| Final project presentations | 31–32 | |
| Final exam | 32 | |

## Module A — Data handling & EDA (CLO-1)

| Week | Session | Topic | Activities / deliverables |
|---|---|---|---|
| 1 | 1 | Course orientation; what is data science; the data science lifecycle; roles and tools | Syllabus walk-through; setup checklist |
| 1 | 2 | Python refresher: types, control flow, functions, comprehensions; first Jupyter notebook | Notebook: `course-notebooks/01-python-for-data-science.ipynb` |
| 2 | 3 | Jupyter in depth: cells, markdown, kernels, magic commands, notebook hygiene | Notebook exercise; run-all check |
| 2 | 4 | Git & GitHub: init/clone, add/commit/push, branches, pull requests | Set up personal repo; first commit |
| 3 | 5 | NumPy I: `ndarray`, creation, indexing, slicing, dtypes | In-class exercises |
| 3 | 6 | NumPy II: universal functions, broadcasting, aggregation, `np.random` | **Lab 06 due** (NumPy II) |
| 4 | 7 | Pandas I: Series & DataFrame, construction, attributes, `loc`/`iloc` | In-class exercises |
| 4 | 8 | Pandas II: reading/writing CSV, Excel, JSON; filtering and sorting | In-class exercises |
| 5 | 9 | Data cleaning I: missing values, duplicates, dtype conversion | In-class exercises |
| 5 | 10 | Data cleaning II: string methods, `apply`/`map`, renaming, `melt`/`pivot` | **Lab 10 due** (cleaning II) |
| 6 | 11 | Data acquisition: local files, public APIs with `requests`, scraping ethics | Notebook: API exercise |
| 6 | 12 | Combining data: `concat`, `merge`, `join`; relational thinking | **Lab 12 due**; **Assignment 1 released** |
| 7 | 13 | Matplotlib: line, bar, scatter, histogram; figures/axes; saving figures | In-class exercises |
| 7 | 14 | Seaborn: statistical plots, `pairplot`, heatmaps; visualization principles | **Lab 14 due** (seaborn) |
| 8 | 15 | EDA workflow: summary stats, distributions, correlations; EDA case study | **Quiz 1** at session start (Weeks 1–7); **Assignment 1 due**; EDA case study (penguins) |
| 8 | 16 | **Midterm exam** (written + practical notebook task on CLO-1) | Exam session |

## Module B — Machine learning basics (CLO-2)

| Week | Session | Topic | Activities / deliverables |
|---|---|---|---|
| 9 | 17 | Intro to ML; supervised vs. unsupervised; scikit-learn overview; train/test split | **Assignment 2 released** (API + Streamlit app, due W15 S30); start the self-paced Streamlit module (`streamlit/`); Notebook: first model |
| 9 | 18 | Linear regression; metrics (MSE, R²) | **Lab 18 due** (regression) |
| 10 | 19 | Classification I: k-NN and logistic regression; confusion matrix, precision/recall | In-class exercises |
| 10 | 20 | Classification II: decision trees; overfitting; basic hyperparameter tuning | **Lab 20 due** (classification II) |
| 11 | 21 | Unsupervised learning: k-means; elbow method; feature scaling | In-class exercises |
| 11 | 22 | Pipelines & cross-validation; choosing the right model | **Lab 22 due** (pipelines & CV) |
| 12 | 23 | Final project kickoff: problem framing, project brief, data selection | **Project released** |
| 12 | 24 | Reproducible workflows: virtual environments, `requirements.txt`, random seeds, project structure | Project workshop time |

## Module C — AI-assisted workflows (CLO-3)

| Week | Session | Topic | Activities / deliverables |
|---|---|---|---|
| 13 | 25 | LLMs for data science: what they are, prompting for analysis, when (not) to use them | In-class exercises |
| 13 | 26 | PandasAI: natural-language queries on DataFrames; limitations and reproducibility | **Lab 26 due**; **Project proposal due** |
| 14 | 27 | Ollama: install, pull models, chat from Python; local vs. cloud models | **Lab 27 due** (Ollama) |
| 14 | 28 | Simple AI agents: tool calling, agent loops; automating a data-analysis subtask | Build day: Assignment 2 app + project |
| 15 | 29 | n8n: visual workflows; automating data collection/processing | **Quiz 2** at session start (Weeks 8–14); In-class build |
| 15 | 30 | Ethics & responsible AI: bias, privacy, provenance, transparency; documenting AI-assisted work | **Lab 30 due**; **Assignment 2 due** (API + Streamlit app) |
| 16 | 31 | Final project presentations (part 1); peer feedback | Presentations |
| 16 | 32 | Final project presentations (part 2); course wrap-up; **final exam** | **Final exam**; project final submission |

## Deliverable summary

| Deliverable | Type | Released | Due | CLO |
|---|---|---|---|---|
| Labs 1–32 | Weekly labs | each week | next session after release | 1, 2, 3 |
| Quiz 1, 2 | In-class, ~25 min | session start | same session | 1, 2, 3 |
| Assignment 1 — Data cleaning & EDA | Individual | W6 S12 | W8 S15 | CLO-1 |
| Assignment 2 — API + Streamlit data app | Individual | W9 S17 | W15 S30 | CLO-1, CLO-3 |
| Midterm exam | Exam | — | W8 S16 | CLO-1, CLO-2 |
| Final exam | Exam | — | W16 S32 | CLO-1, CLO-2, CLO-3 |
| Final project | Team (2–3) | W12 S23 | W16 S31/32 | CLO-1, CLO-2, CLO-3 |