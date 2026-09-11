# Midterm Exam — Weeks 1–8 (Sessions 1–16)

**Administered:** W8 S16 · **Time:** 90 minutes · **Closed notes for Parts I–IV;**
open-notebook (no internet) for Part V as specified by the instructor.
**Covers:** Python, Jupyter, Git/GitHub, NumPy, Pandas, data cleaning, data
acquisition & combining, visualization, EDA workflow.
**CLOs:** CLO-1 (primary), CLO-2 (entry-level question in Part VI).
**Bloom's levels:** Remember–Create · **Difficulty:** Easy–Hard.

Format: Part I MCQ (12 × 2), Part II code tracing (8 × 3), Part III debugging
(5 × 4), Part IV short answer (6 × 3), Part V practical coding (3 tasks, 8
each), Part VI scenario (2 × 5). Total 100. Answers embedded — remove
`**Answer:**`/`**Key:**` lines for the student paper.

---

## Part I — Multiple choice (12 × 2 = 24)

**Q1 (MCQ).** `np.arange(12).reshape(3, 4)[:, 1]` has shape:
a) `(3,)`  b) `(3, 1)`  c) `(1, 3)`  d) `(4,)`
**Answer:** a) — slicing with `:` keeps rows, selects one column → 1-D.
**CLO-1 · Apply · Easy**

**Q2 (MCQ).** Which expression returns a **copy**-safe way to select rows
where `program` is either "DS" or "AI"?
a) `df[df.program == "DS" | "AI"]`
b) `df[df["program"].isin(["DS", "AI"])]`
c) `df[df["program"] == ["DS", "AI"]]`
d) `df.loc["DS", "AI"]`
**Answer:** b) — `.isin` is the readable, correct membership filter.
**CLO-1 · Apply · Easy**

**Q3 (MCQ).** `df["tip"].mean()` returns 3.0, but your colleague's identical
code returns 2.998. The most likely cause:
a) Their pandas version rounds differently.
b) Their data has extra/missing rows (e.g., different dropna).
c) `.mean()` is random.
d) They used `median` by accident only.
**Answer:** b) — the data differs (or was cleaned differently); always
verify shapes before comparing outputs. **CLO-1 · Analyze · Medium**

**Q4 (MCQ).** Which is the correct sequence for a first EDA?
a) Plot → clean → load → describe
b) Load → quality check → univariate → bivariate → insights
c) Model → split → clean → plot
d) Load → model → plot → clean
**Answer:** b) — overview → quality → distributions → relationships →
insights. **CLO-1 · Understand · Easy**

**Q5 (MCQ).** `plt.subplots(2, 2)` returns:
a) one Figure and one Axes
b) a tuple `(fig, axes)` where axes is a 2×2 array
c) four Figures
d) a dict of Axes
**Answer:** b) — figure plus a 2-D array of Axes; index `axes[row, col]`.
**CLO-1 · Understand · Easy**

**Q6 (MCQ).** A merge of two tables returned more rows than either input.
The most likely explanation:
a) `ignore_index=True` duplicates rows.
b) A one-to-many key multiplied rows.
c) The tables had different dtypes.
d) The index was reset.
**Answer:** b) — duplicate keys on the "one" side multiply matches; check
key cardinality before merging. **CLO-1 · Analyze · Medium**

**Q7 (MCQ).** `df.drop_duplicates()` does NOT remove a row that shares an
email with another row. Why?
a) drop_duplicates keeps the last occurrence.
b) The rows differ in other columns — they are not complete duplicates.
c) Emails are ignored.
d) The index must be reset first.
**Answer:** b) — complete-row equality is required; use
`drop_duplicates(subset=["email"])` for key-based dedup.
**CLO-1 · Apply · Medium**

**Q8 (MCQ).** After `df["income"].str.replace(",", "")`, the dtype is:
a) float64  b) int64  c) object  d) str (new pandas dtype)
**Answer:** c) — still strings; convert with `.astype(float)` before math.
**CLO-1 · Apply · Medium**

**Q9 (MCQ).** Which command uploads your local commits to GitHub?
a) `git commit`  b) `git add`  c) `git push`  d) `git merge`
**Answer:** c). **CLO-1, CLO-3 · Remember · Easy**

**Q10 (MCQ).** An API response has status 200 but `resp.json()` raises.
The most likely cause:
a) The server is down.
b) The body is not valid JSON (e.g., an HTML error page).
c) The URL is wrong.
d) The timeout was too long.
**Answer:** b) — 200 says "request OK"; the body may still be HTML or
malformed; inspect `resp.text` first. **CLO-1 · Analyze · Medium**

**Q11 (MCQ).** Why is `alpha=0.4` used on a 300-point scatter?
a) To make colors prettier.
b) To reveal density where points overlap.
c) To hide outliers.
d) To speed up rendering only.
**Answer:** b) — transparency exposes overplotting.
**CLO-1 · Understand · Easy**

