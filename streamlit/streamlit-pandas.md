# Streamlit · 04 — Dataframes and Tables: Displaying Data

**Time:** ~60 min · **CLOs:** CLO-1, CLO-3 · **Level:** Beginner
**Prerequisite:** pandas (Module A). Everything here is pandas + Streamlit
wrappers.

---

## 1. Displaying dataframes: `st.dataframe` vs `st.table`

```python
import streamlit as st
import pandas as pd

df = pd.DataFrame({"name": ["Ali", "Sara"], "score": [85, 92]})

st.dataframe(df)     # interactive: sort columns by clicking, scroll, search
st.table(df)         # static: plain table, no interaction
```

| | `st.dataframe` | `st.table` |
|---|---|---|
| Sorting by column | ✅ click headers | ❌ |
| Scrolling / large data | ✅ | ❌ (shows everything) |
| Search box | ✅ | ❌ |
| Style | modern, highlighted | plain, compact |
| When to use | explore data | show a small fixed table (e.g. a result) |

**Rule:** use `st.dataframe` for exploration and large frames; use
`st.table` for small, static results (top-5 rows, a metrics table).

## 2. `st.metric` — one number, with context

```python
st.metric("Average score", 88.5)                       # number + label
st.metric("Average score", 88.5, delta="+3.2 vs last week")
```

`delta` shows an up/down arrow next to the number. Perfect for key findings
at the top of a dashboard: row count, mean, accuracy.

## 3. Pandas integration — the whole point

**Any pandas output displays directly in Streamlit.** No conversion step:

```python
st.write(df.head())                 # smart display of a dataframe
st.dataframe(df.describe())         # stats table
st.write(df["score"].mean())        # plain number
```

Combine with widgets (document 3) and you get *filtering*:

```python
import seaborn as sns

tips = sns.load_dataset("tips")
day = st.selectbox("Day", tips["day"].unique())
filtered = tips[tips["day"] == day]     # plain pandas filter
st.dataframe(filtered)
```

Change the dropdown → new dataframe. That's interactive filtering: **widget
→ pandas → display**, the pattern of every data app.

---

# Example 3 — CSV Data Viewer

A complete app where the user uploads their own CSV and explores it.

## Explanation

The app asks the user for a file (`file_uploader`), reads it with pandas
(`pd.read_csv` accepts the uploaded file object directly), then shows three
layers of information: quick stats (`st.metric`), the data
(`st.dataframe`), and a column summary (`df.describe()`). Everything is
guarded for the "no file yet" case, which happens on the first run.

## Code

Save as `app.py`:

```python
import streamlit as st
import pandas as pd

st.title("📂 CSV Data Viewer")
st.markdown("Upload a CSV file and explore it instantly.")

# 1) Ask for the file
uploaded = st.file_uploader("Choose a CSV file", type=["csv"])

# 2) Nothing uploaded yet -> stop gracefully
if uploaded is None:
    st.info("Please upload a CSV file to begin.")
    st.stop()

# 3) Read it with pandas
df = pd.read_csv(uploaded)

# 4) Quick facts at the top
st.header("Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Rows", len(df))
col2.metric("Columns", len(df.columns))
col3.metric("Missing values", int(df.isna().sum().sum()))

# 5) The data itself
st.header("Data")
st.dataframe(df)

# 6) Numerical summary
st.header("Summary of numeric columns")
st.dataframe(df.describe())
```

## Expected result

- Before upload: an upload box and the blue info message
  "Please upload a CSV file to begin."
- After uploading (try `sns.load_dataset("tips").to_csv("tips.csv")` in a
  notebook first, or use any course CSV):
  - **Overview** — three big numbers: Rows (e.g. 244), Columns (7),
    Missing values (0 or more).
  - **Data** — the full interactive dataframe (sortable, searchable).
  - **Summary of numeric columns** — the `describe()` table (count, mean,
    std, min, quartiles, max).

## Exercise

1. Add a `st.multiselect` of columns, and show only the selected columns
   (`df[selected_columns]`). Handle the empty selection.
2. Add a checkbox "Show first 10 rows only" that displays `df.head(10)`
   instead of the full frame.
3. Add a `st.selectbox("Column")` plus `st.metric("Mean", df[col].mean())`
   for any numeric column chosen.

## Challenge

Extend the viewer to **clean the data**: a checkbox "Drop rows with missing
values" and a selectbox "Choose a numeric column to plot" that shows a
histogram (`st.bar_chart(df[col].value_counts())` is the zero-code option;
Matplotlib comes in document 5). Display "before/after" row counts so the
user sees the effect of cleaning.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| `st.dataframe` and `st.table` look "the same" | they differ in interactivity — use dataframe for exploration |
| App crashes on first run (no file) | guard with `if uploaded is None: st.info(...); st.stop()` |
| `pd.read_csv(uploaded)` fails | check the file is really CSV — `type=["csv"]` on the uploader filters |
| Filter selectbox shows duplicate options | use `df["col"].unique()` as options |
| Dashboard re-reads the file on every click | caching — document 6 (`@st.cache_data`) |

## Checkpoint questions

1. When would you use `st.table` instead of `st.dataframe`? *(CLO-1 ·
   Understand · Easy)*
   **Answer:** for a small static result you don't want the user to sort or
   scroll, like a top-5 list or a summary table.
2. What does `st.metric("Rows", len(df))` display? *(CLO-1 · Understand ·
   Easy)*
   **Answer:** a labeled number — "Rows" with the current dataframe length —
   optionally with a delta arrow.
3. Write the two lines that load an uploaded CSV and show only its first 5
   rows. *(CLO-1 · Apply · Medium)*
   **Answer:**
   ```python
   df = pd.read_csv(uploaded)
   st.dataframe(df.head(5))
   ```