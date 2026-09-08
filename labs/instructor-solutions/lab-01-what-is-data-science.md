# Lab 01 — Solution: Environment Setup

**Session:** W1 S1 · **CLO:** CLO-1

## Complete solution

```bash
# 1. versions (record ALL output)
python --version          # e.g. Python 3.12.x / 3.14.x
git --version             # e.g. git version 2.4x
jupyter --version         # prints the notebook server + kernels versions

# 2. virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. course stack (requirements.txt at repo root)
pip install -r requirements.txt
```

```python
# smoke_test.py — run inside the activated environment
import sys
import numpy as np
import pandas as pd

print("Python:", sys.version.split()[0])
print("NumPy:", np.__version__)
print("pandas:", pd.__version__)

numbers = [2, 4, 6, 8]
print("mean of", numbers, "=", np.mean(numbers))
```

```bash
# 4. GitHub repo
git init                      # if starting locally
git remote add origin <url>   # point at the GitHub repo
echo "# hello" > hello.md     # then edit hello.md with the lifecycle paragraph
git add hello.md
git commit -m "Add course hello with data science lifecycle overview"
git push -u origin main
```

## Expected output

```
Python: 3.12.x
NumPy: 2.x.y
pandas: 2.x.y
mean of [2, 4, 6, 8] = 5.0
```

## Model answers

1. **Lifecycle stages:** ask (problem → question) → get (acquire data) →
   clean/explore (wrangle, EDA) → model/analyze → communicate/act. Any
   standard 5-stage naming is acceptable if the ideas are present.
2. **Module map:** Module A = clean/explore (and get); Module B = model;
   Module C = AI-assisted versions of all stages + responsible use.
3. **Virtual environment:** isolates package versions per project, so
   different projects (or this course vs. another) don't break each other;
   reproducible installs via `requirements.txt`.
4. **git push:** uploads local commits to the remote (GitHub) so others can
   see/collaborate; GitHub adds backup, history, PRs, issues.
5. **False.** Jupyter is an *environment* (notebook interface + kernels);
   the language is Python.

## Challenge solution

```markdown
# versions.md
| Tool | Version | Date |
|---|---|---|
| Python | 3.12.x | 2026-09-08 |
| NumPy | 2.x.y | 2026-09-08 |
| pandas | 2.x.y | 2026-09-08 |
| Git | 2.4x | 2026-09-08 |
| Jupyter | (notebook version) | 2026-09-08 |
```

```bash
git add versions.md && git commit -m "Record machine baseline for reproducibility"
git push
```