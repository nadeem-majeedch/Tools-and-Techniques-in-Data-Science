# Content for notebook 05: Data Aggregation.
CELLS = [
    ("md", """# 05 — Data Aggregation

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Apply Python and standard data science libraries to datasets.

Real questions are usually *grouped* questions: "tips **by day**", "sales
**by region**", "grades **by section**". Aggregation is the set of tools for
answering them — `groupby`, `value_counts`, `crosstab`, and the combining
tools `concat` and `merge`.

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain split-apply-combine, the idea behind `groupby`.
2. Compute grouped summaries with one or more aggregations (`agg`).
3. Use `value_counts` and `crosstab` for categorical exploration.
4. Stack tables with `concat` and match tables with `merge`.
5. Choose the right join type (`inner`, `left`, `outer`) and verify the result.

---
"""),
    ("md", """## Theory: split-apply-combine

Every `groupby` question has the same three steps:

1. **Split** the table into groups by the unique values of a column.
2. **Apply** a function to each group (mean, sum, count, ...).
3. **Combine** the results into a new table indexed by the groups.

`df.groupby("day")["tip"].mean()` reads like a sentence: "group by day,
take tip, average it". Remember: `groupby` alone does nothing visible —
you must apply an aggregation.

---
"""),("code", """import pandas as pd
import seaborn as sns

tips = sns.load_dataset("tips")

# The canonical example: mean tip by day
by_day = tips.groupby("day")["tip"].mean().round(2)
print(by_day)
print()
print(type(by_day))     # a Series, indexed by day

# Multiple statistics at once with agg
summary = tips.groupby("day")["tip"].agg(["mean", "median", "count"]).round(2)
print(summary)

# Expected output:
#   day
#   Thur    2.77
#   Fri     2.73
#   Sat     2.99
#   Sun     3.26
#   Name: tip, dtype: float64
"""),
    ("md", """## Grouping by more than one column

Grouping by two columns splits into (day, sex) pairs — one row per
combination. The result is a MultiIndex (two levels); flattening it with
`reset_index()` often makes the table easier to read.

---
"""),("code", """two = tips.groupby(["day", "sex"])["tip"].mean().round(2)
print(two)
print()
print(two.reset_index())

# Expected output (first rows):
#   day   sex
#   Thur  Male     2.57
#         Female   3.09
#   Fri   Male     2.59
#         Female   2.78
#   ...
"""),
    ("md", """## Categorical exploration: value_counts and crosstab

- `value_counts()` — how many of each value in one column.
- `crosstab(col1, col2)` — a two-way count table.

Both produce the raw material for bar charts and chi-square-style thinking.

---
"""),("code", """print(tips["day"].value_counts())
print()
print(pd.crosstab(tips["day"], tips["smoker"]))
print()
# Normalize to proportions for fair comparison
print(pd.crosstab(tips["day"], tips["smoker"], normalize="index").round(2))

# Expected output:
#   Sat     87
#   Sun     76
#   Thur    62
#   Fri     19
#   Name: count, dtype: int64
#
#   smoker  Yes  No
#   day
#   Thur     17  45
#   Fri       8  11
#   Sat      39  48
#   Sun      25  51
"""),
    ("md", """## Combining data: concat vs merge

Two different questions, two different tools:

- **`concat`** stacks tables with the *same structure* (more rows: Jan + Feb
  sales). It does not match anything.
- **`merge`** matches tables on a *shared key* (SQL JOIN): students +
  courses on `student_id`.

Rule: **same shape → concat; shared key → merge.**

---
"""),("code", """# --- concat: stacking rows ---
jan = pd.DataFrame({"day": ["Mon", "Tue"], "sales": [100, 120]})
feb = pd.DataFrame({"day": ["Mon", "Tue"], "sales": [110, 130]})
both = pd.concat([jan, feb], ignore_index=True)
print(both)

# --- merge: matching on a key ---
students = pd.DataFrame({"student_id": [1, 2, 3], "name": ["Ali", "Sara", "Usman"]})
courses  = pd.DataFrame({"student_id": [1, 1, 2], "course": ["Python", "Stats", "Python"]})

inner = pd.merge(students, courses, on="student_id")            # only matches
left  = pd.merge(students, courses, on="student_id", how="left")  # keep ALL students
print()
print("inner rows:", len(inner), "| left rows:", len(left))
print(left)
"""),
    ("md", """## Merge joins: inner, left, outer

`how=` decides which rows survive:

- `"inner"` — only keys in **both** tables (default; silently drops the rest).
- `"left"` — all left rows, unmatched right values become NaN.
- `"outer"` — everything from both sides.

**After every merge: check `shape` and `isna().sum()`** — a merge can look
right and be wrong.

---
"""),("code", """left_tbl = pd.DataFrame({"id": [1, 2, 3], "name": ["A", "B", "C"]})
right_tbl = pd.DataFrame({"id": [2, 3, 4], "score": [88, 91, 75]})

for how in ["inner", "left", "outer"]:
    merged = pd.merge(left_tbl, right_tbl, on="id", how=how)
    print(f"{how:6s} -> {len(merged)} rows")
    print(merged.to_string(index=False))
    print()

# Expected output:
#   inner  -> 2 rows
#   id name  score
#    2    B     88
#    3    C     91
#
#   left   -> 3 rows
#   id name  score
#    1    A    NaN
#    2    B   88.0
#    3    C   91.0
#
#   outer  -> 4 rows
#   id name  score
#    1    A    NaN
#    2    B   88.0
#    3    C   91.0
#    4  NaN   75.0
"""),
    ("md", """## Beginner example: the grouped question

"Are tips different on weekends?" — one question, four lines, an answer with
evidence.

---
"""),("code", """tips["is_weekend"] = tips["day"].map({"Fri": 0, "Sat": 1, "Sun": 1, "Thur": 0})

result = tips.groupby("is_weekend")["tip_pct"] if "tip_pct" in tips else tips.groupby("is_weekend")["tip"]
result = tips.groupby("is_weekend")["tip"].mean().round(2)
print(result)

# Expected output:
#   is_weekend
#   0    2.76
#   1    3.12
#   Name: tip, dtype: float64
"""),
    ("md", """## Intermediate example: a relational mini-project

Two tables (customers, orders) joined and aggregated — the shape of most real
analyses. Watch the row explosion: one customer with three orders produces
three rows.

---
"""),("code", """customers = pd.DataFrame({
    "customer_id": [101, 102, 103],
    "city": ["Lahore", "Karachi", "Lahore"],
})

orders = pd.DataFrame({
    "customer_id": [101, 101, 101, 102, 103],
    "amount": [500, 300, 200, 900, 400],
})

# Join, then aggregate: total and count of orders per city
joined = pd.merge(orders, customers, on="customer_id", how="left")
print("joined rows:", len(joined), "(row explosion: customer 101 has 3 orders)")

per_city = joined.groupby("city")["amount"].agg(["sum", "count", "mean"]).round(0)
print(per_city)

# Expected output:
#   joined rows: 5 (row explosion: customer 101 has 3 orders)
#              sum  count  mean
#   city
#   Karachi   900.0      1   900.0
#   Lahore   1400.0      4   350.0
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Grouped summary

On `tips`, compute the **average total bill** for each combination of `day`
and `time` (lunch/dinner), rounded to 2 decimals. Use `groupby` +
`reset_index`."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
out = tips.groupby(["day", "time"])["total_bill"].mean().round(2).reset_index()
print(out)
# Expected output (first rows):
#      day   time  total_bill
# 0   Thur  Lunch       17.68
# 1   Thur  Dinner      18.78
# 2    Fri  Lunch       16.39
# ...
"""),
    ("md", """### Exercise 2 — crosstab

Build a crosstab of `sex` × `smoker` from `tips` (absolute counts), then the
row-normalized version. Which sex has a higher share of smokers?"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
print(pd.crosstab(tips["sex"], tips["smoker"]))
print()
print(pd.crosstab(tips["sex"], tips["smoker"], normalize="index").round(2))
# Expected output:
#   smoker  Yes  No
#   sex
#   Male     60  97
#   Female   33  54
#
#   smoker  Yes   No
#   sex
#   Male    0.38 0.62
#   Female  0.38 0.62
# (Both sexes have the same 38% smoker share in this dataset.)
"""),
    ("md", """### Exercise 3 — Merge

Create `left = pd.DataFrame({"id": [1, 2], "x": [10, 20]})` and
`right = pd.DataFrame({"id": [2, 3], "y": [200, 300]})`. Merge with
`how="outer"` and fill the resulting NaN values with 0."""),
    ("code", """import pandas as pd
left = pd.DataFrame({"id": [1, 2], "x": [10, 20]})
right = pd.DataFrame({"id": [2, 3], "y": [200, 300]})

# your code here
"""),
    ("code", """# Solution
merged = pd.merge(left, right, on="id", how="outer").fillna(0)
print(merged)
# Expected output:
#    id     x      y
# 0   1  10.0    0.0
# 1   2  20.0  200.0
# 2   3   0.0  300.0
"""),
    ("md", """## Challenge exercise

Use the `penguins` dataset:

1. Compute mean `body_mass_g` per species (round to whole grams).
2. Compute the same, but split further by `island`.
3. Find which (species, island) pair has the *highest* mean body mass.
4. Verify your finding with a `pivot_table`: rows = `species`,
   columns = `island`, values = mean `body_mass_g`."""),
    ("code", """import seaborn as sns
penguins = sns.load_dataset("penguins").dropna()

# your code here
"""),
    ("code", """# Solution
by_species = penguins.groupby("species")["body_mass_g"].mean().round(0)
print(by_species)

by_both = penguins.groupby(["species", "island"])["body_mass_g"].mean().round(0)
print(by_both)
print("Highest pair:", by_both.idxmax(), round(by_both.max()))

print(pd.pivot_table(penguins, index="species", columns="island",
                     values="body_mass_g", aggfunc="mean").round(0))
"""),
    ("md", """## Recap

- `groupby` = split → apply → combine; always finish with an aggregation.
- `agg(["mean", "count", ...])` for several statistics at once.
- `value_counts` (one column) and `crosstab` (two columns) for categories.
- `concat` stacks same-shaped tables; `merge` matches on a key.
- `how=` controls joins: inner / left / outer — choose deliberately.
- After any merge: check row counts and missing values.

---
"""),
    ("md", """## Questions

1. What are the three steps of split-apply-combine?
2. Why does `df.groupby("day")` alone print nothing useful?
3. What is the difference between `concat` and `merge`?
4. Which join type keeps all rows of the left table?
5. What is a row explosion and when is it expected?
6. What should you always check after a merge?

---
**Next:** notebook 06 — Data Visualization.
"""),
]