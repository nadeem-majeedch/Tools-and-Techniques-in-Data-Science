# Lab 08 — Solution: Pandas II

**Session:** W4 S8 · **CLO:** CLO-1

## Complete solution

```python
import pandas as pd
import seaborn as sns
from pathlib import Path

Path("datasets").mkdir(exist_ok=True)

tips = sns.load_dataset("tips")
clean = tips.dropna()
print("shape after dropna:", clean.shape)          # (244, 7)

clean.to_csv("datasets/tips-clean.csv", index=False)
back = pd.read_csv("datasets/tips-clean.csv")
print("shape after round-trip:", back.shape)       # (244, 7)
print(back.dtypes)

# 4. sorting
print(back.nlargest(5, "total_bill"))                       # top-5 bills
print(back.sort_values(["day", "tip"], ascending=[True, False]))

# 5. chained filter
sun_big = back[(back["day"] == "Sun") & (back["total_bill"] > 20)] \
    .sort_values("tip", ascending=False)
print(sun_big)                                              # 6 rows

# 6. JSON export/import
back.head(5).to_json("datasets/tips-sample.json", orient="records")
js = pd.read_json("datasets/tips-sample.json")
print("json shape:", js.shape)                              # (5, 7)

# 7. summary outputs
print("Sat mean tip:", back[back["day"] == "Sat"]["tip"].mean().round(2))
print("highest mean bill day:",
      back.groupby("day")["total_bill"].mean().idxmax())    # Sat
two_thirty = back[(back["size"] == 2) & (back["total_bill"] > 30)]
print("size-2 rows with bill > 30:", len(two_thirty))       # 3
```

## Expected output

- Both shapes `(244, 7)`; dtypes identical before/after (float64 × 3,
  int64, object × 3).
- Top bill 50.81; sorted table as described.
- Filter chain: 6 rows (Sun, bill > 20).
- JSON: `(5, 7)`.
- Sat mean tip ≈ 2.99; highest mean bill day = Sat; 3 rows for size 2 +
  bill > 30.

## Model answers

1. **index=False** — without it, pandas writes the RangeIndex as an extra
   `Unnamed: 0` column; reading back adds a useless column and changes the
   shape.
2. **Object columns** (`sex`, `smoker`, `day`, `time`) survive as objects;
   numeric stay numeric. The classic trap is a column that *looks* numeric
   but has a stray string ("1,234") — it round-trips as object.
3. **NaNs last** is `sort_values` default (`na_position="last"`); change
   with `na_position="first"`.
4. **orient="records"** — a list of dicts (one per row) — the format most
   JSON APIs and web apps expect.
5. Chained: compact, reads top-to-bottom as a pipeline; variables: easier
   to debug each step and reuse intermediates.

## Challenge solution

```python
no_day = clean.drop(columns=["day"])
no_day.to_csv("datasets/tips-noday.csv", index=False)
reloaded = pd.read_csv("datasets/tips-noday.csv")

# merge day back from the ORIGINAL tips using the index
day_only = clean[["day"]].reset_index()          # index becomes a column
joined = reloaded.reset_index().merge(day_only, on="index", how="left")
joined = joined.drop(columns="index")
print(joined.shape)                              # (244, 7)
print(joined["day"].isna().sum())                # 0 — every row matched
# The merge assumes the row order is preserved by the CSV round-trip
# (true here: no sorting, no index shuffling).
```