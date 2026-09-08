# Lab 3 — Solution: Interactive EDA Dashboard (Penguins)

## Complete app.py

```python
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Penguins — Interactive EDA Dashboard")

# Data loaded once (cached — not on every rerun)
@st.cache_data
def load_data():
    return sns.load_dataset("penguins")

df = load_data()

# ---------- Global filter (applies to EVERY chart below) ----------
st.header("Global filter")
drop_missing = st.checkbox("Drop rows with missing values")
min_mass = st.slider("Minimum body mass (g)", 2700, 6300, 2700, step=100)

if drop_missing:
    df = df.dropna()
df = df[df["body_mass_g"] >= min_mass]

# ---------- Overview ----------
st.header("Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Rows", len(df))
c2.metric("Missing values", int(df.isna().sum().sum()))
c3.metric("Mean body mass", f"{df['body_mass_g'].mean():,.0f} g")

# ---------- Interactive histogram ----------
st.header("Histogram")
num_col = st.selectbox("Numeric column", df.select_dtypes("number").columns)
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df[num_col], bins=30, kde=True, ax=ax)
ax.set_title(f"Distribution of {num_col}")
st.pyplot(fig)

# ---------- Fixed charts ----------
st.header("Body mass by species")
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=df, x="species", y="body_mass_g", ax=ax)
st.pyplot(fig)

st.header("Bill length vs bill depth")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df, x="bill_length_mm", y="bill_depth_mm",
                hue="species", ax=ax)
st.pyplot(fig)
```

## Expected numbers (penguins, unfiltered)

- 344 rows, 2 missing values, mean body mass ≈ 4,201 g.
- After checking "Drop rows with missing values": 342 rows, 0 missing.
- Raising `min_mass` shrinks every chart together (global filter applied
  before any chart is drawn).

## Model answers to the questions

1. **Why does every chart update with one filter change?** The filter lines
   run *before* the charts in the script, and a widget change re-runs the
   whole script — so every chart is rebuilt from the already-filtered
   dataframe. Order matters: filters first, charts second.
2. **What if you forgot `ax=ax` in seaborn?** Seaborn would draw into
   Matplotlib's *implicit current axes*, which `st.pyplot(fig)` may not
   capture reliably — the chart can come out empty, cropped, or on the
   wrong figure. `fig, ax = plt.subplots()` + `ax=ax` + `st.pyplot(fig)`
   makes the target explicit.

## Challenge solution (tabs + heatmap)

```python
tab1, tab2 = st.tabs(["Charts", "Correlations"])
with tab1:
    # ...all charts from above...
with tab2:
    st.header("Correlation heatmap")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(df.select_dtypes("number").corr(), annot=True, ax=ax)
    st.pyplot(fig)
```