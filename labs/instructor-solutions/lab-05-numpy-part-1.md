# Lab 05 — Solution: NumPy I

**Session:** W3 S5 · **CLO:** CLO-1

## Complete solution

```python
import numpy as np

np.random.seed(7)
footfall = np.random.randint(0, 60, size=(3, 24))

print("shape:", footfall.shape)   # (3, 24): 3 stores x 24 hours
print("ndim:", footfall.ndim)     # 2
print("dtype:", footfall.dtype)   # int64
print("size:", footfall.size)     # 72 elements

# 2. morning slice (hours 8-11 inclusive -> columns 8:12)
morning = footfall[:, 8:12]
print("morning:\n", morning)      # (3, 4) block

# 3. one store's day
store2 = footfall[1]              # 1-D: shape (24,)
print("store2 shape:", store2.shape)
store2_2d = footfall[1].reshape(1, -1)   # (1, 24) — keeps 2-D
print("store2 reshaped:", store2_2d.shape)

# 4. per-store totals: axis=1 sums ACROSS columns (hours) -> one number per row
store_totals = footfall.sum(axis=1)
print("per-store totals:", store_totals, "sum:", footfall.sum())

# 5. per-hour mean across stores: axis=0 sums ACROSS rows (stores)
hour_means = footfall.mean(axis=0)
print("per-hour means:", hour_means.round(1))

# 6. busiest hour (highest total across stores)
col_sums = footfall.sum(axis=0)
print("busiest hour index:", np.argmax(col_sums))
print("check:", col_sums[np.argmax(col_sums)] == col_sums.max())

# 7. dtype conversion
as_float = footfall.astype(float) + 0.5
print("new dtype:", as_float.dtype)   # float64
```

## Expected output

```
shape: (3, 24)
ndim: 2
dtype: int64
size: 72
morning: (3, 4) block of ints
store2 shape: (24,)
store2 reshaped: (1, 24)
per-store totals: [ ... ] sum: [total of all 72]
busiest hour index: <0-23, deterministic for seed 7>
new dtype: float64
```

(With `seed(7)` all printed arrays are fixed; students can verify against
their own run.)

## Model answers

1. `axis=0` = down the rows (collapse rows, keep columns): per-hour
   summaries across stores. `axis=1` = across the columns: per-store
   summaries. `sum(axis=1)` removes the hour axis.
2. **1-D row** — indexing with a single integer drops the dimension by
   design; `reshape(1, -1)` (or `footfall[[1]]`) restores 2-D.
3. **dtype** — every element's type; one array = one dtype, because
   operations are vectorized under that type. Mixed types would force
   object arrays and kill performance.
4. **Same result** — `footfall[1, 8:12]` and `footfall[1][8:12]` both give
   store 2's hours 8–11; the first is a single indexing expression
   (preferred — one pass).
5. **Seed** — makes the "random" data reproducible for grading and for
   comparing with classmates.

## Challenge solution

```python
busy = footfall > 40                      # boolean array, same shape
busy_hours = busy.sum(axis=1)             # count True per store
print("busy hours per store:", busy_hours)
print("busiest store index:", np.argmax(busy_hours))
# busy is bool: sum() counts True as 1, False as 0 — no cast needed.
```