**Q12 (MCQ).** `penguins.groupby("species")["body_mass_g"].mean()` returns:
a) a DataFrame with two columns.
b) a Series indexed by species.
c) a single number.
d) a NumPy array of 3 columns.
**Answer:** b) — one column aggregated per group → Series.
**CLO-1 · Apply · Easy**

## Part II — Code tracing (8 × 3 = 24)

**Q13.** What prints?

```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
print(a.sum(axis=0))
print(a.sum(axis=1))
```

**Answer:** `[4 6]` (column sums) then `[3 7]` (row sums).
**CLO-1 · Apply · Easy**

**Q14.** What prints?

```python
s = pd.Series([10, 20, 30, 40])
print(s[s > 20].mean())
```

**Answer:** `35.0` — mask selects 30 and 40.
**CLO-1 · Apply · Easy**

**Q15.** What prints?

```python
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
print(df.loc[1, "a"], df.iloc[1, 0])
```

**Answer:** `2 2` — both target row 1, column a; labels and positions
coincide on a default index. **CLO-1 · Apply · Easy**

**Q16.** What prints?

```python
words = ["KHI", "LHE", "khi", "KHI "]
clean = [w.strip().upper() for w in words]
print(len(set(clean)))
```

**Answer:** `2` — {"KHI", "LHE"} after strip + upper.
**CLO-1 · Apply · Medium**

**Q17.** The file `sales.txt` has a header line. What does this print?

```python
rows = []
with open("sales.txt") as f:
    next(f)
    for line in f:
        parts = line.strip().split(",")
        rows.append((parts[0], int(parts[1])))
print(len(rows))
```

**Answer:** the number of data rows (header skipped; one tuple per line).
**CLO-1 · Apply · Medium**

**Q18.** What prints?

```python
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2)
print(type(axes))
```

**Answer:** `numpy.ndarray` — a 1-D array of 2 Axes (not a list).
**CLO-1 · Apply · Medium**

**Q19.** `tips.merge(menu, on="item", how="left")` — `tips` has 10 rows and
one item is missing from `menu`. What is the result's shape and what is in
the missing cell?
**Answer:** `(10, ...)` — all tips rows survive; the missing item's price is
`NaN`. **CLO-1 · Apply · Medium**

**Q20.** What prints?

```python
import pandas as pd
df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
print(df["x"].corr(df["y"]))
```

**Answer:** `1.0` — perfect positive linear relationship.
**CLO-1 · Apply · Easy**

## Part III — Debugging (5 × 4 = 20)

**Q21.** Explain the error and fix the code.

```python
big = df[df.total_bill > 20 & df.size == 2]
```

**Answer:** precedence — `&` binds tighter than `>`/`==`; wrap conditions:
`df[(df["total_bill"] > 20) & (df["size"] == 2)]`.
**CLO-1 · Analyze · Medium**

**Q22.** This raises `KeyError: 'month'` after the notebook "worked earlier."
Give two likely causes and the diagnostic step.
**Answer:** (1) an earlier cell overwrote `df` with a different frame;
(2) the file was re-read with different headers. Diagnose: check
`df.columns` and cell order (Restart & Run All). **CLO-1 · Analyze · Medium**

**Q23.** The CSV round-trip added an `Unnamed: 0` column. Why, and what is
the one-line fix?
**Answer:** the index was saved as a column — `to_csv(..., index=False)`.
**CLO-1 · Apply · Easy**

**Q24.** This fails with "cannot convert float NaN to integer." Why?

```python
df["age"] = df["age"].astype(int)
```

**Answer:** NaN has no integer representation; fill or drop missing values
first, then convert. **CLO-1 · Analyze · Medium**

**Q25.** Two plots that should show the same trend look different because one
saved figure was generated before the data fix. What habit prevents this?
**Answer:** re-run the notebook top-to-bottom (Restart & Run All) before
exporting figures, and regenerate outputs after every data change — stale
outputs are a reproducibility failure. **CLO-1, CLO-3 · Evaluate · Medium**

## Part IV — Short answer (6 × 3 = 18)

**Q26.** Explain the difference between `.loc` and `.iloc`, with a case where
they differ.
**Answer:** `.loc` selects by index *label*, `.iloc` by integer *position*;
they differ whenever the index is not 0..n−1 (e.g., after a filter or
`set_index`). **CLO-1 · Understand · Easy**

**Q27.** When is `dropna` better than `fillna` for missing values? Give one
example where filling is right.
**Answer:** drop when rows are few, the field is essential, and loss is
affordable; fill (e.g., mean/median) when a numeric column has light,
random missingness and you must keep every row. **CLO-1 · Evaluate · Medium**

**Q28.** Why must `X` be 2-D for scikit-learn while `y` is 1-D?
**Answer:** features are a matrix of samples × variables; the target is one
value per sample. The API enforces this shape contract.
**CLO-2 · Understand · Medium** *(entry-level CLO-2 item)*

