# Streamlit Module — Building Data Apps in Pure Python

**Audience:** shared by BS Data Science 3rd semester (Introduction to Data
Science) and MS Data Science 1st semester (Tools and Techniques in Data
Science) · **Level:** Beginner
**Prerequisites:** pandas, Matplotlib/Seaborn, basic scikit-learn (Module A/B)
**No HTML, CSS, or JavaScript required — Streamlit apps are 100% Python.**

## What this module is

Streamlit turns a plain Python script into an interactive web app. This
module teaches the complete beginner path: from "what is it and why do data
scientists use it" to a working machine-learning prediction app and a full
mini dashboard.

## Module map

| # | Document | You learn | Example |
|---|---|---|---|
| 1 | `streamlit-introduction.md` | What/why Streamlit, install, run, first app | 1 — Hello Data Science |
| 2 | `streamlit-tutorial.md` | Guided 45-min tour: app structure, reruns, first widgets | build your first app |
| 3 | `streamlit-widgets.md` | All input widgets: button, checkbox, selectbox, slider, file uploader… | 2 — Interactive calculator |
| 4 | `streamlit-pandas.md` | Dataframes, tables, metrics, CSV viewer | 3 — CSV data viewer |
| 5 | `streamlit-visualization.md` | Built-in charts, Matplotlib & Seaborn in apps | 4 — Interactive EDA dashboard |
| 6 | `streamlit-ml-app.md` | Caching, session state, ML predictions | 5 — ML prediction app |
| 7 | `streamlit-dashboard-project.md` | Sidebars, navigation, combining everything | 6 — Mini data science dashboard |
| 8 | `streamlit-faq.md` | Common questions and gotchas | — |
| 9 | `streamlit-cheatsheet.md` | One-page reference of every element taught | — |
| 10 | `labs/` | 4 practical labs (student version + solutions) | — |

## The six progressive examples

| Example | File | Skill added |
|---|---|---|
| 1 · Hello Data Science | `streamlit-introduction.md` | first app, text elements |
| 2 · Interactive calculator | `streamlit-widgets.md` | number input, selectbox, button |
| 3 · CSV data viewer | `streamlit-pandas.md` | file upload, dataframe, metrics |
| 4 · Interactive EDA dashboard | `streamlit-visualization.md` | charts + interactive filters |
| 5 · ML prediction app | `streamlit-ml-app.md` | caching, session state, predictions |
| 6 · Mini data science dashboard | `streamlit-dashboard-project.md` | sidebar, navigation, full pipeline |

Each example has: explanation → code → expected result → exercise → challenge.

## Where this fits in the course

- **Assignment 2** (`../assignments/assignment-02-api-streamlit-app/`) — the
  app you build there uses exactly the skills from documents 3–5; its
  bundled `streamlit-tutorial.md` is a shorter, assignment-specific version
  of document 2.
- **Module C topic 11** (`../module-c/topic-11-ai-in-streamlit.md`) — how to
  add an AI chat box (local Ollama) to the apps you build here.
- **Final project** — the required interactive Streamlit app
  (`../projects/final-project/`) is documents 4–7 combined with real data.

## Quick start

```bash
pip install -r requirements.txt        # includes streamlit
streamlit hello                        # demo app — proves the install
streamlit run app.py                   # run your own app (Ctrl+C to stop)
```

Every example in this module is a complete, runnable script. Save it as
`app.py` and run `streamlit run app.py`.