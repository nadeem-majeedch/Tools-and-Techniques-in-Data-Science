# Lab 2 — Solution: CSV Data Viewer with Filters

## Complete app.py

```python
import streamlit as st
import pandas as pd

st.title("CSV Data Viewer")

# 1) Upload + graceful first run
uploaded = st.file_uploader("Upload a CSV", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV to begin.")
    st.stop()

df = pd.read_csv(uploaded)

# 2) Overview metrics
st.header("Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Rows", len(df))
c2.metric("Columns", len(df.columns))
c3.metric("Missing values", int(df.isna().sum().sum()))

# 3) Column filter (multiselect -> list!)
st.header("Data")
cols = st.multiselect("Show columns", df.columns, default=list(df.columns))
if cols:
    st.dataframe(df[cols])
else:
    st.info("Pick at least one column.")

# 4) Numeric summary
st.header("Numeric summary")
num_cols = df.select_dtypes("number").columns
if len(num_cols) > 0:
    col = st.selectbox("Numeric column", num_cols)
    st.metric(f"Mean of {col}", f"{df[col].mean():.3f}")
    st.dataframe(df[col].describe())
else:
    st.warning("No numeric columns found in this file.")
```

## Expected numbers (tips.csv)

- Rows 244, Columns 7, Missing 0.
- `tip` column: mean 2.998, describe() shows count 244, std ≈ 1.38,
  min 1.00, max 10.00.

## Model answers to the questions

1. **Why check `uploaded is None`?** On the first run (and before the user
   picks a file) the widget returns `None` — calling `pd.read_csv(None)`
   would crash. The guard shows a friendly message and `st.stop()`s the
   script before anything touches the file.
2. **What does an empty multiselect return?** `[]` — and
   `df[[]]` raises `KeyError`/`UndefinedVariableError`-style failures.
   `if cols:` is False for an empty list, so the app shows an info message
   instead of crashing.

## Challenge solution (search box)

```python
search = st.text_input("Search all columns (substring)")
if search:
    mask = df.astype(str).apply(
        lambda row: row.str.contains(search, case=False).any(), axis=1)
    filtered = df[mask]
    st.metric("Matching rows", len(filtered))
    st.dataframe(filtered)
else:
    st.dataframe(df[cols])
```