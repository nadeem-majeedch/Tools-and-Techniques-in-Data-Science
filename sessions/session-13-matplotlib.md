# Session 13 — Matplotlib: Figures, Axes, Customization

**Week 7 · Session 13 · Module A · 90 min · CLO-1**

## 1. Learning objectives

By the end of this session, students can:
- Explain why visualization is a core analysis tool, not decoration.
- Create line, bar, scatter, and histogram plots with `plt`/`ax`.
- Use the figure–axes model to control multiple plots in one figure.
- Customize labels, titles, colors, grid, legend, and limits.
- Save publication-quality figures with `savefig` and `dpi`.
- Choose the right chart for the question (relationship → scatter; distribution → histogram; categories → bar).

## 2. Key concepts

- **A chart answers a question** — pick the chart for the question, not the prettiest one.
- **Figure vs. axes:** figure = canvas; axes = one plot area (a figure holds 1..n axes).
- The **pyplot interface** (`plt.plot(...)`) is convenient; the **object interface** (`fig, ax = plt.subplots()`) is explicit and scales to subplots.
- **Three workhorse charts:** line (trend over time), scatter (relationship between two numerics), bar (category values), histogram (distribution of one numeric).
- **`%matplotlib inline`** embeds figures in the notebook.
- Label everything: title, x-label, y-label, legend — an unlabeled chart is noise.

## 3. Detailed lecture notes

**Why visualize?** Numbers hide patterns; pictures reveal them. Anscombe's
quartet is the canonical demo: four datasets with identical mean, variance,
correlation, and regression line — but wildly different scatter plots. If you
only summarize, you miss the point; if you plot, you see it. Visualization is
therefore part of *exploration* (finding problems: outliers, clusters, missing
patterns) and *communication* (the final lifecycle stage).

**The mental model: figure and axes.** A figure is the canvas; axes are the plot
areas on it. `plt.plot(x, y)` creates a figure with one axes implicitly; the
explicit form gives control:
```python
fig, ax = plt.subplots()        # one canvas, one plot
ax.plot(x, y)
fig, axes = plt.subplots(1, 2)  # one canvas, two plots side by side
```
Every customization is a method on `ax`: `set_title`, `set_xlabel`,
`set_ylabel`, `legend`, `grid`, `set_xlim`, `set_ylim`. Colors via `color=`,
style via `linestyle=`, `marker=`. Teach the explicit form early — it makes
subplots trivial later instead of a mystery.

**Choosing the chart.** The single most useful decision framework:
- **Trend over time** (ordered x) → line plot.
- **Two numeric variables, relationship?** → scatter plot.
- **Categories vs. numeric values** → bar plot.
- **Distribution of one numeric variable** → histogram (`ax.hist`).
- Part-to-whole → pie (avoid — bars are easier to read; say so briefly).
Show each on the same dataset (`tips`): line isn't great for tips (no time
axis — use flights), scatter of `total_bill` vs `tip` reveals the relationship,
bar of mean tip by day, histogram of `tip`.

**Taste and honesty.** A few principles: label every axis with units; never
truncate a bar chart's y-axis to exaggerate; use color meaningfully (not
rainbow); 3D charts are usually worse than 2D. Data visualization ethics =
don't mislead. Mention this connects to responsible AI/communication (Session 30).

**Saving and sharing.** `fig.savefig("charts/tips-scatter.png", dpi=150,
bbox_inches="tight")` — commit charts next to notebooks when a report needs
them. `dpi` controls resolution; `bbox_inches="tight"` trims whitespace.

## 4. Important terminology

- **Figure** — the canvas that holds axes.
- **Axes** — one plot area (labels, ticks, data); a figure can contain many.
- **pyplot (`plt`)** — the stateful convenience interface.
- **Object interface** — `fig, ax = plt.subplots()`; explicit and preferred for control.
- **Series/DataFrame `.plot()`** — Pandas' shortcut that calls matplotlib for you.
- **Histogram** — bars over binned numeric ranges; shows distribution.
- **Scatter plot** — points at (x, y) pairs; shows relationships/outliers.
- **Legend** — key mapping colors/markers to series.
- **`savefig`** — export the figure to PNG/PDF/SVG.
- **Anscombe's quartet** — the four datasets proving summary statistics can lie without plots.

## 5. Python examples

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

%matplotlib inline

# --- The four workhorse charts, one axes each ---
fig, axes = plt.subplots(2, 2, figsize=(10, 7))

# 1. Line: trend over time
flights = sns.load_dataset("flights")
monthly = flights.groupby("month")["passengers"].sum()
axes[0, 0].plot(monthly.index, monthly.values, marker="o")
axes[0, 0].set_title("Line: passengers by month")
axes[0, 0].set_xlabel("Month"); axes[0, 0].set_ylabel("Passengers")

