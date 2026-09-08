# Quiz 1 — Weeks 1–7 (Sessions 1–14)

**Administered:** W8 S15, session start · **Time:** ~25 minutes · **Closed notes**
**Covers:** Python refresher, Jupyter, Git/GitHub, NumPy, Pandas, data cleaning,
data acquisition & combining, Matplotlib/Seaborn visualization.
**CLOs:** CLO-1 (all questions), a subset tagged CLO-3 (Git/reproducibility).

Every question carries three tags: **CLO**, **Bloom's level** (revised
taxonomy), and **difficulty** (Easy / Medium / Hard). The answer key is
embedded — remove the `**Answer:**` lines to produce a student paper.

---

## A. Python & Jupyter

**Q1.1 (MCQ).** Which statement about Python lists vs. tuples is correct?
a) Lists are immutable, tuples are mutable.
b) Tuples are immutable, lists are mutable, and both can hold mixed types.
c) Tuples are faster than lists *because* they are mutable.
d) Lists cannot contain other lists.
**Answer:** b) — tuples are immutable sequences; lists are mutable. Both hold
mixed types. **CLO-1 · Understand · Easy**

**Q1.2 (Code tracing).** What does the following print?

```python
words = ["data", "science", "ai"]
out = [w.upper() for w in words if len(w) > 2]
print(out)
```

**Answer:** `['DATA', 'SCIENCE', 'AI']` — all three words have length > 2; the
comprehension filters then transforms. **CLO-1 · Apply · Easy**

**Q1.3 (Debugging).** This code raises `TypeError`. Identify the cause and the
fix.

```python
total = 0
for row in ["2", "3.5"]:
    total = total + row
print(total)
```

**Answer:** `row` is a string; `0 + "2"` fails. Fix: `total = total +
float(row)`. **CLO-1 · Analyze · Medium**

**Q1.4 (Conceptual).** Why do data science courses insist on a virtual
environment per project? Give two reasons.
**Answer:** (1) isolation — different projects can need different package
versions without breaking each other; (2) reproducibility — a frozen
environment (`requirements.txt`) can be recreated on another machine.
**CLO-1 · Understand · Medium**

**Q1.5 (Short answer).** In Jupyter, a cell prints `NameError: name 'df' is
not defined` even though "it worked earlier." What happened, and what is the
standard fix?
**Answer:** hidden state — the cell that defined `df` was not run in this
kernel session (or was run out of order). Fix: Kernel → Restart & Run All so
cells execute top-to-bottom. **CLO-1 · Analyze · Medium**

## B. Git & GitHub

**Q2.1 (MCQ).** What does `git commit` do?
a) Uploads your code to GitHub.
b) Creates a snapshot of the staged changes with a message.
c) Saves the file to disk.
d) Merges two branches.
**Answer:** b) — commit snapshots the *staged* content; `git push` uploads,
`git add` stages. **CLO-1/CLO-3 · Understand · Easy**

**Q2.2 (Scenario).** Two students edit the same line of `eda.ipynb` on
different branches and then merge. Git reports a conflict. Explain why, and
give the correct resolution steps.
**Answer:** both branches changed the same lines, so Git cannot choose
automatically. Resolve: open the file, keep the intended version(s), then
`git add <file>` and `git commit` to record the merge. **CLO-3 · Analyze ·
Medium**

**Q2.3 (Command tracing).** Order these commands so the final result is a
pushed commit containing only `notebook.ipynb`:
`git commit -m "..."`, `git push origin main`, `git add notebook.ipynb`,
`git status`.
**Answer:** `git status` (inspect) → `git add notebook.ipynb` → `git commit
-m "..."` → `git push origin main`. **CLO-1/CLO-3 · Apply · Easy**

**Q2.4 (Conceptual).** Why write commit messages that explain *why* a change
was made rather than *what* changed? Give one concrete benefit.
**Answer:** history becomes readable — months later, `git log` tells you the
intent (why), not just the diff (what); this makes review, debugging, and
reverting specific changes practical. **CLO-3 · Evaluate · Medium**

## C. NumPy

**Q3.1 (MCQ).** `a = np.arange(12).reshape(3, 4)`. What is the shape of
`a[1]`?
a) `(3, 4)`  b) `(4,)`  c) `(1, 4)`  d) `(3,)`
**Answer:** b) — a single integer index drops the dimension; the row is a
1-D array of length 4. Use `a[[1]]` or `a[1].reshape(1, -1)` to keep 2-D.
**CLO-1 · Apply · Easy**

