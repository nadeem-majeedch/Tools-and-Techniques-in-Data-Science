# Streamlit Lab 2 — CSV Data Viewer with Filters

**Week:** Module C (Streamlit module) · **CLO-1, CLO-3** · **Time:** ~75 min

## Learning objectives

- Read an uploaded CSV with `pd.read_csv(uploaded)`.
- Display overview metrics with `st.metric` and data with `st.dataframe`.
- Filter by columns (`multiselect`) and values (`selectbox`) interactively.
- Handle the "no file uploaded yet" first run.

## Problem statement

Build **one app** (`app.py`) — a CSV viewer that:

1. Asks the user to upload a CSV.
2. Shows overview metrics (rows, columns, missing values).
3. Shows the data with a **column filter** (multiselect of columns).
4. Lets the user pick one numeric column and see its `describe()` summary
   and mean as a metric.

Test it with the tips dataset: in a notebook run
`import seaborn as sns; sns.load_dataset("tips").to_csv("tips.csv")` (or
use any CSV from the course's `datasets/`).

## Tasks

1. Create `streamlit-lab2/app.py`.
2. **Upload + guard:**
   ```python
   uploaded = st.file_uploader("Upload a CSV", type=["csv"])
   if uploaded is None:
       st.info("Upload a CSV to begin.")
       st.stop()
   df = pd.read_csv(uploaded)
   ```
3. **Overview:** three `st.metric` cards — rows, columns, missing values.
4. **Column filter:**
   ```python
   cols = st.multiselect("Show columns", df.columns, default=list(df.columns))
   if cols:
       st.dataframe(df[cols])
   else:
       st.info("Pick at least one column.")
   ```
5. **Numeric summary:** a `selectbox` over numeric columns + `st.metric`
   with the mean + `st.dataframe(df[col].describe())`.
6. Run the app, upload `tips.csv`, verify each interaction, screenshot.

## Expected output (verify all)

- Before upload: upload box + info message, nothing crashes.
- After uploading tips.csv: Rows = 244, Columns = 7, Missing = 0.
- Unchecking a column removes it from the table; empty selection shows the
  info message instead of an error.
- Picking `tip` as the numeric column shows mean ≈ 2.998 and the full
  describe() table.

**Questions to answer in your submission:**

1. Why must the app check `uploaded is None` before reading the file?
2. What does `st.multiselect` return when the user removes all columns, and
   why does `if cols:` prevent a crash?

## Challenge

Add a **search box** (`st.text_input`) that filters the dataframe by
substring across all columns (hint: `df.astype(str).apply(lambda row:
row.str.contains(q, case=False).any(), axis=1)`), and show the filtered row
count as a metric so the user sees how many rows match.