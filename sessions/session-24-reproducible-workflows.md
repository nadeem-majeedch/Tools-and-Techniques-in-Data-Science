# Session 24 — Reproducible Workflows

**Week 12 · Session 24 · Module B → C · 90 min · CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Explain why reproducibility is a scientific and professional requirement.
- Structure a project folder so someone else can run it (layout, README, requirements).
- Use virtual environments, `requirements.txt`, and random seeds correctly.
- Write a short "how to reproduce" README section.
- Apply a reproducibility checklist to their own project.

## 2. Key concepts

- **Reproducibility = someone else (or future-you) can re-run your analysis and get the same results.**
- The enemy is **silent context**: versions, seeds, cwd, hidden state, manual steps.
- Three pillars: **environment** (Python + package versions), **seeds** (randomness), **process** (documented steps in order).
- A project folder is a *product*: README, data, notebooks, results, requirements — each with a place.
- Version control (Session 4) is the historical backbone; reproducibility is the operational guarantee.
- AI tools (Module C) make documentation *more* important, not less: prompts and AI-assisted steps must be recorded.

## 3. Detailed lecture notes

**Why this session?** Modules A and B taught *how* to analyze; this session
teaches how to make the analysis *trustworthy*. The nightmare scenario: you
finish the project, the grader (or your boss, or your collaborator) tries to
re-run it, and it crashes — wrong package version, missing seed, notebook
executed out of order, absolute path. Every minute of good analysis is lost.
Reproducibility is what turns a notebook into evidence. This is the first
explicit CLO-3 session; the theme deepens with AI tools in Sessions 25–30.

