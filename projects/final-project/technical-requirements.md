# Final Project — Technical Requirements

## 1. Environment

- Python 3 (record your exact version in `requirements.txt` as a comment:
  `# Python 3.12`).
- One virtual environment per machine (`.venv`), never committed.
- `requirements.txt` at repo root, **pinned** (e.g., `streamlit==1.3x`)
  — generate with `pip freeze` and add the Python-version header.
- The project must run from a fresh environment:
  `python -m venv .venv && .venv/bin/pip install -r requirements.txt`.

## 2. Allowed stack

| Category | Allowed | Not allowed |
|---|---|---|
| Data | pandas, NumPy | — |
| Viz | Matplotlib, Seaborn | — |
| ML | scikit-learn (regression/classification/clustering) | PyTorch, TensorFlow |
| App | Streamlit | Flask, Django, dash |
| Acquisition | requests (keyless APIs), local/public files | paid APIs, scraping without consent |
| AI (optional) | PandasAI, Ollama (local), simple agent loops, n8n | cloud-model APIs requiring keys |

If a tool isn't in the table, ask the instructor before using it.

## 3. Dataset rules

- Openly licensed (CC0/CC BY preferred) and **documented** (source, URL,
  license, retrieval date).
- ≤ 10 MB committed; larger data loads via `data_loader.py` with caching.
- Must work offline after the first fetch (cache in `data/`).
- No personal data without approval; if any, aggregate/de-identify (see
  ethics session W15).

## 4. Recommended repository layout

```
data-science-final-project/
├── README.md              # readme template
├── requirements.txt       # pinned + Python version header
├── data_loader.py         # fetch/cache/clean entry point
├── data/                  # cached raw + clean (gitignored? no — small CSVs commit)
│   ├── raw.csv
│   └── clean.csv
├── eda.ipynb              # executed, restart-safe, seeded
├── models.ipynb           # executed, restart-safe, seeded
├── app.py                 # Streamlit app
├── report.md              # report template
├── proposal.md            # proposal template
└── figures/               # exported figures (optional)
```

(Equivalent alternative: the project lives in `projects/final/` inside
your private course repo — pick one layout and state it in the README.)

## 5. Notebook standards

- Imports in the first cell; `SEED = 42` defined once at the top.
- Every randomized call seeded (`random_state`, `np.random.seed`).
- Restart & Run All must pass with no errors; outputs visible.
- Two consecutive runs must produce identical key numbers.

## 6. Code standards

- Functions over repeated copy-paste; short docstrings.
- No hard-coded paths/URLs scattered in notebooks — use `data_loader.py`.
- No secrets/keys committed; no absolute machine paths.
- Figures: labeled axes, titles, and one-line captions where shown.

## 7. Streamlit app standards

- `streamlit run app.py` works from the repo root in a fresh env.
- ≥ 3 sidebar widgets; every widget changes the displayed output.
- `@st.cache_data` on the load function; cache status visible.
- Data table + at least 2 figures (line/bar + histogram/scatter).

## 8. Git standards

- ≥ 10 commits, meaningful messages, spread over the working period.
- `.gitignore`: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`.
- The commit at the deadline is what's graded; tag it `final-submission`.

## 9. Verification checklist (before submission)

- [ ] Fresh-env install succeeds (`pip install -r requirements.txt`)
- [ ] Both notebooks Restart & Run All with zero errors
- [ ] `streamlit run app.py` starts and shows data
- [ ] README numbers match the notebook's last run
- [ ] License + source documented
- [ ] AI disclosure present (even if "no AI used" — say so)