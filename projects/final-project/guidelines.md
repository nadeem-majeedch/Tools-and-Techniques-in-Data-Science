# Final Project — Guidelines

**Weight:** 15% of the course grade (the project sits inside the **40% final**
institutional bucket, alongside the 25% final exam) · **Teams:** 2–3 students · **CLOs:** 1, 2, 3

## 1. What you must build

An end-to-end data science project, in order:

```
Problem → Data acquisition → Cleaning → EDA → Visualization →
Basic ML → Evaluation → Streamlit app → AI-assisted analysis
(optional: LLM / agent / n8n) → Documentation → GitHub
```

### Required minimum components (all 13 mandatory)

1. **Problem definition** — a specific, answerable question with a stated
   audience and decision.
2. **Dataset / data source** — documented, openly licensed (no paid APIs).
3. **Data acquisition** — reproducible loading (script/function, cached).
4. **Data cleaning** — dtypes, missing values, duplicates, with a logged
   reason per decision.
5. **EDA** — univariate + group comparisons + correlations.
6. **Visualization** — at least 3 labeled figures answering specific
   questions.
7. **Basic ML model** — at least one scikit-learn model (regression,
   classification, or clustering) with a train/test split.
8. **Model evaluation** — honest metric(s), a baseline comparison, and a
   one-paragraph interpretation.
9. **Interactive Streamlit application** — widgets that filter/explore the
   data and show your figures/tables (see `../assignments/assignment-02-api-streamlit-app/streamlit-tutorial.md`).
10. **GitHub repository** — commit history showing the project evolving.
11. **README** — runnable-by-a-stranger documentation (template provided).
12. **Final report** — ~1,000 words incl. ethics + reproducibility
    reflection (template provided).
13. **Presentation** — 6 minutes + 2–3 minutes Q&A (template provided).

### Optional advanced components (pick 0+; at least one recommended for CLO-3)

- PandasAI natural-language queries (audited and logged)
- Ollama local model assisting an analysis step
- LLM prompt/verification protocol applied to your own work
- A simple AI agent loop over your data tools
- n8n (or equivalent) automation for data collection/processing

None are required — the mandatory AI-assisted requirement is the
**AI-assisted analysis** step (an LLM/PandasAI/Ollama-assisted step with
disclosure + verification), which can be as small as one documented,
verified query.

## 2. Teams

- 2–3 students. All members must be able to explain any part of the
  project (viva, §7).
- Roles are encouraged but every member contributes code: e.g., data/EDA,
  modeling, app, documentation — with **commit history** as evidence.
- Peer evaluation forms are submitted at presentation time
  (`peer-evaluation-form.md`) and inform the individual component of the
  grade.

## 3. Scope limits (what "achievable" means)

- **No paid APIs, no API keys, no cloud services** required. Use keyless
  APIs (e.g., Open-Meteo), public datasets, or the course built-ins.
- **No advanced frameworks**: pandas, NumPy, Matplotlib, Seaborn,
  scikit-learn, Streamlit, and (optionally) requests, PandasAI, Ollama,
  n8n are the allowed stack. No PyTorch/TensorFlow/Django/Flask.
- Datasets: ≤ 10 MB committed; larger datasets load via a script with a
  documented source. License must permit reuse (CC0/CC BY preferred).
- Everything must run offline after the first fetch (cache your data).

## 4. Milestones & deadlines

| Milestone | Due | Gate |
|---|---|---|
| Kickoff, teams, draft question | W12 S23 (in class) | Lab 23 workbook |
| **Proposal** | W13 S26 | graded gate (5% of project) |
| Reproducible repo layout + seeds | W12 S24 (workshop) | Lab 24 |
| Mid-project check-in (cleaning + EDA done) | W14 S28 (in class) | informal |
| **Presentation** | W16 S31–32 | graded |
| **Final submission** (report + repo) | W16 S32 | graded |

Proposal is a gate: no proposal, no project grade — see rubric.

## 5. Submission

- Private GitHub repository: `data-science-final-project` (or
  `projects/final/` inside your private course repo — pick one, tell your
  instructor). Invite the instructor.
- At least **10 commits** spread over the working period.
- Final submission bundle: repo (at deadline commit) + report + README +
  executed notebooks + app runnable via `streamlit run app.py`.
- Late policy: −10%/day per `../assessment-plan.md`.

## 6. Academic integrity & AI use

Course policy (`../assessment-plan.md`) applies in full:

1. **Disclose** every AI-assisted step (tool, prompt, how used) in the
   README and report.
2. **Verify** AI-generated code runs and you can explain it; findings must
   be checked against the data (the verification protocol from Session 25).
3. Plagiarism of peers/external code is subject to institutional policy.
4. You may be asked to explain any line of your work in the viva; being
   unable to explain AI-generated code is treated as unverified use.

## 7. Viva

After the presentation, any team member may be asked 2–4 questions from
`viva-questions.md` (own-component questions for each member). The viva is
worth 10% of the project grade and is individual.

## 8. Deliverables checklist (submit this in your repo)

- [ ] Proposal (one page, proposal template)
- [ ] GitHub repo with ≥ 10 commits and instructor invited
- [ ] `data/` or `data_loader.py` (cached, documented source + license)
- [ ] `eda.ipynb` and `models.ipynb` — executed, restart-safe, seeded
- [ ] `app.py` — Streamlit app with widgets, `@st.cache_data`
- [ ] `requirements.txt` with pinned versions + Python version header
- [ ] `README.md` (readme template)
- [ ] `report.md` (report template, incl. ethics + AI disclosure)
- [ ] Presentation slides committed (presentation template)
- [ ] Peer evaluation forms submitted (all members)