# 2. Scatter: relationship
tips = sns.load_dataset("tips")
axes[0, 1].scatter(tips["total_bill"], tips["tip"], alpha=0.6)
axes[0, 1].set_title("Scatter: bill vs tip")
axes[0, 1].set_xlabel("Total bill ($)"); axes[0, 1].set_ylabel("Tip ($)")

# 3. Bar: categories
by_day = tips.groupby("day")["tip"].mean()
axes[1, 0].bar(by_day.index, by_day.values, color="teal")
axes[1, 0].set_title("Bar: mean tip by day")

# 4. Histogram: distribution
axes[1, 1].hist(tips["tip"], bins=20, edgecolor="white")
axes[1, 1].set_title("Histogram: distribution of tips")

fig.tight_layout()
fig.savefig("charts/tips-overview.png", dpi=150, bbox_inches="tight")
```

## 6. Beginner example

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 8, 7]

plt.plot(x, y)
plt.title("My first chart")
plt.xlabel("X"); plt.ylabel("Y")
plt.show()
```

Five lines — and every later chart is this same shape with more options.

## 7. Practical Data Science example

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

%matplotlib inline
tips = sns.load_dataset("tips")

# Question: "Do bigger parties tip a higher percentage?"
# (percent tip is the fair comparison across bill sizes)
tips["tip_pct"] = tips["tip"] / tips["total_bill"] * 100

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(tips["size"], tips["tip_pct"], alpha=0.6)
ax.set_title("Tip percentage vs. party size")
ax.set_xlabel("Party size (people)")
ax.set_ylabel("Tip percentage (%)")
ax.grid(alpha=0.3)

# Annotation: the honest observation
ax.axhline(tips["tip_pct"].mean(), color="red", linestyle="--",
           label=f'mean = {tips["tip_pct"].mean():.1f}%')
ax.legend()
fig.savefig("charts/tip-pct-by-size.png", dpi=150, bbox_inches="tight")
```

## 8. In-class activity (50 min)

In `notebooks/week-07/session-13-matplotlib.ipynb`:

1. **Four charts (20 min):** reproduce the four-workhorse-chart example on `tips`
   — but choose *your own* x/y combinations and write a one-line takeaway under each.
2. **Customization (15 min):** pick one chart and add: title, axis labels with
   units, grid, legend, and a color that isn't the default; then a second subplot
   with a different chart for the same question.
3. **Chart choice (10 min):** given three questions (trend, relationship,
   distribution), predict the chart type; then plot one of them.
4. **Save & check (5 min):** `savefig` to `charts/`; confirm the file exists and opens.

## 9. Lab exercise

**Lab 13** (`../labs/lab-13-matplotlib.md`) — due before Session 14: build the
2×2 dashboard figure on `tips`, label every axis, and save it at 150 dpi.
(Quiz 2 runs later: **Session 29**, covering Weeks 8–14.)

## 10. Common mistakes

- Plotting without labels → a chart no one (including you, later) can read.
- `plt.show()` before `savefig` in some setups → empty saved file (order matters in stateful mode).
- Choosing a line plot for categorical data → meaningless zig-zags.
- Forgetting `%matplotlib inline` → charts in a separate window or missing from the notebook.
- Ignoring `figsize` → tiny, unreadable defaults in notebooks.
- Overplotting: 10,000 points with no `alpha` → a solid blob hiding the pattern.
- Pie charts for comparisons — bars are almost always clearer.

## 11. Short assessment questions

1. What is the difference between a figure and an axes?
2. Which chart type for: (a) temperature over a week; (b) relationship between height and weight; (c) most common grade in a class?
3. What does `bins` control in a histogram?
4. Why is the explicit `fig, ax = plt.subplots()` form better than `plt.plot` alone?
5. How do you save a figure at high resolution with trimmed whitespace?
6. True/False: two datasets with identical summary statistics always look similar when plotted. (False — Anscombe's quartet.)

## 12. CLO mapping

CLO-1: visualization is the "visualize" verb of CLO-1 and half of EDA. The
figure–axes skills here feed directly into the Seaborn session (14), the EDA
case study (15), and the final project's exploration section.

## 13. Suggested homework

- Finish Lab 4 and commit (due Session 14).
- Practice: recreate any chart from your Assignment 1 data with custom labels and saved output.
- Read: Matplotlib "Pyplot tutorial" (matplotlib.org) — the first half only.
- Preview: `sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day")` — Session 14 shows why Seaborn makes this one line.