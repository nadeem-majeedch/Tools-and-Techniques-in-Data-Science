# Streamlit · 07 — The Complete Mini Data Science Dashboard

**Time:** ~90 min · **CLOs:** CLO-1, CLO-2, CLO-3 · **Level:** Intermediate
**Prerequisite:** documents 1–6. This is the capstone: everything combined.

---

## 1. Structure: sidebar + navigation

Real apps organize with a **sidebar** (`st.sidebar`) and **navigation**.
Two beginner-friendly ways to navigate:

```python
page = st.sidebar.radio("Navigate", ["Overview", "EDA", "Model", "About"])
```

or tabs (newer Streamlit):

```python
tab1, tab2, tab3 = st.tabs(["Overview", "EDA", "Model"])
with tab1:
    st.write("Overview content")
```

Radio is the classic pattern — `if page == "EDA":` guards each section.
Tabs look nicer; both are fine. This example uses radio so the flow is
explicit.

## 2. The dashboard skeleton

```text
sidebar (global controls)          main area (changes with the page)
┌──────────────────────┐          ┌──────────────────────────┐
│ page radio           │          │ depends on the selection │
│ dataset filter       │ ───────► │ e.g. EDA page: charts    │
│ (checkboxes,        │          │ Model page: prediction   │
│  sliders)            │          │ About: documentation     │
└──────────────────────┘          └──────────────────────────┘
```

Rule: **global filters live in the sidebar** (they affect every page);
page-specific widgets live in the main area.

---

# Example 6 — Complete Mini Data Science Dashboard

A full end-to-end app on the tips dataset: an overview with metrics, an
interactive EDA page, a small ML page (predict tip size category), and an
About page. This is a miniature version of the final project's app.

## Explanation

Three layers: **sidebar** holds navigation + a global filter (smokers);
**pages** hold page-specific content; the **ML page** trains a tiny
classifier (cached) and predicts from widgets. Everything from documents
3–6 appears here — widgets, pandas filtering, charts, caching, metrics,
session-state-free by design (no memory needed).

## Code

Save as `app.py`:

```python
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

st.set_page_config(page_title="Tips Dashboard", page_icon="🍽️")
st.title("🍽️ Tips — Mini Data Science Dashboard")

# ---------- 1. Data (cached) ----------
@st.cache_data
def load_data():
    return sns.load_dataset("tips")

df = load_data()

# ---------- 2. Global filter (sidebar) ----------
st.sidebar.header("Global filters")
only_smokers = st.sidebar.checkbox("Only smokers")
if only_smokers:
    df = df[df["smoker"] == "Yes"]

# ---------- 3. Navigation ----------
page = st.sidebar.radio("Page", ["Overview", "EDA", "Model", "About"])

# ---------- 4. Pages ----------
if page == "Overview":
    st.header("Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", len(df))
    c2.metric("Mean tip", f"${df['tip'].mean():.2f}")
    c3.metric("Mean bill", f"${df['total_bill'].mean():.2f}")
    c4.metric("Tip rate", f"{100 * df['tip'].sum() / df['total_bill'].sum():.1f}%")
    st.dataframe(df)

elif page == "EDA":
    st.header("Exploratory Analysis")
    num_col = st.selectbox("Numeric column",
                           df.select_dtypes("number").columns)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df[num_col], bins=30, kde=True, ax=ax)
    ax.set_title(f"Distribution of {num_col}")
    st.pyplot(fig)

    cat_col = st.selectbox("Compare by", ["day", "sex", "smoker", "time"])
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x=cat_col, y="tip", ax=ax)
    ax.set_title(f"Tip by {cat_col}")
    st.pyplot(fig)

elif page == "Model":
    st.header("Predict Tip Size Category")

    @st.cache_data
    def train_model(data):
        # Small but honest model: big tip = above the median tip
        X = data[["total_bill", "size"]]
        y = (data["tip"] > data["tip"].median()).astype(int)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42)
        model = KNeighborsClassifier(n_neighbors=5)
        model.fit(X_train, y_train)
        return model, X_test, y_test

    model, X_test, y_test = train_model(df)
    accuracy = model.score(X_test, y_test)
    st.caption(f"Model accuracy on test data: {accuracy:.1%}")

    bill = st.slider("Total bill ($)", 0.0, 60.0, 20.0, step=0.5)
    size = st.slider("Party size", 1, 6, 2)
    prediction = model.predict([[bill, size]])[0]
    st.success("Predicted: **large tip** 🎉" if prediction == 1
               else "Predicted: **small tip**")

else:  # About
    st.header("About this app")
    st.markdown("""
    - Built with **Streamlit** — 100% Python, no HTML/CSS/JS.
    - Dataset: `seaborn.load_dataset("tips")` (244 restaurant bills).
    - Model: k-NN predicting whether the tip is above the median.
    - Explore more: the sidebar filters apply to **every page**.
    """)
```

## Expected result

- **Sidebar** on the left: a "Global filters" section (Only smokers
  checkbox) and a "Page" radio with four options.
- **Overview** — four metric cards (244 rows, mean tip ~$3.00, mean bill
  ~$19.79, tip rate ~14.8%) and the full dataframe.
- **EDA** — the two interactive charts from Example 4 (histogram + boxplot).
- **Model** — the accuracy caption (k-NN, seed 42, ~85–90% depending on the
  split) and two sliders; every change instantly re-predicts.
- **About** — the documentation text.
- Tick **Only smokers** on any page → row count and every chart update
  together.

## Exercise

1. Add an "Only weekend" checkbox to the sidebar and filter
   `df = df[df["day"].isin(["Sat", "Sun"])]`.
2. Add a fourth page, "Correlations", with a heatmap of numeric columns.
3. Add `st.session_state` to the Model page: count how many predictions the
   user has made and show it ("You have made N predictions").

## Challenge

Extend the dashboard to a **second dataset**: a sidebar selectbox
("Dataset": tips / penguins) that switches everything — overview metrics,
EDA columns, and the model target — using one `load_data(name)` cached
function. Keep the ML page generic (pick numeric features with a
`multiselect` and predict above/below median of a target chosen by the
user). This "one app, many datasets" pattern is the final project's
starting point.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Sidebar widgets appear in the main area | prefix with `st.sidebar.` |
| Filters only affect one page | apply filters *before* the page branches, as in the example |
| Radio navigation shows all pages | wrap each page's content in `if page == "...":` blocks |
| Model retrains on navigation | cache training; the radio change is a rerun like any other |
| App gets messy and long | keep the skeleton: data → filters → navigation → pages |

## Checkpoint questions

1. Why do global filters belong in the sidebar? *(CLO-1 · Understand ·
   Medium)*
   **Answer:** they are visible and stable across pages, and the user expects
   them to stay put while browsing — putting them inline would scatter them
   across pages.
2. In the dashboard, why does the Model page's cached model retrain when
   the "Only smokers" filter changes? *(CLO-2 · Analyze · Medium)*
   **Answer:** the cached function's argument is the *filtered* dataframe,
   which changed — so the cache key changed and training re-ran. That is
   the correct behaviour: a different dataset needs a different model.
3. List the four structural layers of the dashboard. *(CLO-1 · Understand ·
   Easy)*
   **Answer:** cached data loading → sidebar global filters → navigation →
   page-specific content.