# Streamlit in 30 Minutes

A crash course for Assignment 2. You already know the hard parts (pandas,
seaborn); Streamlit is just a thin layer that turns a Python script into a
web page.

## 1. What Streamlit is

Streamlit runs your Python script **top to bottom** on every interaction
and renders whatever the script prints — text, tables, and figures — as a
web app. You never write HTML. When a user moves a widget, Streamlit
reruns the script with the new widget value. That is the entire mental
model:

> **The script is the app. Widgets are variables. Every rerun redraws the
> page.**

Install once: `pip install streamlit`. Run any script with:
`streamlit run app.py`. Your browser opens `http://localhost:8501`.

## 2. Your first app

```python
# app.py
import streamlit as st

st.title("My first app")
name = st.text_input("Your name")
st.write(f"Hello, {name}!")
```

Run it. Type a name — the page reruns and updates. That's interactivity
for free.

## 3. Text and data

```python
st.header("A header")          # like ## in markdown
st.markdown("**bold** and a [link](https://example.com)")
st.dataframe(df)              # interactive, sortable table
st.write("any object works:", df.head())
st.metric("Mean tip", "$2.99")  # big number card
```

## 4. Widgets you need (sidebar = navigation)

```python
st.sidebar.header("Controls")
cities = st.sidebar.multiselect("Cities", df["city"].unique(),
                                default=df["city"].unique()[:2])
metric = st.sidebar.selectbox("Metric", ["temp_c_mean", "temp_c_max", "temp_c_min"])
start, end = st.sidebar.date_input("Date range", [df["date"].min(), df["date"].max()])
show_raw = st.sidebar.checkbox("Show raw data")
```

Widgets return ordinary Python values (`list`, `str`, `tuple`, `bool`) —
use them to filter your DataFrame exactly as in pandas:

```python
subset = df[(df["city"].isin(cities)) &
            (df["date"] >= pd.Timestamp(start)) &
            (df["date"] <= pd.Timestamp(end))]
```

## 5. Charts

Use your existing matplotlib/seaborn skills and hand the figure to
Streamlit:

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=subset, x="date", y=metric, hue="city", ax=ax)
ax.set_title(f"{metric} by city")
ax.tick_params(axis="x", rotation=30)
st.pyplot(fig)               # <-- the magic line
```

`st.line_chart(df)` exists for quick one-liners, but `st.pyplot` lets you
reuse everything from Sessions 13–14.

## 6. Performance: cache the expensive parts

Without caching, moving a slider re-fetches and re-cleans your data every
rerun (slow, and rude to the API). Wrap the slow function:

```python
import streamlit as st

@st.cache_data
def load_clean_data():
    # fetch or read cache, clean, return DataFrame
    return df

df = load_clean_data()   # runs once; reruns reuse the cached result
```

`@st.cache_data` caches by function arguments, so it also handles
city/date parameters if you put them in the function.

## 7. Layout (enough to look professional)

```python
st.set_page_config(page_title="Weather Explorer", layout="wide")
st.title("Weather Explorer")
st.caption("Hourly Open-Meteo data, cached locally")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Time series")
    st.pyplot(fig1)
with col2:
    st.subheader("Distribution")
    st.pyplot(fig2)

st.sidebar.caption("Data cached from Open-Meteo — see README.")
```

## 8. Debugging checklist

| Symptom | Fix |
|---|---|
| App won't start | `streamlit run app.py` from the repo root; venv active |
| Slider is slow | wrap loading in `@st.cache_data` |
| Widget value ignored | the plot code must read the widget variable |
| Dates don't filter | widgets return `date`; convert with `pd.Timestamp(...)` |
| Figure cut off | `fig.tight_layout()` before `st.pyplot(fig)` |
| Port in use | `streamlit run app.py --server.port 8502` |

## 9. What "done" looks like (rubric cross-check)

- `streamlit run app.py` works on a clean machine (fresh venv + your
  `requirements.txt`).
- Sidebar has ≥ 3 widgets; moving any of them changes the plots/table.
- Loading is cached; the sidebar shows "using cache / fetched".
- Every section has a title and a one-line description.
- README explains source, license, run commands, and your findings.

## 10. Going further (optional)

- `st.plotly_chart` for hover tooltips; `st.tabs` for sections;
  `st.download_button` to export filtered data; deployment via
  Streamlit Community Cloud (needs a public repo). None of these are
  required — the rubric rewards a working, labeled, cached app over fancy
  features.