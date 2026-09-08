# Lab 12 — Combining Data: concat & merge

**Session:** Week 6 · Session 12 · 90 min
**CLO:** CLO-1
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Stack frames with `pd.concat` (rows and columns) and explain
   `ignore_index`.
2. Join tables on keys with `merge` (inner, left, outer) and detect
   surprises.
3. Reason about one-to-many merges and row multiplication.
4. Choose `concat` vs `merge` for a given question.

## Problem statement

A restaurant chain merges two sources: daily sales by table, and a menu
price list. Naively joining them can silently multiply rows. You must build
a combined frame, explain each join's row count, and produce an invoice
report — demonstrating you understand *why* counts change.

## Dataset requirements

Built inline (three small DataFrames in the starter code). No files.

## Step-by-step tasks

1. **Build** `sales_q1`, `sales_q2` (same columns), `menu` (item → price),
   and `staff` (item → chef). Print shapes.
2. **concat rows:** stack `sales_q1` and `sales_q2` with `pd.concat`,
   `ignore_index=True`. Why is `ignore_index` needed here? (The two frames
   have overlapping original indices.) Report the shape — it must be the
   sum.
3. **concat columns:** `pd.concat([sales_q1[["item","qty"]],
   sales_q1[["price"]].assign(dummy=0)], axis=1)` — run it, observe how
   pandas aligns by index, and note in one sentence what axis=1 means.
4. **merge inner:** join `sales_all` with `menu` on `"item"` (inner).
   Report rows: is it `len(sales_all)`? If any item in sales is missing
   from the menu, the count drops — explain.
5. **merge left:** repeat with `how="left"`. Now every sales row survives;
   missing prices become NaN. Count the NaNs — they mark menu gaps.
6. **one-to-many trap:** `menu` has two prices for `"pizza"` (small, large)
   — check the starter data. Merge again and observe that pizza rows
   **double**. Report how many rows total and explain the cause.
7. **Invoice:** group `sales_all` by `item`, sum `qty`, merge prices, and
   compute `revenue = qty * price`. Print a sorted report with a grand
   total (you may drop rows with missing price, stating so).

## Starter code

```python
import pandas as pd

sales_q1 = pd.DataFrame({
    "item": ["tea", "coffee", "pizza", "cake", "tea", "juice"],
    "qty":  [2, 1, 1, 3, 1, 2],
})
sales_q2 = pd.DataFrame({
    "item": ["coffee", "pizza", "cake", "juice", "tea", "soup"],
    "qty":  [3, 2, 1, 1, 4, 2],
})
menu = pd.DataFrame({
    "item":  ["tea", "coffee", "pizza", "pizza", "cake", "juice"],
    "size":  ["small", "small", "small", "large", "small", "small"],
    "price": [1.20, 2.50, 4.00, 6.50, 4.00, 3.00],
})
staff = pd.DataFrame({
    "item": ["tea", "coffee", "pizza", "cake", "juice"],
    "chef": ["Sana", "Usman", "Ali", "Ayesha", "Bilal"],
})

print(sales_q1.shape, sales_q2.shape, menu.shape)
# your code here
```

## Expected output

- Task 2 shape: `(12, 2)`.
- Task 4: inner merge has **10 rows** — the `"soup"` row from Q2 has no
  menu entry and disappears.
- Task 5: left merge has 12 rows, with exactly 1 NaN price (soup).
- Task 6: pizza rows double → **13 rows** total (10 + 2 extra pizza rows
  from the small/large split... compute and report the actual number with a
  comment explaining it).
- Task 7: revenue report sorted by revenue descending, with grand total
  computed from rows that have a price.

## Questions

1. `concat(..., ignore_index=True)` — when is the flag required, and what
   does it do to the index?
2. Inner vs left merge on `"item"`: which rows differ between the two
   results here, and why?
3. What is a one-to-many merge, and what symptom tells you it happened?
4. Why would `merge` on `"item"` alone be wrong given the menu has two
   pizza sizes? What key would fix it?
5. When would you pick `concat` over `merge`?

## Challenge task

Join `staff` onto your final report so each revenue line shows its chef.
Then answer: "which chef generated the most revenue?" using `groupby
("chef")["revenue"].sum()`. Watch out: the staff table is one row per item,
but your report has one row per item — which merge type keeps the counts
correct, and why?

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| concat rows with ignore_index explained | 4 | 12 rows + reasoning |
| concat columns axis=1 observed | 2 | comment on alignment |
| Inner merge count + gap explanation | 4 | 10 rows, soup identified |
| Left merge + NaN counting | 3 | 12 rows, 1 NaN |
| One-to-many trap detected | 4 | 13 rows + cause explained |
| Invoice report + grand total | 4 | correct math, sorted |
| Answers to questions | 3 | Q3, Q4 correct |
| Challenge: chef revenue | 3 | correct chef + merge choice |
| **Total** | **27** | |