# Session 12 — Combining Data: concat, merge, join

**Week 6 · Session 12 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain the difference between stacking tables (`concat`) and matching tables (`merge`).
- Use `concat` to combine rows or columns of tables with the same structure.
- Use `merge` with `on`, `how`, and `left_on`/`right_on` for relational joins.
- Explain inner vs. left vs. outer joins and choose the right one.
- Detect and debug common merge problems: duplicate keys, name collisions, row explosions.

## 2. Key concepts

- **Two ways to combine:** stack (same structure → `concat`) vs. match (shared key → `merge`).
- **Keys** — the columns that identify records (e.g., `student_id`); joins match on keys.
- **Join types:** `inner` (only matches), `left` (keep all left rows), `right`, `outer` (everything).
- **`concat`** — row-wise (`axis=0`, the default) or column-wise (`axis=1`).
- **`merge`** is SQL's JOIN in Pandas — one of the most valuable skills in industry interviews and real work.
- Most real datasets are **relational**: separate tables linked by keys; combining is how you build the analysis table.

## 3. Detailed lecture notes

**Why combining?** Real data rarely lives in one table. A university might have
`students.csv`, `courses.csv`, and `enrollments.csv` — each with a key
(`student_id`, `course_id`). Analysis needs them *joined* into one table.
Knowing when to stack and when to match is the difference between correct
pipelines and duplicated/garbled ones.

**concat — stacking.** `pd.concat([df1, df2])` stacks rows: same columns,
more rows (e.g., January sales + February sales). `axis=1` stacks side by side:
same rows, more columns (rarely needed; keys must align). What `concat` does
*not* do: match values. If you concat two tables with overlapping IDs you get
duplicated rows, not merged records. Rule: **same shape → concat; shared key →
merge.**

**merge — matching.** The mental model: for every left row, find right rows with
the same key value; combine them. `pd.merge(left, right, on="student_id")` joins
on the common column. `how=` controls which rows survive:
- `how="inner"` — only keys present in **both** (default; often silently drops unmatched data — check!).
- `how="left"` — all left rows, fill unmatched right columns with NaN (the everyday default for analysis).
- `how="outer"` — everything, NaN where missing on either side.
Show the classic 2×2 examples (students × courses) with each `how` and let
students *see* which rows survive. When key names differ:
`left_on="id", right_on="student_id"`. When merging on the index:
`df1.join(df2)` (convenience wrapper).

**Danger zones.** Three classic merge bugs:
1. **Row explosion:** if a key repeats on the right side, every match creates a
   row (1 student × 3 courses = 3 rows) — usually *desired*, but surprising; check
   `shape` after merging.
2. **Name collisions:** both tables have a `name` column → result has
   `name_x`/`name_y`; rename columns before merging or use `suffixes`.
3. **Silent loss with `inner`:** unmatched keys vanish with no warning; count
   rows before/after to verify.
Rule: **after any merge, check `shape` and `isna().sum()`** — the merge is only
correct if the numbers tell the story you expected.

**Relational thinking.** Tables = entities; keys = relationships; joins = the
queries that connect them. This course stops at 2-way merges, but the *habit*
(define keys, choose join type, verify) scales to any database.

## 4. Important terminology

- **Key** — a column whose values identify records (primary key = unique per table).
- **`concat`** — stack tables along rows (`axis=0`) or columns (`axis=1`).
- **`merge`** — join tables on key columns (SQL JOIN).
- **`on=`** — shared key column; **`left_on`/`right_on`** — differently named keys.
- **`how=`** — `inner`, `left`, `right`, `outer` join type.
- **Left table / right table** — the two arguments to `merge`; "left" semantics keep all left rows.
- **Row explosion** — multiple matches multiply rows.
- **Suffixes** — how Pandas disambiguates colliding column names (`_x`, `_y`).
- **One-to-many** — one key value in the left table matches many in the right (the common case).

## 5. Python examples

```python
import pandas as pd

students = pd.DataFrame({
    "student_id": [1, 2, 3],
    "name": ["Ali", "Sara", "Usman"],
})
courses = pd.DataFrame({
    "student_id": [1, 1, 2, 4],
    "course": ["Python", "Stats", "Python", "DB"],
    "grade": ["A", "B", "A", "C"],
})

# --- concat: same structure, more rows ---
more = pd.DataFrame({"student_id": [5], "name": ["Zara"]})
all_students = pd.concat([students, more], ignore_index=True)
print(all_students)

# --- merge: match on key ---
inner = pd.merge(students, courses, on="student_id")          # only ids 1,2
left  = pd.merge(students, courses, on="student_id", how="left")  # keeps id 3 (no course -> NaN)
outer = pd.merge(students, courses, on="student_id", how="outer") # keeps id 4 (no name -> NaN)
print("inner rows:", len(inner), "| left rows:", len(left), "| outer rows:", len(outer))

# --- different key names ---
grades = courses.rename(columns={"student_id": "sid"})
merged = pd.merge(students, grades, left_on="student_id", right_on="sid", how="left")
print(merged.drop(columns="sid"))
```

