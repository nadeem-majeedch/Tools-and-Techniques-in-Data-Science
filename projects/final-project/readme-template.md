# <Project Title>

**Team:** <names> · **Semester:** <term> · **Course:** Introduction to Data
Science (3rd semester)

## Summary (3–4 sentences)

<What question you answered, with what data and methods, and the headline
result — e.g., "We predicted penguin species from two bill measurements
with 97% test accuracy using k-NN, and shipped an interactive Streamlit
app that lets anyone explore the measurements.">

## Findings (claim → number)

1. <Finding 1 — e.g., "Gentoo penguins average ~5,050 g vs ~3,700 g for
   the other species (boxplot, Fig 2).">
2. <Finding 2>
3. <Finding 3>

## Data

- Source: <name / URL / API>
- License: <license>
- Retrieval: <keyless API call, download, or seaborn built-in> ·
  retrieved <date>
- Shape: <rows × columns> · cached in `data/`

## How to run

```bash
python -m venv .venv
# Windows: .venv\Scripts\pip install -r requirements.txt
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py        # the app
.venv/bin/jupyter lab eda.ipynb       # the analysis
```

Everything works offline after the first data fetch.

## Repository layout

```
data_loader.py    # fetch → clean → cache
eda.ipynb         # cleaning + EDA (executed)
models.ipynb      # ML model + evaluation (executed)
app.py            # Streamlit app
data/             # cached raw + clean CSVs
report.md         # full report incl. ethics reflection
proposal.md       # original proposal
```

## Model & evaluation

- Model: <e.g., LogisticRegression, scaled features>
- Metric: <e.g., CV accuracy 0.97 ± 0.02; test accuracy 0.96>
- Baseline: <e.g., majority-class 0.44 — model beats it by 0.52>
- Interpretation: <1–2 sentences>

## Known issues / limitations

- <data limitation> · <method limitation> · <app limitation>

## AI-use disclosure

<Per course policy — for each AI-assisted step: tool, prompt summary, how
the output was used, and what you verified yourself. If you did not use
AI, state "No AI assistance used in this project.">

## Reproducibility

- Python <version>; pinned `requirements.txt`.
- `SEED = 42` in every notebook; two consecutive Restart & Run All runs
  produce identical numbers (verified <date>).