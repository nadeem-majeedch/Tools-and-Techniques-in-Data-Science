# Lab 24 — Solution: Reproducible Workflows

**Session:** W12 S24 · **CLO:** CLO-3

## Complete solution

```bash
# 1. freeze + header
pip freeze > requirements.txt
# edit requirements.txt: add first line "# Python 3.14 (venv used for build)"

# 4. fresh environment test
python -m venv .venv-repro
.venv-repro\Scripts\pip install -r requirements.txt    # Windows
# or: .venv-repro/bin/pip install -r requirements.txt  # macOS/Linux
.venv-repro\Scripts\jupyter lab eda.ipynb              # Restart & Run All
```

```python
# cell 1 of every notebook — SEED defined once, used everywhere
SEED = 42
import numpy as np
import pandas as pd
np.random.seed(SEED)
```

```python
# seed audit — every randomized call, before:
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# after:
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED)

# KMeans(...)          -> KMeans(..., random_state=SEED, n_init=10)
# DecisionTreeClassifier(...) -> DecisionTreeClassifier(..., random_state=SEED)
```

Folder layout target:

```
projects/final/
  README.md          # proposal + how to run + headline metric
  requirements.txt
  data/              # or data_loader.py
  eda.ipynb
  models.ipynb
  HOW_TO_RUN.md
```

Checklist (self-grade): seed everywhere ✓, requirements pinned ✓, data
loads via loader/cache ✓, top-to-bottom run ✓, outputs versioned ✓,
README with run instructions ✓.

## Model answers

1. **Exact pins** — `numpy==2.0.1` reproduces the exact environment;
   `>=` allows future versions that may change behavior (APIs, defaults,
   results), breaking reproducibility.
2. **Hidden nondeterminism** — parallel training (n_jobs), dict/set
   iteration order, floating-point summation order, time/date-based
   features, and sklearn estimators without `random_state` (e.g., some
   splitting defaults, bagging).
3. **Seed at top** — it must execute *before* any random call; a seed set
   mid-notebook is too late and easy to miss; one constant at the top is
   auditable at a glance.
4. **Reproducibility ≠ correctness** — a pipeline can deterministically
   produce a wrong answer (bug, leakage, bad data). Reproducible means "same
   input → same output," not "output is true."
5. **Loader function/file** — keeps the source, license, and caching in
   one place; notebooks stay short; changing the data source doesn't
   require editing every notebook that loads it.

## Challenge solution

```python
# data_loader.py
"""Load the course project dataset.

Source : seaborn built-in "penguins" (Palmer Penguins, CC0)
License: public domain; see https://github.com/allisonhorst/penguins
Cache  : datasets/penguins.csv (created on first call)
"""
from pathlib import Path
import pandas as pd
import seaborn as sns

_CACHE = Path("datasets/penguins.csv")

def load_data(refresh: bool = False) -> pd.DataFrame:
    """Return the penguins DataFrame (cached locally after first call)."""
    if _CACHE.exists() and not refresh:
        return pd.read_csv(_CACHE)
    df = sns.load_dataset("penguins")
    _CACHE.parent.mkdir(exist_ok=True)
    df.to_csv(_CACHE, index=False)
    return df
```

```python
# in the notebook:
from data_loader import load_data
penguins = load_data()
```

Commit everything: `git add -A && git commit -m "Make project reproducible: pins, seeds, loader"`.