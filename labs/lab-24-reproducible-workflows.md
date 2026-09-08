# Lab 24 — Reproducible Workflows

**Session:** Week 12 · Session 24 · 90 min
**CLO:** CLO-3
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Pin dependencies with a `requirements.txt` and reproduce an environment.
2. Control randomness with seeds everywhere it matters.
3. Structure a project folder so someone else can run it.
4. Audit a notebook for reproducibility holes.

## Problem statement

"Works on my machine" is the enemy. You will take the EDA/model notebook
from your Lab 23 repo and make it **runnable by a stranger**: pinned
requirements, seeded randomness, a documented folder layout, and a written
reproducibility checklist. Then you will *prove* it by running your own
notebook from a fresh kernel (Restart & Run All) after "losing" the venv.

## Dataset requirements

Your own project dataset from Lab 23 (or penguins as fallback).

## Step-by-step tasks

1. **Freeze requirements:** in your project folder run
   `pip freeze > requirements.txt`. Inspect it: it will contain transitive
   deps — that is fine, but add a comment header naming the Python version
   you used (edit the file to add `# Python 3.14` etc. as the first line).
2. **Seed audit:** open your notebook. Find every place randomness appears:
   `train_test_split`, `KMeans`, `DecisionTreeClassifier`,
   `np.random.*`. Add `random_state=42` (or a `SEED = 42` constant defined
   once at the top) to each. If you use `np.random`, call
   `np.random.seed(SEED)` at the top of the notebook.
3. **Two-run test:** run the notebook twice (Restart & Run All). All
   printed numbers that should be deterministic **must be identical**.
   Record any that aren't, and fix them.
4. **Fresh environment test:** create a *second* venv
   (`.venv-repro`), install `-r requirements.txt`, and run the notebook
   with that kernel. It must work (allow 5–10 minutes for installs).
5. **Folder layout:** confirm your project folder has at least:
   ```
   projects/final/
     README.md          # proposal + how to run
     requirements.txt
     data/              # or data_loader.py
     eda.ipynb
     models.ipynb
   ```
   Add a `HOW_TO_RUN.md` with exactly three commands.
6. **Checklist (markdown):** write a 6-item reproducibility checklist
   (seed, requirements, data loader, order-of-cells, versioned outputs,
   README) and self-grade each item ✓/✗.

## Starter code

```markdown
# HOW_TO_RUN.md
1. python -m venv .venv
2. .venv/bin/pip install -r requirements.txt   (or .venv\Scripts\pip on Windows)
3. .venv/bin/jupyter lab eda.ipynb             (then: Kernel -> Restart & Run All)
```

```python
# put this at the top of your notebook (cell 1)
SEED = 42
import numpy as np
np.random.seed(SEED)
```

## Expected output

- `requirements.txt` with a `# Python` version header, committed.
- Notebook with `SEED` used in every randomized call — verified by search
  (`random_state` appears ≥ 3 times or `SEED` is threaded through).
- Two consecutive Restart & Run All runs produce identical key numbers.
- `.venv-repro` install + run succeeds (document the run).
- `HOW_TO_RUN.md` committed; folder layout matches the tree.
- Checklist with all 6 items self-graded.

## Questions

1. Why pin exact versions (`numpy==2.0.1`) instead of `numpy>=2.0`?
2. Where else can nondeterminism hide besides random seeds? (Think: model
   training order, dict iteration, time-based features.)
3. Why does the seed belong at the *top* of the notebook?
4. What is the difference between reproducibility and correctness? Can a
   run be reproducible and wrong?
5. Why keep data loading in a function/file instead of pasting the URL in a
   notebook cell?

## Challenge task

Write a tiny `data_loader.py` for your project dataset: a function
`load_data()` that returns the DataFrame, with a docstring stating source,
license, and cache location (see Lab 11's caching pattern). Import and call
it from your notebook (replace the inline load). Commit and push everything
from this lab.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| requirements.txt + version header | 3 | committed |
| Seed audit complete | 5 | every random call seeded |
| Two-run determinism test | 4 | identical key numbers |
| Fresh venv run succeeds | 4 | documented |
| Folder layout + HOW_TO_RUN | 3 | matches tree |
| Checklist self-graded | 3 | 6 items |
| Answers to questions | 3 | Q1, Q2, Q4 correct |
| Challenge: data_loader.py | 5 | function + docstring + used |
| **Total** | **30** | |