# <Project Title> — Final Report

**Team:** <names> · **Date:** <date> · **Word count target:** ~1,000 words
(±20%)

---

## 1. Executive summary (150 words max)

<Question, data, method, headline result, and why it matters. The busy
stakeholder reads only this.>

## 2. Problem definition

- **Question:** <one sentence>
- **Audience:** <who cares>
- **Decision:** <what the answer informs>
- **Why it's interesting/hard:** <1–2 sentences>

## 3. Data

- Source + license + retrieval method + date (table).
- Shape, columns, and any data-quality issues found.
- Cleaning summary: 3–5 key decisions with reasons (full log in the
  notebook).

## 4. Exploratory data analysis

- 3 key findings (claim → number → figure reference).
- One figure embedded with a caption (at minimum).

## 5. Method & modeling

- Framing: target, features, supervised/unsupervised, task type.
- Model(s) tried, split/CV setup, seeds.
- Why this model fits the question (1 paragraph).

## 6. Results & evaluation

- Metric(s) with exact numbers; **baseline comparison**.
- Table: model vs. baseline.
- Interpretation: what the numbers mean *for the decision in §2*.
- Limitations of the evaluation (small test set, imbalance, leakage
  risks).

## 7. Streamlit application

- What it lets a user do (widgets, panels).
- One screenshot or detailed panel description.
- Link to run instructions (README).

## 8. AI-assisted analysis (CLO-3)

- What AI assistance was used (PandasAI/Ollama/LLM prompt/agent), if any.
- One example: prompt → output → **your verification** → verdict.
- Why the verification step matters (2–3 sentences).

## 9. Ethics & reproducibility

- **Data sheet:** source, who collected it, what it doesn't contain
  (privacy), known limitations.
- **Bias check:** any group analyzed differently? Sample sizes?
- **Reproducibility:** environment pins, seeds, restart-safe notebooks,
  cache strategy.
- **AI-use disclosure:** tool + prompt + verification per
  `../assessment-plan.md`.

## 10. Threats to validity (from the proposal, updated)

<Under what conditions would the conclusion be wrong? At least one data
problem and one modeling problem, with mitigations.>

## 11. Conclusion & future work

- Restate the answer to the question (1–2 sentences).
- 2–3 concrete next steps if given another week.

## 12. Appendix

- Cleaning log (or link to notebook section).
- Viva preparation notes (optional).
- References/data sources.