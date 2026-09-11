# Course Notebooks

Twenty complete, **executed** Jupyter notebooks — one per major course topic.
Each notebook contains markdown theory, learning objectives, explanation
before code, beginner → intermediate examples, exercises, a challenge
exercise, a recap, and review questions. Every code cell was executed and
verified end-to-end (see *How these were verified* below).

| # | Notebook | Module | Key tools |
|---|---|---|---|
| 01 | Python for Data Science | A | core Python |
| 02 | NumPy | A | numpy |
| 03 | Pandas | A | pandas |
| 04 | Data Cleaning | A | pandas |
| 05 | Data Aggregation | A | pandas (groupby/merge) |
| 06 | Data Visualization | A | matplotlib, seaborn |
| 07 | EDA | A | pandas, seaborn |
| 08 | Git/GitHub Workflow | A | git (run inside the notebook) |
| 09 | APIs and Data Acquisition | A | requests, JSON |
| 10 | Introduction to ML | B | scikit-learn |
| 11 | Regression | B | scikit-learn |
| 12 | Classification | B | scikit-learn |
| 13 | Clustering | B | scikit-learn |
| 14 | PandasAI | C | pandasai (guarded) |
| 15 | LLM Fundamentals | C | prompt patterns (guarded) |
| 16 | Ollama with Python | C | ollama (guarded) |
| 17 | Tool/Function Calling | C | ollama + schemas (guarded) |
| 18 | AI Agents | C | agent loop (guarded) |
| 19 | n8n Workflows | C | workflow-in-Python pattern |
| 20 | End-to-End Data Science Project | A+B+C | full pipeline |

## How to use

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows
# or: source .venv/bin/pip install -r requirements.txt   (macOS/Linux)
.venv/Scripts/jupyter lab course-notebooks/01-python-for-data-science.ipynb
```

Run notebooks **in order** — later notebooks reuse patterns from earlier ones.

## Guards and degraded modes

Notebooks 14–18 depend on optional, LLM-related software that may not be
installed or running on a given machine:

- **pandasai (14):** installed separately; on Python 3.14 it does not build.
  Cells import it inside a guard and print a message instead of failing.
- **Ollama (16–18):** requires the Ollama app running with a model pulled
  (`ollama pull llama3.2`). Guarded cells degrade gracefully, and the
  **mock/simulation paths always run**, so the notebooks teach the full
  workflow with or without a model.
- **Notebook 09 & 19** call the keyless Open-Meteo weather API; cells cache
  results in `datasets/` so reruns work offline.

Anything a notebook saves (CSVs, figures, JSON) goes into a `datasets/`
folder created next to the notebook on first run. That folder is
git-ignored.

## How these were verified

`scripts/build_course_notebooks.py` generates the `.ipynb` files from
readable source modules in `scripts/notebook_src/`. `scripts/execute_notebooks.py`
executes every notebook with a real kernel and writes outputs back into the
files. Current status: **20/20 notebooks execute without errors** on
Python 3.14 with the pinned `requirements.txt` stack.

To rebuild or re-verify after editing a source module:

```bash
.venv/Scripts/python scripts/build_course_notebooks.py
.venv/Scripts/python scripts/execute_notebooks.py
```

## Continuous integration & read-only checking

GitHub Actions runs the same validation on every push and pull request that
touches the notebooks (`.github/workflows/notebooks.yml`). CI executes all
20 notebooks with a real kernel and fails if any cell raises an error.

Two properties matter:

- **Notebooks are never modified by CI.** `scripts/check_notebooks.py`
  executes each notebook *in memory* and discards the outputs, so the
  `.ipynb` files on disk are untouched (the workflow double-checks this with
  `git diff`).
- **No optional services are required.** The Ollama daemon is not installed
  in CI; notebooks 14–18 detect that and run their mock/simulation paths.
  No API keys or paid services are used anywhere.

To run the same check locally before pushing (nothing is modified):

```bash
.venv/Scripts/python -m pip install -r requirements.txt nbclient nbformat
.venv/Scripts/python scripts/check_notebooks.py          # all notebooks
.venv/Scripts/python scripts/check_notebooks.py 03 12    # a subset
```

Use `scripts/execute_notebooks.py` instead **only** when you intentionally
want to re-execute and save outputs back into the delivered files.

*Instructor note:* exercise cells ship with `# your code here` placeholders
followed by worked solutions — delete the solution cells before distributing
if you want the exercises unsolved.