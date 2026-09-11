# Final Project — Grading Rubric

**Project weight:** 6 of the 25-mark Sessional (institutional scheme:
Sessional 25 · Mid Exam 35 · Final Exam 40) · **Rubric version:** v1.2

## 1. How the project grade is built (100% project grade)

| Component | Share | Type | When |
|---|---|---|---|
| Proposal | 5% | gate (team) | W13 S26 |
| Main submission (13 required components) | 85% | team | W16 S32 |
| Viva | 10% | individual | W16 S31–32 |
| **Total** | **100%** | | |

- **Proposal is a gate**: if a team has no approved proposal by the deadline,
  the project grade is capped at 50% (see §4, penalty 1).
- The **viva is individual**: each member is graded on their own component
  and their ability to explain any part of the work.
- The **peer evaluation form** does not add points directly; it is used to
  adjust the individual viva and to flag non-contribution (see §4, penalty 3).

## 2. Main submission rubric (85% of project grade)

Each criterion is scored on the scale in §3. Weights follow
`assessment-plan.md` §5.

| # | Criterion (weight) | What we grade | CLO |
|---|---|---|---|
| 1 | Problem framing & data acquisition (20%) | A specific, answerable question with audience + decision; documented, openly licensed data source; reproducible, cached acquisition (script/function). | CLO-1 |
| 2 | Cleaning & EDA (25%) | Correct dtype/missing/duplicate handling with logged reasons; univariate + group + correlation exploration; findings stated as claim→number→plot. | CLO-1 |
| 3 | Modeling (25%) | At least one appropriate scikit-learn model (regression/classification/clustering); proper train/test split; scaling/encoding where needed. | CLO-2 |
| 4 | Model evaluation (part of 3) | Honest metric choice; baseline comparison; one-paragraph interpretation of results, limits included. | CLO-2 |
| 5 | AI-assisted analysis (15%) | At least one documented, verified AI-assisted step (LLM/PandasAI/Ollama); prompt + output logged; result verified against data; disclosure in README/report. | CLO-3 |
| 6 | Streamlit application (part of 2) | `app.py` runs with `streamlit run app.py`; ≥ 3 widgets genuinely drive tables/figures; `@st.cache_data` used; no errors. | CLO-1 |
| 7 | Reproducibility & ethics (10%) | `requirements.txt` (pinned), seeds, ≥ 10 commits showing evolution, cache-on-first-fetch; ethics + reproducibility reflection in report. | CLO-3 |
| 8 | Presentation & communication (5%) | 6-minute talk, clear narrative, at least 2 figures explained, handles Q&A. | CLO-3 |

## 3. Level descriptors (applied to every criterion)

| Level | Range | Descriptor |
|---|---|---|
| Excellent | 90–100% | Correct, complete, justified decisions; extra insight; everything runs; work is explainable. |
| Good | 75–89% | Correct and complete with minor gaps (e.g., one undocumented cleaning choice, metric not compared to baseline). |
| Satisfactory | 60–74% | Core task done but shallow (e.g., EDA is a list of plots with no claims; evaluation without interpretation). |
| Needs work | 40–59% | Partially done; visible errors or missing required sub-steps. |
| Missing | 0% | Component absent or non-functional. |

## 4. Penalties

1. **No proposal by deadline** → project grade capped at 50%.
2. **Late submission** → −10% of the project grade per day
   (`assessment-plan.md` late policy).
3. **Non-contribution** → a member flagged on peer-evaluation forms by all
   teammates with no rebuttal loses the viva component (10%) and their share
   of criterion 8 (presentation).
4. **Unexplained AI-generated code in the viva** → treated as unverified use:
   criterion 5 (AI-assisted analysis) is scored at 0 and the case is reported
   per academic integrity policy.
5. **No ethics reflection** → criterion 7 capped at 50%.

## 5. Scoring sheet (printable)

| Component | Points | Score | Notes |
|---|---|---|---|
| Proposal (5) | /5 | | gate |
| Problem framing & acquisition (17) | /17 | | 20% of 85 |
| Cleaning & EDA (21) | /21 | | 25% of 85 |
| Modeling + evaluation (21) | /21 | | 25% of 85 |
| AI-assisted analysis (13) | /13 | | 15% of 85 |
| Streamlit app (included above) | — | | part of criterion 2/6 |
| Reproducibility & ethics (8.5) | /8.5 | | 10% of 85 |
| Presentation (4.25) | /4.25 | | 5% of 85 |
| Viva (10) | /10 | | individual |
| **Total** | **/100** | | |

Rounding to one decimal. Final course contribution = project grade ÷ 100 × 6
Sessional marks (e.g. 85/100 → 5.1 of the 6 marks).