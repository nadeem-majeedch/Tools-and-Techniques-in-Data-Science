# Session 16 — Midterm Exam (CLO-1)

**Week 8 · Session 16 · Module A · 90 min · CLO-1 (+ light CLO-2 preview)**

## 1. Learning objectives

By the end of this session, students demonstrate they can:
- Complete the full CLO-1 workflow independently: acquire → clean → manipulate → visualize → explore.
- Write correct Pandas/NumPy/Matplotlib code under exam conditions.
- Explain concepts (why, not just how) in short written answers.
- Structure answers so a grader can follow the reasoning without running the code.

## 2. Key concepts (review list)

- Data science lifecycle and where each tool fits (S1).
- Python basics: types, control flow, functions, comprehensions, file reading (S2).
- Notebook hygiene and Git submission mechanics (S3–S4).
- NumPy: arrays, slicing, masks, broadcasting, aggregation, seeds (S5–S6).
- Pandas: Series/DataFrame, `loc`/`iloc`, I/O, filtering, `groupby`, `value_counts` (S7–S8).
- Cleaning: missing values (drop vs. fill *and why*), duplicates, dtypes, strings, `apply`/`map`, `melt`/`pivot` (S9–S10).
- Acquisition & combining: `requests` + JSON, `concat` vs. `merge`, join types (S11–S12).
- Visualization & EDA: figure/axes, four chart types, `hue`, boxplots, heatmaps, correlation, the EDA recipe (S13–S15).

## 3. Detailed lecture notes

**Session format (90 min):**
- **0–10 min:** seating, login, open the exam notebook; rules recap (below).
- **10–70 min:** written section (25–30 min) followed by the practical notebook task (30–35 min).
- **70–80 min:** optional extension task for early finishers.
- **80–90 min:** submit: save notebook, push to the exam branch, confirm the commit hash.

**Structure of the exam** (as specified in `../assessment-plan.md`):
- **Part A — Written (≈30 marks):** 15–20 short questions: definitions,
  code-reading ("what does this output?"), code-writing (one-liners), and
  explain-why items (e.g., "why fill with the group median rather than drop?").
- **Part B — Practical notebook (≈70 marks):** a small dataset (e.g., `penguins`
  or a CSV provided with the exam) and a task list: load → inspect → clean
  (with justification) → reshape/derive a column → filter/sort → 3 charts →
  2 written findings with evidence. Graded on correctness *and* on the
  markdown justifications.

**Advice to repeat (write on the board):**
- Read the whole exam before starting; budget time: practical task ≈ 60% of marks.
- Answer the explain-why questions even if short — partial credit exists.
- In the notebook: one finding per markdown cell, with the printed evidence below it.
- `Kernel → Restart & Run All` before submitting — stale output loses marks.
- Don't over-clean: justify every `dropna`/`fillna` choice in one sentence.

**Rules (from `../assessment-plan.md`):** closed-notes for Part A; the practical
part allows the official docs (pandas/NumPy/Matplotlib reference) but **not**
saved notebooks or AI assistants (this is a CLO-1 assessment of individual skill;
CLO-3's AI tools are assessed separately in Sessions 25–30 and the project).

## 4. Important terminology

Review vocabulary likely to appear: dataset/observation/feature · EDA · lifecycle
· dtype · broadcasting · boolean mask · view vs copy · `loc` vs `iloc` ·
split-apply-combine · NaN/MCAR vs MNAR · imputation · tidy data / long vs wide ·
`melt` · API · status code · inner vs left join · key · figure vs axes ·
histogram vs boxplot · correlation vs causation · finding–evidence–implication ·
seed.

## 5. Python examples (sample-style questions)

```python
# --- Code-reading: what prints? ---
import numpy as np
a = np.arange(6).reshape(2, 3)
print(a[:, 1])            # column 1 -> [1 4]

# --- Code-writing: one line, filter + select ---
# Given df (columns: name, score), keep rows with score >= 60, only 'name'.
# Answer: df.loc[df["score"] >= 60, "name"]

# --- Explain-why: ---
# "Why set np.random.seed(42) before generating data in an analysis?"
# Answer: reproducibility — same seed yields the same sequence, so the
# analysis can be re-run and verified.

# --- Practical-flavored task skeleton ---
import pandas as pd
import seaborn as sns
df = sns.load_dataset("penguins")
print(df.isna().sum())
# then: justify, clean, groupby, plot, find.
```

## 6. Beginner example

```python
# The minimal "everything works" exam check — run FIRST, in the exam notebook:
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
print("stack OK:", np.array([1, 2]).mean() == 1.5)
print("pandas OK:", pd.Series([1, 2]).sum() == 3)
```

## 7. Practical Data Science example

A practice run of the practical task, on `flights` (so students see the shape
before the real exam):

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

df = sns.load_dataset("flights")
print(df.info(), df.isna().sum().sum())          # 1. inspect
yearly = df.groupby("year")["passengers"].sum()  # 2. manipulate
print(yearly)                                     # 3. summarize
sns.lineplot(data=df, x="year", y="passengers", hue="month")  # 4. visualize
plt.title("Passengers over time by month")
# 5. finding: "Air travel grew steadily; summer months are consistently busiest."
```

## 8. In-class activity

The exam *is* the activity this session (per the format in section 3). After
submission, the last 10 minutes are a brief **after-action review**: one thing
that surprised you, one skill to re-practice — shared anonymously via a quick
poll or sticky notes.

## 9. Lab exercise

No lab this session. Students who finished early may use remaining time to
commit the week's work. Labs resume with **Lab 5** (regression, due Session 18).

## 10. Common mistakes (exam-specific)

- Spending 40 minutes on Part A and rushing the 70-mark practical.
- Submitting without **Restart & Run All** → stale outputs and hidden errors.
- `dropna()` everywhere without justification → lost marks on the explain-why criterion.
- Plotting without labels → charts that can't be interpreted.
- Writing findings without evidence ("tips are higher" — where's the number/chart?).
- Forgetting `index=False` when exporting; forgetting `.head()` when inspecting.
- Not reading the whole paper first.

## 11. Short assessment questions

Five-minute self-test before the exam (answers in `../quizzes/` style):

1. Write one line: rows where `day == "Sun"`, columns `tip` only.
2. `df.groupby("day")["tip"].mean()` — what is the result's *index*?
3. Why is `fillna(0)` wrong for a temperature column?
4. Which join keeps all rows of the left table?
5. What does a boxplot's whisker-length tell you? (Roughly: typical spread; points beyond are outliers.)

## 12. CLO mapping

The midterm assesses **CLO-1** (all of it) and gives a light preview of CLO-2
(reading correlation/patterns that modeling will exploit). CLO-3 is assessed
separately in Module C per the assessment plan.

## 13. Suggested homework

- Rest and review the midterm feedback when returned (within one week).
- Read: skim Session 17's objectives — machine learning begins next session; the only prerequisite is what you just demonstrated.
- Optional: fix and re-commit any exam-notebook errors for practice (not for re-grading).