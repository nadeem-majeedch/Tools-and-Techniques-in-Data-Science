# Assignment 2 — API + Data Acquisition + Streamlit Data Application

**Released:** W9 S17 · **Due:** W15 S30 (before session start) · **Individual**
**Weight:** 5% of course grade (part of the 10% assignments component)
**CLO mapping:** CLO-1 (data acquisition/cleaning/EDA/viz), CLO-3
(reproducibility, documentation, responsible data use)

---

## 1. Learning objectives

By completing this assignment you can:

1. Acquire data from a public API (or a documented public dataset) with
   proper error handling and caching.
2. Load and transform the data into a tidy DataFrame with pandas.
3. Clean and reshape it (dtypes, dates, missing values, aggregations).
4. Perform a structured EDA and extract 2–3 findings.
5. Build visualizations that answer specific questions.
6. Build a **Streamlit application** that displays the data and its
   visualizations **interactively**.
7. Add appropriate **user controls/widgets** (selectors, sliders,
   filters) so a non-technical user can explore the data.
8. Document the project in a README that a stranger can run.
9. Commit the project to GitHub with a visible commit history.
10. Apply the course AI-use and reproducibility rules to the whole
    pipeline.

## 2. Problem statement

Your department wants a **self-serve data dashboard**: instead of asking you
for a new chart every week, stakeholders will open a web app and explore the
data themselves. You will build that app end-to-end: fetch data from a
public API or dataset, clean it, analyze it, and ship an interactive
Streamlit application with working controls — plus a README that lets
anyone run it.

## 3. Requirements

- Python 3 + course environment, plus `streamlit` (add it to your
  `requirements.txt`).
- Everything must run offline after the first fetch (cache the data).
- Deliverables in a **private GitHub repository** named
  `assignment-02-data-app` (see GitHub requirements).
- The app must start with `streamlit run app.py` on a clean machine.
- AI assistance permitted only under §11.

## 4. Dataset requirements (choose ONE)

- **Option A — Open-Meteo API (keyless, recommended):** hourly weather for
  2+ cities over ≥ 30 days (Lab 11 pattern). Free, no key, works in class.
- **Option B — any public dataset you can load and document:** e.g., a
  government open-data CSV/JSON, a Kaggle dataset you have permission to
  use, or another keyless API. You must document source, license, and
  retrieval method in the README.
- Required properties: ≥ 2 dimensions to explore (e.g., city × time, or
  region × category), at least one numeric variable, and enough rows that
  filtering is meaningful (≥ 500 rows or a time series ≥ 30 points).
- Cache the fetched data to `data/` so the app (and grading) runs offline
  after the first fetch.

## 5. Tasks

### Part A — Acquisition (15%)
1. Fetch the data via the API (with `params`, timeout, `raise_for_status`)
   or download the public dataset; **cache** it to `data/raw.csv`.
