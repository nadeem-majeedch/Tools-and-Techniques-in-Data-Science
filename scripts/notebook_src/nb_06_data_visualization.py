# Content for notebook 06: Data Visualization.
CELLS = [
    ("md", """# 06 — Data Visualization

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Apply Python and standard data science libraries to datasets.

Numbers hide patterns; pictures reveal them. Visualization is half of EDA
(finding problems and patterns) and the entire *communication* stage. This
notebook teaches Matplotlib (the canvas) and Seaborn (statistical plots that
speak DataFrame).

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain the figure–axes model and why it matters.
2. Create line, scatter, bar, and histogram plots with Matplotlib.
3. Customize titles, labels, colors, legends, and grids.
4. Save publication-quality figures with `savefig`.
5. Use Seaborn's data-frame-native API with `hue` for a third variable.
6. Read boxplots, heatmaps, and pairplots.

---
"""),
    ("code", """# Make sure the datasets/ folder exists next to this notebook.
from pathlib import Path
Path("datasets").mkdir(exist_ok=True)
print("datasets/ ready")
"""),
    ("md", """## Theory: choose the chart for the question

Before any code, decide *what the chart must show*:

| Question | Chart |
|---|---|
| Trend over time | line plot |
| Relationship between two numeric variables | scatter plot |
| Categories vs. a numeric value | bar plot |
| Distribution of one numeric variable | histogram / boxplot |
| Correlations between many numerics | heatmap |
| Everything at once (small dataset) | pairplot |

A chart is an answer to a question. Label everything — title, x-label,
y-label, legend — an unlabeled chart is noise.

---
"""),("code", """# Global setup for every notebook cell in this file
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

%matplotlib inline

tips = sns.load_dataset("tips")
flights = sns.load_dataset("flights")
print("data loaded:", tips.shape, flights.shape)
"""),
    ("md", """## The figure–axes model

- The **figure** is the canvas.
- The **axes** are the plot areas on the canvas (a figure can hold many).
- The explicit form `fig, ax = plt.subplots()` gives you control; the
  shorthand `plt.plot(...)` hides the axes.

Everything you customize is a method on `ax` (`set_title`, `set_xlabel`,
`set_ylabel`, `legend`, `grid`). Using `fig, ax` makes subplots trivial.

---
"""),("code", """# The four workhorse charts, one per subplot
fig, axes = plt.subplots(2, 2, figsize=(11, 8))

# 1. Line: trend over time (monthly passengers, averaged over years)
monthly = flights.groupby("month")["passengers"].mean()
axes[0, 0].plot(monthly.index, monthly.values, marker="o")
axes[0, 0].set_title("Line: passengers by month")
axes[0, 0].set_xlabel("Month"); axes[0, 0].set_ylabel("Average passengers")

# 2. Scatter: relationship between bill and tip
axes[0, 1].scatter(tips["total_bill"], tips["tip"], alpha=0.6)
axes[0, 1].set_title("Scatter: bill vs tip")
axes[0, 1].set_xlabel("Total bill ($)"); axes[0, 1].set_ylabel("Tip ($)")

# 3. Bar: mean tip by day
by_day = tips.groupby("day")["tip"].mean()
axes[1, 0].bar(by_day.index, by_day.values, color="teal")
axes[1, 0].set_title("Bar: mean tip by day")
axes[1, 0].set_ylabel("Mean tip ($)")

# 4. Histogram: distribution of tips
axes[1, 1].hist(tips["tip"], bins=20, edgecolor="white")
axes[1, 1].set_title("Histogram: distribution of tips")
axes[1, 1].set_xlabel("Tip ($)")

fig.tight_layout()
fig.savefig("datasets/tips-overview.png", dpi=120, bbox_inches="tight")
plt.show()
"""),
    ("md", """## Customization: make it readable

Five settings cover most needs: `figsize`, colors, `alpha` (transparency),
grid, and limits. Save with `savefig(dpi=..., bbox_inches="tight")`.

---
"""),("code", """fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(tips["total_bill"], tips["tip"], alpha=0.5, color="#1f77b4")
ax.axhline(tips["tip"].mean(), color="red", linestyle="--", label="mean tip")
ax.set_title("Tip vs bill — every point is one bill")
ax.set_xlabel("Total bill ($)")
ax.set_ylabel("Tip ($)")
ax.grid(alpha=0.3)
ax.legend()
plt.show()
"""),
    ("md", """## Seaborn: statistical plots from DataFrames

Seaborn is built on Matplotlib, but its API matches how data actually lives:
`data=df, x="col"` — no manual extraction. Its superpower is `hue`: one extra
argument encodes a categorical variable by color.

---
"""),("code", """# hue: three variables in one figure
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day")
plt.title("Tip vs bill, colored by day")
plt.show()

# col: same data, separate panels per day
sns.relplot(data=tips, x="total_bill", y="tip", col="day", col_wrap=2)
plt.show()
"""),
    ("md", """## Boxplots and distributions

A **boxplot** shows the median (middle line), the middle 50% of data (box),
whiskers (typical range), and outliers (dots). It is the best quick way to
compare distributions across categories.

---
"""),("code", """fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.boxplot(data=tips, x="day", y="tip", ax=axes[0])
axes[0].set_title("Boxplot: tip distribution by day")

sns.histplot(data=tips, x="tip", kde=True, ax=axes[1])
axes[1].set_title("Histogram + density of tips")

plt.tight_layout()
plt.show()
"""),
    ("md", """## Heatmaps and pairplots

- `sns.heatmap(df.corr(), annot=True)` — the correlation matrix at a glance.
- `sns.pairplot(df, hue=...)` — every numeric pair as a scatter, with
  distributions on the diagonal. The best "first look" at a small dataset.

---
"""),("code", """# Correlation heatmap (numeric columns only)
corr = tips[["total_bill", "tip", "size"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlations in the tips data")
plt.show()

# Pairplot on penguins: can measurements separate the species?
penguins = sns.load_dataset("penguins").dropna()
sns.pairplot(penguins, hue="species")
plt.show()
"""),
    ("md", """## Beginner example: the 5-line chart

---
"""),("code", """import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 8, 7]

plt.plot(x, y, marker="o")
plt.title("My first chart")
plt.xlabel("Day"); plt.ylabel("Value")
plt.show()
"""),
    ("md", """## Intermediate example: a findings chart

A chart that *answers a question*, with annotations. This is the format you
will use in EDA and the final project.

---
"""),("code", """tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100

fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=tips, x="day", y="tip_pct", ax=ax)
ax.axhline(tips["tip_pct"].mean(), color="red", linestyle="--",
           label=f'overall mean = {tips["tip_pct"].mean():.1f}%')
ax.set_title("Tip percentage by day of week")
ax.set_xlabel("Day"); ax.set_ylabel("Tip percentage (%)")
ax.legend()
fig.savefig("datasets/tip-pct-by-day.png", dpi=120, bbox_inches="tight")
plt.show()

# Written takeaway (the markdown habit):
# "Saturday and Sunday sit at or above the overall mean; Friday's median is
#  clearly lower — weekend tables tip a higher percentage."
"""),
    ("md", """## Exercises

---
"""),
    ("md", """### Exercise 1 — Histogram

Plot a histogram of `total_bill` with 30 bins. What shape do you see?
(Answer: roughly right-skewed — most bills are small, a long tail of large
bills.)"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(tips["total_bill"], bins=30, edgecolor="white")
ax.set_title("Distribution of total bills")
ax.set_xlabel("Total bill ($)")
plt.show()
"""),
    ("md", """### Exercise 2 — hue

Recreate the bill-vs-tip scatter with `hue="smoker"`. What does the color
split suggest? (Answer: smokers and non-smokers overlap heavily — smoking is
not clearly related to tipping.)"""),
    ("code", """# your code here
"""),
    ("code", """# Solution
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="smoker")
plt.title("Tip vs bill by smoker status")
plt.show()
"""),
    ("md", """### Exercise 3 — savefig

Make a bar chart of mean `total_bill` by `day`, and save it to
`datasets/exercise3-bar.png` at 150 dpi."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
fig, ax = plt.subplots(figsize=(7, 4))
means = tips.groupby("day")["total_bill"].mean()
ax.bar(means.index, means.values, color="orange")
ax.set_title("Mean bill by day"); ax.set_ylabel("Mean bill ($)")
fig.savefig("datasets/exercise3-bar.png", dpi=150, bbox_inches="tight")
print("saved")
"""),
    ("md", """## Challenge exercise

Using `flights`:

1. Plot the total passengers per **year** as a line chart (aggregate with
   `groupby("year").sum()`).
2. Overlay one line per **month** (`sns.lineplot` with `hue="month"` — or
   keep it simple: 12 lines with `hue`).
3. Add a title, axis labels, and a legend.
4. Save the figure to `datasets/flights-trend.png`.
5. In markdown, state the two most obvious patterns (steady growth; summer
   peak)."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
fig, ax = plt.subplots(figsize=(10, 5))

yearly = flights.groupby("year")["passengers"].sum()
ax.plot(yearly.index, yearly.values, marker="o")
ax.set_title("Total air passengers per year")
ax.set_xlabel("Year"); ax.set_ylabel("Passengers")

sns.lineplot(data=flights, x="month", y="passengers", hue="year", legend=False, alpha=0.4)
fig.savefig("datasets/flights-trend.png", dpi=150, bbox_inches="tight")
plt.show()
"""),
    ("md", """## Recap

- Figure = canvas; axes = plots. Use `fig, ax = plt.subplots()`.
- Chart choice follows the question: line (trend), scatter (relationship),
  bar (categories), histogram (distribution).
- Customize: `set_title`, `set_xlabel`, `set_ylabel`, `legend`, `grid`.
- Save with `savefig(dpi=..., bbox_inches="tight")`.
- Seaborn: `data=df, x="col"`, plus `hue` for a third variable.
- `boxplot`, `heatmap(corr)`, and `pairplot` are the EDA workhorses.
- Every chart needs a written takeaway.

---
"""),
    ("md", """## Questions

1. What is the difference between a figure and an axes?
2. Which chart type for: temperature over a week / height vs weight / most common grade?
3. What does `alpha` do in `scatter`?
4. What does `hue` add to a Seaborn plot?
5. In a boxplot, what do the dots beyond the whiskers represent?
6. What does `sns.pairplot(df, hue="species")` produce?

---
**Next:** notebook 07 — Exploratory Data Analysis.
"""),
]