## 6. Beginner example

```python
import pandas as pd

orders = pd.DataFrame({"order_id": [1, 2], "customer": ["A", "B"]})
payments = pd.DataFrame({"order_id": [1, 2], "amount": [500, 300]})

print(pd.merge(orders, payments, on="order_id"))
```

Two tables, one key, one line — a join. This is how every billing system works.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns

# Relational version of the tips data: bills + a "customer" lookup table
bills = sns.load_dataset("tips").reset_index().rename(columns={"index": "bill_id"})
customers = pd.DataFrame({
    "bill_id": bills["bill_id"],
    "city": ["Lahore", "Karachi", "Islamabad", "Multan"] * 61,   # synthetic, for demo
}).head(len(bills))

# What if some bills have no customer record? Simulate a mismatch:
customers = customers[customers["bill_id"] % 5 != 0]     # drop every 5th

# Inner join loses those bills silently:
inner = pd.merge(bills, customers, on="bill_id", how="inner")
print("bills:", len(bills), "-> inner join rows:", len(inner))

# Left join keeps every bill and flags unmatched customers as NaN:
left = pd.merge(bills, customers, on="bill_id", how="left")
print("left join rows:", len(left), "| missing city:", left["city"].isna().sum())

# Real question answered on the joined table:
print(left.groupby("city")["tip"].mean().round(2))
```

The point: join choice **changed the analysis population**. Left join = "every
bill, customer info when available" — usually what you want; inner join silently
dropped data.

## 8. In-class activity (50 min)

In `notebooks/week-06/session-12-combining-data.ipynb`:

1. **concat (10 min):** split `tips` into two frames by day range and re-stack with `concat`; verify row count.
2. **merge drill (20 min):** create small `students` and `courses` tables; run inner/left/outer merges; write which rows survive in each and why (markdown).
3. **Verify habit (10 min):** for each merge, compare `len()` before/after and check `isna().sum()`.
4. **One-to-many (10 min):** merge students with a multi-row course table; explain the row explosion with a sentence and a printed `shape`.

## 9. Lab exercise

**Lab 3 is due today** (`labs/lab-03/`): data acquisition & combining — fetch an
API dataset, load a CSV, combine them with `merge` on a shared key, and answer
checkpoint questions. **Assignment 1 released** (due Session 15): cleaning +
manipulation with Pandas — see `../assignments/assignment-01`.

## 10. Common mistakes

- Using `concat` to combine tables that should be `merge`d → duplicated rows, no matching.
- Default `how="inner"` dropping data silently → always count rows before/after.
- Merging on columns with different names and forgetting `left_on`/`right_on`.
- Ignoring `_x`/`_y` collisions instead of renaming columns first.
- Forgetting that a repeated key on the right side multiplies rows ("where did 90 rows come from?").
- Merging on an index unintentionally (two default 0..n indexes match 1:1 and silently corrupt the join).
- Not verifying after merging — a merge can look right and be wrong.

## 11. Short assessment questions

1. When do you use `concat` instead of `merge`?
2. What does `how="left"` guarantee about the result's row count?
3. Which join type drops unmatched rows from both sides?
4. After `pd.merge(a, b, on="id")` you get 4× the rows of `a`. What happened and is it wrong?
5. Both tables have a `date` column; what will the merged frame contain, and how do you control it?
6. What should you always check after a merge? (Row count and missing values.)

## 12. CLO mapping

CLO-1: combining tables is core data manipulation — and the final skill
Assignment 1 assumes. Relational thinking (keys, joins) also prepares the
final project's multi-source data work.

## 13. Suggested homework

- Start Assignment 1 early (due Session 15) — it builds directly on Sessions 7–12.
- Practice: find two related CSVs (or make them) and answer a question only answerable after a join.
- Read: pandas docs — "Merge, join, concatenate" (skim the merge section; ignore the advanced SQL-like material).
- Preview: `tips.plot(kind="scatter", x="total_bill", y="tip")` and `sns.histplot(tips["tip"])` — Session 13 turns these one-liners into proper figures.