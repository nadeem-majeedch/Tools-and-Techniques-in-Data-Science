# Lab 03 — Solution: Jupyter in Depth

**Session:** W2 S3 · **CLO:** CLO-1

## Complete solution

Cell 1 (markdown):

```markdown
# Tips EDA — notebook hygiene practice
**Name:** <student>  **Date:** <date>
A restart-safe notebook demonstrating clean Jupyter practice.
```

Cell 2 (imports):

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
```

Cell 3 (data):

```python
tips = sns.load_dataset("tips")
print("shape:", tips.shape)
tips.head()
```

Cell 4 (analysis):

```python
mean_tip_by_day = tips.groupby("day")["tip"].mean().round(2)
mean_tip_by_day
```

Cell 5 (markdown — the table):

```markdown
| Day | Mean tip |
|---|---|
| Thur | 2.77 |
| Fri | 2.73 |
| Sat | 2.99 |
| Sun | 3.26 |
```

Cell 6 (timing):

```python
%timeit tips["tip"].mean()
```

Cell 7 (the trap — must be *fixed*, not deleted):

```python
secret = 42          # fix: define before use
print(secret)        # was: NameError before the fix
```

Cell 8 (markdown — challenge report):

```markdown
## Report
- The dataset has **244** rows and 7 columns.
- **Sunday** has the highest mean tip (≈ $3.26).
- `total_bill` ranges from **3.07** to **50.81**.
```

## Expected output

- Cell 3: `shape: (244, 7)` + 5-row preview.
- Cell 4: `Fri 2.734848, Sat 2.993103, Sun 3.255813, Thur 2.771452`
  (rounded 2.73 / 2.99 / 3.26 / 2.77).
- Cell 6: something like `12.1 µs ± 0.4 µs per loop (mean ± std. dev. of 7
  runs, 100000 loops each)`.
- Cell 7: `NameError: name 'secret' is not defined` **before** the fix;
  `42` after.
- Final Restart & Run All: no errors.

## Model answers

1. **Kernel** = the Python process executing cells; restart resets its
   memory (all variables), giving a clean slate.
2. **Order matters** because cells share one namespace; a cell using a
   variable defined later only works if run in the "right" order — which a
   restart-safety check exposes.
3. `%timeit` repeats a statement many times and reports the best/average
   distribution; `%%time` times a single execution of the whole cell.
4. **NameError in a classmate's copy** — almost always a cell run out of
   order (hidden state): the variable exists in your kernel but not in
   theirs. Fix: Restart & Run All.
5. **Imports first** = one place to see dependencies; no cell depends on a
   library imported midway; clean restart-safety.

## Challenge solution

The markdown report cell above; verify it stays valid after Restart & Run
All (it must not reference variables — it's static text).