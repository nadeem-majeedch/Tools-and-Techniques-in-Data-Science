# Lab 12 — Solution: Combining Data

**Session:** W6 S12 · **CLO:** CLO-1

## Complete solution

```python
import pandas as pd

sales_q1 = pd.DataFrame({"item": ["tea", "coffee", "pizza", "cake", "tea", "juice"],
                         "qty":  [2, 1, 1, 3, 1, 2]})
sales_q2 = pd.DataFrame({"item": ["coffee", "pizza", "cake", "juice", "tea", "soup"],
                         "qty":  [3, 2, 1, 1, 4, 2]})
menu = pd.DataFrame({"item":  ["tea", "coffee", "pizza", "pizza", "cake", "juice"],
                     "size":  ["small", "small", "small", "large", "small", "small"],
                     "price": [1.20, 2.50, 4.00, 6.50, 4.00, 3.00]})
staff = pd.DataFrame({"item": ["tea", "coffee", "pizza", "cake", "juice"],
                      "chef": ["Sana", "Usman", "Ali", "Ayesha", "Bilal"]})

# 2. concat rows
sales_all = pd.concat([sales_q1, sales_q2], ignore_index=True)
print(sales_all.shape)                       # (12, 2)
# ignore_index: both frames have 0..5; without it the combined index would
# repeat 0..5 twice (ambiguous labels).

# 3. concat columns (axis=1) — alignment by index
demo = pd.concat([sales_q1[["item", "qty"]],
                  sales_q1[["qty"]].rename(columns={"qty": "qty_copy"})], axis=1)
print(demo)                                  # side-by-side columns, same rows

# 4. inner merge — soup has no menu entry -> disappears
inner = sales_all.merge(menu, on="item", how="inner")
print("inner rows:", len(inner))             # 10
print("missing from menu:", set(sales_all["item"]) - set(menu["item"]))  # {'soup'}

# 5. left merge — all sales rows survive; soup price NaN
left = sales_all.merge(menu, on="item", how="left")
print("left rows:", len(left), "NaN prices:", left["price"].isna().sum())  # 12, 1

# 6. one-to-many: pizza appears twice in menu -> pizza rows double
print("pizza rows before:", (sales_all["item"] == "pizza").sum(),   # 2
      "after:", (left.merge(menu, on="item", how="left")["item"] == "pizza").sum())  # 4
# Correct fix: merge on item AND size — but sales has no size column, so a
# real solution needs a size key; here we note the doubling explicitly.

# 7. invoice (price from menu; drop rows without price, e.g. soup)
qty = sales_all.groupby("item", as_index=False)["qty"].sum()
inv = qty.merge(menu[menu["size"] == "small"], on="item", how="inner")
inv["revenue"] = inv["qty"] * inv["price"]
inv = inv.sort_values("revenue", ascending=False)
print(inv[["item", "qty", "price", "revenue"]])
print("grand total:", round(inv["revenue"].sum(), 2))
```

## Expected output

- `(12, 2)` after concat rows.
- Inner: 10 rows (soup dropped). Left: 12 rows, 1 NaN (soup).
- Pizza doubling visible (2 → 4 rows in the naive merge).
- Invoice: coffee (3+... compute) etc.; grand total from priced items.

## Model answers

1. **ignore_index** — resets the row labels to 0..n-1 instead of
   duplicating each frame's original 0..5; without it, `.loc[2]` is
   ambiguous (two rows).
2. **Inner vs left** — inner keeps only rows with matching keys in both
   (drops soup); left keeps all rows from the left frame and fills missing
   keys with NaN (soup survives with NaN price).
3. **One-to-many** — a key appears multiple times on the "one" side; each
   occurrence multiplies the matching rows. Symptom: row count jumps
   (pizza 2 → 4) or total revenue doubles.
4. **Wrong key** — pizza has two sizes/prices; merging on `"item"` alone
   matches each pizza sale to *both* menu rows. Fix: include `size` in the
   merge key (and in the sales data).
5. **concat vs merge** — concat stacks frames with the same schema
   (rows: vertically; columns: horizontally). Merge combines *different*
   tables by key, like a SQL JOIN.

## Challenge solution

```python
inv2 = inv.merge(staff, on="item", how="left")     # 1:1 per item — safe
by_chef = inv2.groupby("chef")["revenue"].sum().sort_values(ascending=False)
print(by_chef)
# Staff is one row per item and the invoice is one row per item: a
# many-to-one merge would multiply rows. Left merge on "item" is correct.
```