**Q3.2 (Code tracing).** What does this print?

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b)
print((a > 1).sum())
```

**Answer:** `[11 22 33]` then `2` (the boolean mask `[False, True, True]`
sums to 2). **CLO-1 · Apply · Easy**

**Q3.3 (Debugging).** `np.mean(temps)` prints `15.2` but your team expected
the mean *per store*, where `temps.shape == (3, 24)`. What went wrong and
what is the correct call?
**Answer:** `np.mean(temps)` averages all 72 values. Per store:
`np.mean(temps, axis=1)` → 3 means. **CLO-1 · Apply · Medium**

**Q3.4 (Conceptual).** Why must every element of an ndarray share one dtype?
**Answer:** operations are vectorized over contiguous, same-typed memory; a
single dtype is what makes NumPy fast and predictable. Mixed types would
require an `object` array and lose the speed. **CLO-1 · Understand · Medium**

**Q3.5 (Practical coding).** Write one line that counts how many elements of
`temps` are above 25, using a boolean mask.
**Answer:** `(temps > 25).sum()` — or `np.count_nonzero(temps > 25)`.
**CLO-1 · Apply · Medium**

## D. Pandas

**Q4.1 (MCQ).** `df` has a default RangeIndex. Which selects the row at
*position* 10?
a) `df.loc[10]`  b) `df.iloc[10]`  c) `df["10"]`  d) `df[10]`
**Answer:** b) — `.iloc` is positional; `.loc` is by label (they coincide
only because the index is 0..n−1 here). **CLO-1 · Understand · Easy**

**Q4.2 (Code tracing).** What does this print?

```python
import pandas as pd
df = pd.DataFrame({"day": ["Sat", "Sun", "Sat"], "tip": [2.0, 3.0, 4.0]})
print(df.groupby("day")["tip"].mean())
```

**Answer:** `day`-indexed Series: `Sat 3.0`, `Sun 3.0`. **CLO-1 · Apply ·
Easy**

**Q4.3 (Debugging).** This raises an error. Explain why and fix it.

```python
big = df[df["total_bill"] > 20 & df["size"] == 2]
```

**Answer:** operator precedence — `&` binds tighter than `>`/`==`, so Python
evaluates `20 & df["size"]`. Fix with parentheses: `df[(df["total_bill"] >
20) & (df["size"] == 2)]`. **CLO-1 · Analyze · Medium**

**Q4.4 (Short answer).** You save a DataFrame with `to_csv("out.csv")` and
re-read it: the file contains an extra unnamed column. What happened and how
do you prevent it?
**Answer:** pandas wrote the index as a column. Fix: `to_csv("out.csv",
index=False)`. **CLO-1 · Apply · Easy**

**Q4.5 (Conceptual).** What is the difference between a Series and a
DataFrame, and why can a DataFrame hold mixed column types?
**Answer:** a Series is a labeled 1-D array (one column); a DataFrame is a
labeled 2-D table of Series sharing one index. Each column is its own array
(ndarray/Series), so columns can differ in type. **CLO-1 · Understand · Easy**

**Q4.6 (Practical coding).** Write a single (chained) expression: rows from
`df` where `day == "Sun"` and `total_bill > 20`, sorted by `tip`
descending.
**Answer:** `df[(df["day"] == "Sun") & (df["total_bill"] > 20)].sort_values("tip", ascending=False)`.
**CLO-1 · Apply · Medium**

## E. Data cleaning

**Q5.1 (MCQ).** `df["age"]` has 3 missing values out of 24 rows. When is
`dropna(subset=["age"])` clearly the better choice than `fillna(mean)`?
a) When age is numeric and missingness is tiny.
b) When rows missing age are unusable anyway and you can afford to lose them.
c) When the mean is easy to compute.
d) Never — filling is always better.
**Answer:** b) — dropping is right when the field is essential, missing
rows are few, and loss is affordable; filling injects a fake value.
**CLO-1 · Evaluate · Medium**

**Q5.2 (Debugging).** This raises an error. Why?

```python
df["age"] = df["age"].astype(int)
```

(where `df["age"]` contains NaN)
**Answer:** NaN is a float with no integer representation; `astype(int)`
fails on missing values. Fill or drop NaN first, then convert.
**CLO-1 · Analyze · Medium**

**Q5.3 (Code tracing).** What is the dtype of `df["income"]` after these two
lines, and what would you do next?

```python
df["income"] = df["income"].str.replace(",", "")
print(df["income"].dtype)
```

**Answer:** `object` (still strings). Next: `.astype(float)` before any
arithmetic. **CLO-1 · Apply · Medium**

**Q5.4 (Scenario).** A survey export contains two rows for the same email —
one with an age, one without. You run `df.drop_duplicates()` and the
duplicate remains. Why, and what is the correct call?
**Answer:** the rows differ in other columns, so they are not *complete*
duplicates. Use `df.drop_duplicates(subset=["email"], keep="first")` to
deduplicate on the identifying column. **CLO-1 · Analyze · Medium**

## F. Data acquisition & combining

**Q6.1 (MCQ).** An API call returns status 429. What does that mean and what
is the correct action?
a) Server error — retry immediately.
b) Rate limit exceeded — wait/back off (and check your caching).
c) Not found — fix the URL.
d) Success — parse the body.
**Answer:** b) — 429 = too many requests; respect it with backoff and
caching. **CLO-1 · Understand · Easy**

**Q6.2 (Conceptual).** Why cache API responses to disk even when the API is
free? Give two reasons.
**Answer:** (1) politeness/reliability — you don't hammer shared public
infrastructure; (2) reproducibility/offline — reruns and grading work without
the network. **CLO-1 · Understand · Medium**

**Q6.3 (Code tracing).** `sales` has 10 rows, `menu` has 8 rows, and one
sales item is missing from `menu`. What does `sales.merge(menu,
on="item", how="inner")` return?
**Answer:** 9 rows — the sales row whose item is not in menu is dropped
(inner join keeps only matching keys). A left join would return 10 rows with
a NaN for the missing price. **CLO-1 · Apply · Medium**

**Q6.4 (Scenario).** After a `merge`, the result has *more* rows than either
input. Explain what happened and how to confirm it.
**Answer:** a one-to-many join — the key appears multiple times on the "one"
side (e.g., two menu prices for "pizza"), so each match multiplies rows.
Confirm by checking counts per key before merging and by comparing row
counts before/after. **CLO-1 · Analyze · Medium**

## G. Visualization

**Q7.1 (MCQ).** Which chart is the right first choice for "how has monthly
revenue changed over two years"?
a) pie chart  b) line plot  c) bar chart of each month as separate category
d) histogram
**Answer:** b) — a line plot shows order and trend over time; a histogram
shows a distribution, a pie hides changes. **CLO-1 · Understand · Easy**

**Q7.2 (Code tracing).** `fig, axes = plt.subplots(2, 2)`. What type is
`axes`, and which call targets the bottom-left subplot?
**Answer:** `axes` is a 2×2 NumPy array of Axes objects; the bottom-left is
`axes[1, 0]`. **CLO-1 · Apply · Easy**

**Q7.3 (Conceptual).** A scatter of 300 points shows nothing but a dark blob.
What is the likely cause and the one-line fix?
**Answer:** overplotting — later points hide earlier ones. Fix: add
`alpha=0.4` (or jitter/subsample) so density is visible.
**CLO-1 · Analyze · Medium**

**Q7.4 (Debugging).** The legend shows only one category even though the
plot uses `hue="smoker"`. What is the most likely cause?
**Answer:** the plot was drawn with a filtered subset (one category) — or a
fresh figure was created after the hue-aware call. Check what data the call
actually received. **CLO-1 · Analyze · Medium**

**Q7.5 (Short answer).** When comparing tips across days, why plot
`tip / total_bill * 100` instead of raw `tip`?
**Answer:** raw tip correlates with bill size; the percentage controls for
it, answering "who tips generously" instead of "who had bigger bills."
**CLO-1 · Evaluate · Medium**

---

## Marking guide (suggested)

| Item | Points |
|---|---|
| Q1.1–Q7.5 (33 questions) | 2 each = 66 |
| Bonus: any fully correct practical-coding item (Q3.5, Q4.6) | +2 each |
| **Total** | **66 + up to 4** |

Bloom's spread: Understand ≈ 9, Apply ≈ 13, Analyze ≈ 8, Evaluate ≈ 3.
CLO spread: CLO-1 ≈ 30, CLO-3 ≈ 3.