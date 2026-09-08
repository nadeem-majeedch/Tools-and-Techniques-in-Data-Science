# Lab 13 — Solution: Matplotlib

**Session:** W7 S13 · **CLO:** CLO-1

## Complete solution

```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import pandas as pd
from pathlib import Path

Path("datasets").mkdir(exist_ok=True)
tips = sns.load_dataset("tips")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
# axes is a 2x2 ndarray of Axes; index with [row, col]

# a) mean bill per day — line
daily = tips.groupby("day")["total_bill"].mean()
axes[0, 0].plot(daily.index, daily.values, marker="o")
axes[0, 0].set_title("Mean bill by day")
axes[0, 0].set_xlabel("Day"); axes[0, 0].set_ylabel("Mean bill ($)")

# b) total tip per day — bar
tip_by_day = tips.groupby("day")["tip"].sum()
axes[0, 1].bar(tip_by_day.index, tip_by_day.values,
               color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"])
axes[0, 1].set_title("Total tip by day")
axes[0, 1].set_ylabel("Total tip ($)")

# c) bill vs tip — scatter with alpha
axes[1, 0].scatter(tips["total_bill"], tips["tip"], alpha=0.5)
axes[1, 0].set_title("Bill vs tip")
axes[1, 0].set_xlabel("Total bill ($)"); axes[1, 0].set_ylabel("Tip ($)")

# d) tip histogram
axes[1, 1].hist(tips["tip"], bins=15, edgecolor="white")
axes[1, 1].set_title("Tip distribution")
axes[1, 1].set_xlabel("Tip ($)"); axes[1, 1].set_ylabel("Count")

fig.suptitle("Tips — one week", fontsize=16)
fig.tight_layout()
fig.savefig("datasets/sales-dashboard.png", dpi=150, bbox_inches="tight")

img = mpimg.imread("datasets/sales-dashboard.png")
print("saved image shape:", img.shape)       # e.g. (1050, 1400, 3)
```

## Model answers

1. **Figure vs Axes** — the Figure is the whole canvas/window; an Axes is
   one plotting region within it (with its own ticks/labels). One Figure
   holds many Axes; all plotting happens on Axes.
2. **alpha=0.5** — with 244 points, later points overdraw earlier ones,
   hiding density; translucency reveals the overlap (the tip cloud's
   density shape).
3. **tight_layout** — rescales subplot spacing so titles/labels don't
   overlap or get clipped, especially before saving.
4. **dpi=150** — dots per inch in the saved file; higher dpi = more pixels
   (crisper in print), bigger file.
5. **Bar vs histogram** — a bar chart of *category totals* (day → sum) is
   for comparisons; a histogram shows the *distribution* of one continuous
   variable. Using bars on raw continuous data with one bar per value
   hides shape.

## Challenge solution

```python
fig, ax = plt.subplots(figsize=(8, 6))
for smoker, color in [("Yes", "red"), ("No", "blue")]:
    sub = tips[tips["smoker"] == smoker]
    ax.scatter(sub["total_bill"], sub["tip"], alpha=0.5,
               color=color, label=f"smoker={smoker}")
ax.set_xlabel("Total bill ($)"); ax.set_ylabel("Tip ($)")
ax.set_title("Bill vs tip by smoker status")
ax.legend()
fig.tight_layout()
fig.savefig("datasets/scatter-smoker.png", dpi=150, bbox_inches="tight")
# Reading: the two clouds overlap heavily — smoker status adds little
# visible separation at this granularity.
```