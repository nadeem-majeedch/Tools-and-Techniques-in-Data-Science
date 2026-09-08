# Streamlit Lab 3 — Interactive EDA Dashboard

**Week:** Module C (Streamlit module) · **CLO-1, CLO-3** · **Time:** ~75 min

## Learning objectives

- Build matplotlib/seaborn figures correctly for Streamlit
  (`fig, ax = plt.subplots()`, `ax=ax`, `st.pyplot(fig)`).
- Make charts respond to widgets (selectbox, slider, checkbox).
- Apply a global filter that updates every chart.

## Problem statement

Build **one app** (`app.py`) on the built-in penguins dataset
(`sns.load_dataset("penguins")`):

1. Overview: 3 metrics (rows, missing values, mean body mass).
2. Interactive histogram of any numeric column (selectbox).
3. Boxplot of body mass by species (fixed) and scatter of bill length vs
   bill depth (fixed), both responding to a **global filter**.
4. Global filter: checkbox "Drop rows with missing values" (penguins has
   2 rows with missing values!) plus a slider "Minimum body mass".

## Tasks

1. Create `streamlit-lab3/app.py`.
2. Load penguins once (cache it — `@st.cache_data`).
3. Metrics: rows, missing values (`df.isna().sum().sum()`), mean body mass
   (`f"{df['body_mass_g'].mean():,.0f} g"`).
4. Histogram: selectbox of numeric columns → `sns.histplot(..., kde=True,
   ax=ax)` → `st.pyplot(fig)`.
5. Fixed charts: boxplot of `body_mass_g` by `species`; scatter of
   `bill_length_mm` vs `bill_depth_mm` (`sns.scatterplot(data=df,
   x="bill_length_mm", y="bill_depth_mm", hue="species", ax=ax)`).
6. **Global filter** (applied before any chart):
   ```python
   drop_missing = st.checkbox("Drop rows with missing values")
   min_mass = st.slider("Minimum body mass (g)", 2700, 6300, 2700)
   if drop_missing:
       df = df.dropna()
   df = df[df["body_mass_g"] >= min_mass]
   ```
7. Verify the missing-value checkbox changes the histogram *and* the
   boxplot and scatter together.

## Expected output (verify all)

- Metrics: 344 rows, 2 missing values, mean body mass ≈ 4201 g
  (before filtering).
- Histogram redraws when switching columns.
- Checking "Drop rows with missing values" → missing count becomes 0 and
  every chart rebuilds.
- Moving the slider upward removes the smallest penguins from all charts.

**Questions to answer in your submission:**

1. Why does every chart update when you change a *single* global filter?
2. What would happen if you forgot `ax=ax` in the seaborn calls?

## Challenge

Add a **correlation heatmap page** using `st.tabs` or a radio: one tab for
the charts above, one tab for a heatmap of numeric correlations
(`sns.heatmap(df.select_dtypes("number").corr(), annot=True, ax=ax)`) that
also respects the global filter.