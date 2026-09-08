# Lab 06 — Solution: NumPy II

**Session:** W3 S6 · **CLO:** CLO-1

## Complete solution

```python
import numpy as np

np.random.seed(11)
temps = np.random.normal(loc=15, scale=8, size=(30, 24))
temps = np.clip(temps, -5, 40)
print("shape:", temps.shape)

# 2-3. freeze mask
froze = temps.min(axis=1) < 0              # True/False per day
print("days that froze:", np.sum(froze))
print("freezing day indices:", np.argwhere(froze).ravel())
print("coldest freezing hour:", temps[froze].min().round(2))

# 4. aggregations
print("min:", temps.min().round(2), "max:", temps.max().round(2))
print("mean:", temps.mean().round(2), "std:", temps.std().round(2))
print("p10/p90:", np.percentile(temps, [10, 90]).round(2))

# 5. warmest hour
day, hour = np.unravel_index(temps.argmax(), temps.shape)
print("warmest (day, hour):", day, hour)

# 6. broadcasting normalization (mean/std along the hour axis)
mu = temps.mean(axis=0)
sd = temps.std(axis=0)
normalized = (temps - mu) / sd              # (30,24) - (24,) broadcasts
print("normalized mean/std:", round(normalized.mean(), 6),
      round(normalized.std(), 6))

# 7. noise on a copy
noisy = temps + np.random.normal(0, 0.5, temps.shape)
print("noisy differs:", np.any(noisy != temps))
```

## Expected output

```
shape: (30, 24)
days that froze: <count for seed 11 — non-zero>
freezing day indices: [ ... ]
coldest freezing hour: <-5.0 or close (clip floor)>
min/max/mean/std: plausible for N(15, 8) clipped to [-5, 40]
p10/p90: ~5 and ~25
warmest (day, hour): <fixed pair for seed 11>
normalized mean/std: 0.0 and 1.0
noisy differs: True
```

## Model answers

1. **Flattening** — boolean indexing with a 1-D mask over a 2-D array
   returns a 1-D array of the *selected* elements (row order preserved).
   You get the values, not the structure.
2. **Percentile over mean** — percentile is robust to outliers and
   describes the distribution's shape (e.g., "10% of hours are below 5°");
   the mean alone hides spread.
3. **Shapes** — both `(24,)`; NumPy broadcasts `(24,)` against `(30, 24)`
   by aligning trailing dimensions: `(24,)` → treated as `(1, 24)` →
   stretched to `(30, 24)`.
4. **`&` vs `and`** — `&` is the element-wise boolean operator on arrays;
   `and` is Python's short-circuit operator on single booleans and would
   raise on arrays ("truth value ambiguous").
5. **unravel_index** — converts a flat index (from `argmax`) into the
   multi-dimensional coordinates (`day, hour`) of the original shape.

## Challenge solution

```python
flat = (temps > 25).ravel()
idx = np.argwhere(flat).ravel()
if len(idx) == 0:
    print("no hours above 25")
else:
    gaps = np.diff(idx)
    # streak ends where the gap is > 1
    ends = np.argwhere(gaps > 1).ravel()
    if len(ends) == 0:
        start = idx[0]; length = len(idx)
    else:
        # lengths of each run; pick the max
        lengths = np.diff(np.append(ends, len(idx) - 1)) + 1
        ...
# simpler idiomatic version:
groups = np.split(idx, np.argwhere(gaps > 1).ravel() + 1)
longest = max(groups, key=len)
print("streak length:", len(longest))
day, hour = np.unravel_index(longest[0], temps.shape)
print("starts at (day, hour):", day, hour)
```