**Q29.** What does `value_counts(normalize=True)` return, and when is the
normalized version more useful than the raw counts?
**Answer:** category counts as proportions; normalized compares groups of
unequal size (e.g., smoker share across a split).
**CLO-1 · Apply · Medium**

**Q30.** Name the five stages of the data science lifecycle and map this
midterm's Parts I–V to them.
**Answer:** ask → get → clean/explore → model/analyze → communicate;
Parts I–III ≈ get/clean; Part IV ≈ explore; Part V ≈ explore + analyze;
communication is assessed via written answers. (Any consistent mapping with
justification is accepted.) **CLO-1 · Understand · Medium**

**Q31.** Why is reproducibility (seeds, `requirements.txt`, restart-safe
notebooks) part of CLO-1 rather than an afterthought?
**Answer:** an analysis nobody can rerun cannot be verified, graded, or
trusted; reproducibility is what makes the other CLO skills auditable.
**CLO-3 · Evaluate · Medium**

## Part V — Practical coding (3 × 8 = 24)

Open-notebook; write code in a fresh notebook cell per task. Code must run
on `tips` (seaborn built-in).

**Q32.** Load `tips`, drop rows with missing values, then print: the shape,
the mean tip for `day == "Sat"`, and the number of rows with `size == 2`
and `total_bill > 30`. **CLO-1 · Apply · Medium**
**Key:**

```python
import seaborn as sns
tips = sns.load_dataset("tips").dropna()
print(tips.shape)                                   # (244, 7)
print(tips[tips["day"] == "Sat"]["tip"].mean())     # ~2.99
print(len(tips[(tips["size"] == 2) & (tips["total_bill"] > 30)]))  # 3
```

**Q33.** Build one figure with two subplots: (a) a histogram of `tip` (15
bins); (b) a scatter of `total_bill` vs `tip` with `alpha=0.5`. Label all
axes; save to `midterm-q33.png` at 150 dpi. **CLO-1 · Apply · Medium**
**Key:**

```python
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].hist(tips["tip"], bins=15, edgecolor="white")
axes[0].set_xlabel("Tip ($)"); axes[0].set_ylabel("Count")
axes[1].scatter(tips["total_bill"], tips["tip"], alpha=0.5)
axes[1].set_xlabel("Total bill ($)"); axes[1].set_ylabel("Tip ($)")
fig.tight_layout()
fig.savefig("midterm-q33.png", dpi=150, bbox_inches="tight")
```

**Q34.** From the flights dataset, compute with pandas: the year with the
highest total passengers and the single month–year with the most passengers.
Then write ONE sentence interpreting what the pair of answers says about
growth. **CLO-1 · Apply · Medium**
**Key:**

```python
import seaborn as sns
flights = sns.load_dataset("flights")
print(flights.groupby("year")["passengers"].sum().idxmax())   # 1960
print(flights.loc[flights["passengers"].idxmax()])            # July 1960
# Sentence: the busiest year overall is the last in the series (1960) and
# the single busiest month is near its end (July 1960) — consistent with
# steady growth across the whole series.
```

## Part VI — Scenario (2 × 5 = 10)

**Q35.** A teammate merges two CSV exports by concatenating them and reports
"the total revenue doubled." List the two most likely causes and how you
would confirm each. **CLO-1 · Analyze · Hard**
**Answer:** (1) the exports overlap (same transactions in both) — confirm
with `duplicated()` on an invoice id; (2) the concatenation kept duplicate
rows (no dedup by key) — confirm by comparing `len` before/after
`drop_duplicates(subset=["invoice_id"])`. Fix by merging on the key instead
of blindly concatenating.

**Q36.** Your EDA notebook produces a scatter that appears to show a strong
relationship, but the correlation is 0.12. Give two explanations and the
check for each. **CLO-1 · Analyze · Hard**
**Answer:** (1) the relationship is nonlinear (correlation measures linear
association) — check with a residual/binned-means plot; (2) an outlier or
mis-encoded group dominates the visual — check `groupby` means and a
logged/subsampled view; (3) colors/point size created an illusion — check
with a plain scatter first.

---

## Marking guide

| Part | Max | Items |
|---|---|---|
| I MCQ | 24 | 12 × 2 |
| II Code tracing | 24 | 8 × 3 |
| III Debugging | 20 | 5 × 4 |
| IV Short answer | 18 | 6 × 3 |
| V Practical | 24 | 3 × 8 |
| VI Scenario | 10 | 2 × 5 |
| **Total** | **100** | |

Bloom's spread: Remember 1, Understand 7, Apply 14, Analyze 11, Evaluate 3,
Create 0 (creation is assessed in the project). CLO spread: CLO-1 ≈ 30
items, CLO-2 = 1 (Q28), CLO-3 ≈ 2 (Q25, Q31).