2. On rerun, load from cache if fresh — print `"using cache"` /
   `"fetched"` (visible in the app's sidebar or console).

### Part B — Load & clean (20%)
3. Load into pandas; document shape and dtypes.
4. Clean: dtypes, date parsing, missing values (drop/fill with a logged
   reason), normalize any text columns, remove duplicates.
5. Save the tidy dataset to `data/clean.csv` (`index=False`).

### Part C — EDA (15%)
6. Univariate summaries + at least 2 visualizations (e.g., time series
   line, distribution histogram).
7. At least one **group comparison** (e.g., mean temperature by city) and
   one **relationship** plot (e.g., temperature vs. some second variable).
8. Write **2–3 findings** (claim → number → plot) — these go in the README
   and on the app's "Findings" section.

### Part D — Streamlit application (40%)
9. `app.py` with a sidebar containing **at least three widgets**, e.g.:
   - `st.multiselect` (choose cities/regions),
   - `st.date_input` or `st.slider` (date/time range),
   - `st.selectbox` or `st.radio` (metric to display: mean/max/min),
   - `st.checkbox` (toggle raw-data table / toggle a second plot).
10. The main panel shows: an interactive **line/bar chart** of the
    selected metric over time for the selected cities, a **second plot**
    (histogram or scatter) driven by another widget, and a **data table**
    of the filtered rows (with `st.dataframe`).
11. Use `@st.cache_data` on the load function so reruns don't re-fetch.
12. Label everything (titles, axes, legends); add a one-line description
    per section; show the cache status in the sidebar.

### Part E — Documentation & delivery (10%)
13. README (see §8) and `requirements.txt` with `streamlit` pinned.
14. Commit to GitHub (§7) with a sensible history.

## 6. Expected deliverables

| # | Deliverable | Where |
|---|---|---|
| 1 | `app.py` (complete, runnable Streamlit app) | repo root |
| 2 | `data_pipeline.py` (fetch → clean → cache functions) | repo root |
| 3 | `data/clean.csv` + cached raw file | `data/` |
| 4 | `eda.ipynb` (executed: cleaning + EDA + findings) | repo root |
| 5 | `README.md` (see §8) | repo root |
| 6 | `requirements.txt` (course stack + streamlit) | repo root |

## 7. GitHub requirements

- Private repo `assignment-02-data-app` (invite your instructor).
- **At least 6 commits** spread over the working period — history shows
  the app evolving (e.g., pipeline → EDA → app skeleton → widgets →
  polish → README).
- Meaningful commit messages; push before the deadline; `main` at the
  deadline is graded.
- Do not commit `.venv/`, caches, or API keys.

## 8. README requirements

1. Project title, your name, date.
2. **Data source**: name, URL, license, retrieval method, retrieval date,
   and the caching strategy.
3. What the app does (3–4 sentences) + a screenshot (or, if not possible,
  a description of each panel).
4. **How to run**: create venv → `pip install -r requirements.txt` →
   `streamlit run app.py`.
5. Your 2–3 findings (claim + number).
6. "Known issues / limitations" (e.g., API rate limits, date ranges
   available).
7. **AI-use disclosure**: what you used AI for and what you verified.

## 9. Grading rubric

| Criterion | Max | Notes |
|---|---|---|
| Acquisition + caching | 15 | correct fetch, cache works, offline rerun OK |
| Clean + tidy dataset | 15 | dtypes/dates/missing handled with logged reasons |
| EDA + findings | 15 | 2+ plots, group comparison, 2–3 grounded findings |
| Streamlit app runs | 15 | `streamlit run app.py` works from clean env |
| Widgets (3+) drive the display | 15 | plots/table react to widget state |
| Interactivity & polish | 10 | cache decorator, labels, layout, no hard-coded views |
| README + reproducibility | 10 | all 7 sections; requirements pin streamlit |
| Git history (6+ commits) | 5 | meaningful, spread over time |
| **Total** | **100** | |

Deductions: app crashes on clean run (−15), no caching (−5), widgets that
don't affect output (−10), no README (−10), unexecuted EDA notebook (−10),
AI use without disclosure (see §11).

## 10. CLO mapping

| Task group | CLO | How |
|---|---|---|
| A, B | CLO-1 | acquire and clean data (API + pandas) |
| C | CLO-1 | explore and visualize |
| D | CLO-1, CLO-3 | interactive communication; responsible caching/API use |
| E (§8) | CLO-3 | reproducibility, documentation, AI disclosure |

## 11. Academic integrity rules

- Individual work; discuss ideas freely, write your own code and text.
- **AI use permitted with disclosure** (course policy,
  `../assessment-plan.md`): (1) disclose tool + prompts + usage in the
  README; (2) verify AI-generated code runs and you can explain it;
  (3) never present AI-generated findings without checking them against the
  data.
- Plagiarism of peers or uncredited external code follows institutional
  policy; you may be asked to explain your app in person.
- Exams and quizzes remain closed-AI per policy.

---

## Streamlit quick reference

You have `streamlit-tutorial.md` in this folder — a 30-minute crash course.
Minimum viable app:

```python
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return pd.read_csv("data/clean.csv")

df = load_data()
cities = st.sidebar.multiselect("Cities", df["city"].unique(),
                                default=df["city"].unique()[:2])
metric = st.sidebar.selectbox("Metric", ["temp_c_mean", "temp_c_max"])

subset = df[df["city"].isin(cities)]
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=subset, x="date", y=metric, hue="city", ax=ax)
ax.set_title(f"{metric} by city")
st.pyplot(fig)
st.dataframe(subset)
```

Run it: `streamlit run app.py`.