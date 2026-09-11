# Streamlit · 05 — Charts and Interactive EDA

**Time:** ~75 min · **CLOs:** CLO-1, CLO-3 · **Level:** Beginner
**Prerequisite:** Matplotlib/Seaborn (Module A). Your existing plotting
skills transfer directly.

---

## 1. Three ways to chart in Streamlit

### A. Built-in charts — zero code, data in, chart out

```python
st.line_chart(df)          # line chart of numeric columns
st.bar_chart(df)           # bar chart
st.area_chart(df)          # area chart
```

Give them a dataframe (or a Series) and they plot every numeric column.
Perfect for quick looks; limited control.

### B. Matplotlib — `st.pyplot`

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.hist(df["tip"], bins=20)
ax.set_title("Tip distribution")
st.pyplot(fig)             # <-- pass the figure object
```

**Key detail:** create the `fig` and `ax` with `plt.subplots()`, draw on
`ax`, and pass the figure to `st.pyplot`. Because the app re-runs, the
figure is recreated and re-displayed every time a widget changes.

### C. Seaborn — same rule

```python
import seaborn as sns

fig, ax = plt.subplots()
sns.boxplot(data=df, x="day", y="tip", ax=ax)   # draw into ax!
ax.set_title("Tips by day")
st.pyplot(fig)
```

**Beginner trap:** if you call `sns.boxplot(data=df, x="day", y="tip")`
without `ax=ax`, the plot is drawn into Matplotlib's *current* axes — which
`st.pyplot` may or may not pick up. Always pass `ax=ax` (or use the
returned axes object). The reliable pattern is:

```python
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df["tip"], bins=20, kde=True, ax=ax)
st.pyplot(fig)
```

## 2. Interactive EDA — the pattern

```python
column = st.selectbox("Column", df.select_dtypes("number").columns)
fig, ax = plt.subplots()
sns.histplot(df[column], bins=30, ax=ax)
st.pyplot(fig)
```

Widget picks the column → figure rebuilds → chart updates. **One widget +
one figure = an interactive EDA tool.**

---

# Example 4 — Interactive EDA Dashboard

A complete app: explore a dataset's numeric columns with a histogram and
its categories with a boxplot, filtered by a checkbox.

## Explanation

The app loads the built-in tips dataset, shows quick overview metrics, then
builds two interactive figures: a histogram of whichever numeric column the
user picks, and a boxplot of tip by whichever category the user picks. A
checkbox filters the data first (smokers only) — watch every chart update.

## Code

Save as `app.py`:

```python
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Interactive EDA Dashboard")
st.markdown("Explore the **tips** dataset with live charts.")

# 1) Data
tips = sns.load_dataset("tips")

# 2) Overview metrics
st.header("Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Rows", len(tips))
c2.metric("Mean tip", f"${tips['tip'].mean():.2f}")
c3.metric("Mean bill", f"${tips['total_bill'].mean():.2f}")

# 3) A global filter (checkbox)
only_smokers = st.checkbox("Only smokers")
if only_smokers:
    tips = tips[tips["smoker"] == "Yes"]

# 4) Interactive histogram
st.header("Histogram — pick a numeric column")
num_col = st.selectbox("Numeric column",
                       tips.select_dtypes("number").columns)
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(tips[num_col], bins=30, kde=True, ax=ax)
ax.set_title(f"Distribution of {num_col}")
st.pyplot(fig)

# 5) Interactive boxplot
st.header("Boxplot — tip by category")
cat_col = st.selectbox("Category column", ["day", "sex", "smoker", "time"])
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=tips, x=cat_col, y="tip", ax=ax)
ax.set_title(f"Tip by {cat_col}")
st.pyplot(fig)
```

## Expected result

- Three metric cards: 244 rows, mean tip ≈ $3.00, mean bill ≈ $19.79.
- **Histogram** section: a dropdown of numeric columns (total_bill, tip,
  size); the chart redraws when you switch columns. Default shows the tip
  distribution with a smooth KDE curve.
- **Boxplot** section: a dropdown (day/sex/smoker/time); the boxplot of tip
  by that category redraws on change.
- Tick **Only smokers**: row count drops to 93, the histogram narrows, and
  the boxplots rebuild — every chart reflects the filter.

## Exercise

1. Add a `st.slider("Minimum total bill", 0, 60, 0)` that filters
   `tips = tips[tips["total_bill"] >= min_bill]` before the charts.
2. Change the histogram dropdown to `st.multiselect` of columns and overlay
   two histograms (`ax.hist` twice with `alpha=0.5`), or use
   `sns.histplot(..., multiple="dodge")` with a hue.
3. Add a correlation heatmap for numeric columns
   (`sns.heatmap(tips.select_dtypes("number").corr(), annot=True, ax=ax)`).

## Challenge

Build an **interactive outlier inspector**: a slider for a threshold, then a
scatter plot of `total_bill` vs `tip` with points above the threshold
highlighted in red:

```python
threshold = st.slider("Outlier threshold (tip)", 0.0, 10.0, 5.0)
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=tips, x="total_bill", y="tip", ax=ax)
outliers = tips[tips["tip"] > threshold]
ax.scatter(outliers["total_bill"], outliers["tip"],
           color="red", s=60, label=f"tip > {threshold}")
ax.legend()
st.pyplot(fig)
```

Add a metric showing how many rows are outliers at the current threshold.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Plot doesn't appear | forget `st.pyplot(fig)` — drawing alone doesn't display |
| Seaborn plot "lost" | always pass `ax=ax` when using `plt.subplots()` |
| Chart updates slowly | heavy data processing should be cached (document 6) |
| Empty plot after filtering | the filter emptied the dataframe — check `len(df)` and show an info message |
| Two charts share state | give each its own `fig, ax = plt.subplots()` |

## Checkpoint questions

1. What three arguments does the reliable `st.pyplot` pattern need?
   **CLO-1 · Understand · Easy**
   **Answer:** `fig, ax = plt.subplots()`, drawing on `ax` (with `ax=ax` for
   seaborn), and `st.pyplot(fig)`.
2. Why does the chart update when the user changes a selectbox? *(CLO-1 ·
   Understand · Medium)*
   **Answer:** the rerun model — changing the widget re-runs the script, the
   new value flows into the figure code, and a fresh figure is displayed.
3. What happens if a filter leaves zero rows, and how do you handle it?
   **CLO-1 · Evaluate · Medium**
   **Answer:** the chart becomes empty/errors; guard with `if len(df) == 0:
   st.warning("No data for this filter")` and skip plotting.