**Pillar 1 — Environment.** Your analysis depends on exact package versions:
`pandas 2.1` behaves differently from `pandas 1.3`. Capture it:
- Always work in a virtual environment (Session 1's setup).
- `pip freeze > requirements.txt` (or maintain `requirements.txt` by hand) records versions.
- Better practice: `pip freeze` after each major milestone so the file tracks reality.
Rule: **if it runs only on your machine, it doesn't run at all.** A fresh
`python -m venv` + `pip install -r requirements.txt` must reproduce your
notebook. (Pin exact versions for the project; the course's `requirements.txt`
uses loose pins, which is fine for teaching.)

**Pillar 2 — Seeds.** Randomness lurks everywhere: `train_test_split`,
`KMeans` initialization, any `np.random` call. Without a fixed seed, every
rerun gives different numbers — and different "results". The habit (Sessions
6, 17): `random_state=42` on every random operation, `np.random.seed(...)`
at the top of notebooks. Note: scikit-learn also accepts `random_state` in the
model *and* in the split — set both. In the project README, state the seeds
used.

**Pillar 3 — Process.** A reproducible analysis is a *documented sequence*:
1. **One entry point:** "run this notebook from top to bottom" — order visible, `Restart & Run All` passes.
2. **Relative paths only:** notebooks reference `datasets/...`, never `C:\Users\me\...`.
3. **No hidden manual steps:** if you edited a CSV by hand, say so; better, script it.
4. **Cached acquisitions:** API fetches are cached (Session 11), so reruns don't depend on the network.
5. **README with "How to reproduce":** clone → create venv → install → run notebooks (in order) → expected outputs.
The "how to reproduce" section is graded in the project rubric (10%:
reproducibility & ethics).

**Project folder layout** (put on the board; it's the recommended layout for
the final project):

```
project-name/
├── README.md            # question, how to reproduce, findings summary
├── requirements.txt     # exact versions
├── data/                # raw/ and cleaned/ subfolders (or link to source)
├── notebooks/           # 01-clean.ipynb, 02-eda.ipynb, 03-model.ipynb
├── scripts/             # any reusable helpers (.py)
├── figures/             # saved charts for the report
└── report/              # findings write-up / reflection
```

Numbered notebooks = execution order. `data/raw` untouched, `data/cleaned`
produced by the cleaning notebook — provenance visible.

**Reproducibility with AI tools (preview).** Module C's assistants make work
faster but *opaque*: a PandasAI answer or a model-generated snippet is only
reproducible if the prompt, model, and version are recorded. The rule we adopt:
**every AI-assisted step is documented** (tool, prompt, output, verification) —
details in Sessions 26 and 30. This is the CLO-3 twist on reproducibility:
reproducibility now includes *how the AI was used*.

## 4. Important terminology

- **Reproducibility** — same inputs + same process → same outputs.
- **Environment** — Python version + installed packages (captured in `requirements.txt`).
- **Virtual environment** — isolated package set per project.
- **Seed** — fixed randomness starting point; `random_state` in scikit-learn.
- **`pip freeze`** — dump installed package versions.
- **Relative path** — path relative to the repo root (portable).
- **Entry point** — the notebook/script to start from.
- **Provenance** — documented origin of data and derived files.
- **Raw vs. cleaned data** — never edit raw; cleaning scripts produce cleaned.
- **"How to reproduce" section** — the README contract for re-running your work.

## 5. Python examples

```python
# --- Environment: capture it ---
# terminal:  pip freeze > requirements.txt

# --- Seeds: make randomness reproducible ---
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

np.random.seed(42)                      # numpy-level randomness
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)   # split-level
# and every model: KMeans(random_state=42), DecisionTreeClassifier(random_state=42)...
```

```python
# --- A self-contained notebook header (copy-paste template) ---
"""
PROJECT: tips analysis
AUTHOR:  Ayesha Khan
DATE:    2026-04-10
PURPOSE: predict tips; reproduce with: venv + requirements.txt + run all
RUN:     Kernel -> Restart & Run All
"""
import numpy as np, pandas as pd, seaborn as sns
np.random.seed(42)
```

## 6. Beginner example

```python
# The reproducibility promise, in one comment block:
# 1. python -m venv .venv
# 2. pip install -r requirements.txt
# 3. jupyter lab  ->  open notebooks/01-clean.ipynb  ->  Run All
# Result: identical numbers every time.
```

## 7. Practical Data Science example

Restructure a messy one-folder project into the recommended layout (live demo on
a volunteer's repo or a sample):

```bash
# Before: everything in one folder, absolute paths, no requirements
# After:
project-name/
├── README.md
├── requirements.txt
├── data/raw/tips.csv
├── notebooks/
│   ├── 01-clean.ipynb      # raw -> data/cleaned/tips_clean.csv
│   ├── 02-eda.ipynb        # figures/*.png, findings in markdown
│   └── 03-model.ipynb      # seeds set, CV reported, test evaluated once
├── figures/
└── report/reflection.md
```

`README.md` "How to reproduce" (template):
```markdown
## How to reproduce
1. `python -m venv .venv` then activate it.
2. `pip install -r requirements.txt`
3. Run `notebooks/01-clean.ipynb`, then `02-eda.ipynb`, then `03-model.ipynb`
   (Kernel → Restart & Run All). Seeds: 42 everywhere.
4. Expected: figures in `figures/`, summary table printed in `03-model.ipynb`.
```

## 8. In-class activity (50 min)

1. **Break it (15 min):** take the tips model notebook; deliberately (a) remove
   `random_state`, (b) change cwd so a relative path breaks, (c) run cells out of
   order. Observe each failure mode; then fix all three.
2. **Freeze & verify (15 min):** run `pip freeze > requirements.txt` in your
   project; on a partner's machine (or a fresh venv if time), install and run —
   note what broke and why (this is the real lesson).
3. **Layout sprint (20 min):** restructure your own project folder into the
   recommended layout; move notebooks, add `requirements.txt` and a
   "How to reproduce" README section. Commit.

## 9. Lab exercise

No lab — this is a **project workshop** session. Milestone: your project repo
now has the reproducible layout, seeds set in every notebook, and a
"How to reproduce" README draft. Assignment 2 remains due Session 25.

## 10. Common mistakes

- No `requirements.txt` (or one that doesn't match reality — update after every install).
- Forgetting `random_state` in *one* of several random operations → partially reproducible.
- Absolute paths that work only on your machine.
- Editing `data/raw` files by hand — provenance is destroyed.
- "It works on my machine" — the classic; the fix is a fresh-venv verification.
- Notebooks with cells run out of order (Run All fails or changes results).
- Believing reproducibility ends at code — AI prompts and manual steps must be documented too (Module C).

## 11. Short assessment questions

1. Name the three pillars of reproducibility.
2. What does `pip freeze > requirements.txt` capture, and why pin versions?
3. Why must `random_state` be set in both the split *and* the model?
4. What is wrong with a notebook containing `C:\Users\Ayesha\datasets\tips.csv`?
5. What belongs in a "How to reproduce" section?
6. Why should `data/raw` never be edited directly?

## 12. CLO mapping

CLO-3: reproducibility is one of the two explicit requirements of CLO-3's
workflow development ("considering reproducibility, ethics and responsible AI
use"). This session supplies the mechanics; Sessions 25–30 apply them to
AI-assisted workflows, and Session 30 adds the ethics half.

## 13. Suggested homework

- Finish the project layout + "How to reproduce" and commit.
- Practice: hand your repo link to a classmate; they must get it running from scratch in under 15 minutes. Fix what breaks.
- Read: The Turing Way, "Guide for Reproducible Research" — the "reproducibility" intro chapter (free online).
- Preview: Session 25 introduces LLMs for data science — bring the question "where can AI genuinely help my project, and where shouldn't it?"