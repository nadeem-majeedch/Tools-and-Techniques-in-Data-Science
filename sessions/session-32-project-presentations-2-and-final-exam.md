# Session 32 — Project Presentations II, Final Exam, Wrap-up

**Week 16 · Session 32 · Module C · 90 min · CLO-1, CLO-2, CLO-3**

## 1. Learning objectives

By the end of this session, students demonstrate they can:
- Present the final project (remaining teams) at the same standard as Session 31.
- Complete a comprehensive final exam covering CLO-1, CLO-2, and CLO-3.
- Reflect on what they can now do as data science practitioners.
- Submit the complete final project (repo + report + reflection).

## 2. Key concepts (final review list)

- **Module A (CLO-1):** lifecycle; Python/Jupyter/Git; NumPy; Pandas (I/O, filtering, groupby); cleaning (missing, duplicates, types, strings, reshape); acquisition (files, APIs); combining (concat/merge); visualization (Matplotlib figure/axes, Seaborn hue/facets); the EDA recipe and finding→evidence→implication.
- **Module B (CLO-2):** supervised vs. unsupervised; train/test split; baseline; regression (coefficients, MAE/RMSE/R², residuals); classification (k-NN, logistic, trees; confusion matrix, precision/recall); clustering (k-means, elbow, scaling); pipelines (leakage!) and cross-validation (mean ± std).
- **Module C (CLO-3):** LLMs (fluency ≠ accuracy; prompts; verify); PandasAI (audit generated code, AI log); Ollama (local vs. cloud, privacy); agents (loop, tools, boundaries); n8n (triggers, nodes, idempotency); reproducibility (environment, seeds, process); ethics (bias stages, privacy, provenance, reflection).

## 3. Detailed lecture notes

**Session format (90 min):**
- **0–50 min:** remaining project presentations (5–6 teams; same 10+3 format as Session 31).
- **50–80 min:** final exam (comprehensive, per `../assessment-plan.md` — written section + short practical task).
- **80–90 min:** wrap-up: what you can now do, how the pieces connect, where to go next; final-submission confirmation.

**The final exam (structure).** Closed-notes written section (concepts,
code-reading, explain-why, and one short AI-ethics question), plus a short
practical notebook task (load → clean → summarize → plot one finding). It
covers all three CLOs with the same question styles as the midterm (Session 16)
plus Module C's material. Sample question types:
- **CLO-1:** write the pandas for "mean tip by day, descending"; explain why
  `fillna(0)` is wrong for a temperature column; read a boxplot.
- **CLO-2:** why must test data stay untouched during tuning?; read a confusion
  matrix; what does CV mean ± std tell you?
- **CLO-3:** why can an LLM be confidently wrong?; what must an AI log record?;
  name two stages where bias enters a pipeline.

**Wrap-up — the 16-week story.** Draw the arc on the board: you began with "what
is data science?" (Session 1) and you end able to *do* it end-to-end: acquire
real data (Session 11), clean it with judgment (Sessions 9–10), explore it with
purpose (Sessions 13–15), model it honestly (Sessions 17–22), and accelerate it
with AI — privately, verifiably, and responsibly (Sessions 25–30). The project
you just presented is a portfolio artifact proving all of it.

**What's next (a roadmap, keep it light):** the tools you've learned scale
up: `seaborn` → richer visualization; scikit-learn basics → deeper ML
(feature engineering, random forests, evaluation nuance); Pandas → SQL and
big-data tooling; your AI workflows → more capable agents and automation; the
ethics habit → a professional differentiator. The course gave you the *loop*
(ask → acquire → clean → explore → model → communicate, with AI as an
assistant): every future project is a faster iteration of it.

## 4. Important terminology

Final-term vocabulary sweep (spot-check these in the exam):
`dataset/observation/feature · lifecycle · dtype · broadcasting · boolean mask ·
loc/iloc · split-apply-combine · MCAR/MNAR · imputation · tidy data · melt ·
API · status code · inner/left join · figure/axes · histogram/boxplot ·
correlation vs. causation · seed · train/test · baseline · overfitting ·
MAE/RMSE/R² · confusion matrix · precision/recall · k-means/inertia/elbow ·
pipeline · data leakage · cross-validation · LLM/hallucination · prompt ·
verification protocol · AI log · Ollama/local vs. cloud · agent/tool loop ·
trigger/node/idempotency · reproducibility pillars · bias stages · provenance ·
reflection`.

## 5. Python examples (exam-style quick drills)

```python
# CLO-1 style: clean + summarize in 6 lines
import pandas as pd, seaborn as sns
df = sns.load_dataset("penguins")
print(df.isna().sum())
df = df.dropna(subset=["species", "bill_length_mm"])
print(df.groupby("species")["bill_length_mm"].mean().round(1))

# CLO-2 style: pipeline + CV in 4 lines
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
print(cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(3)),
                      df[["bill_length_mm", "bill_depth_mm"]], df["species"], cv=5).mean())

# CLO-3 style: the verification reflex
# Ask: "is this LLM-generated pandas correct?" -> run it, check one number by
# hand, record tool + prompt in the AI log. (No code needed — it's a habit.)
```

## 6. Beginner example

```python
# The whole course in one line of thinking:
# question -> acquire -> clean -> explore -> model -> communicate
# (with AI as a verified assistant along the way)
print("I can now do this end-to-end.")
```

## 7. Practical Data Science example

The course's capstone pattern, restated as the final exam's practical task:
load a small dataset → inspect → clean with justification → one `groupby`
summary → one labeled chart → one finding with evidence. If students can do
that unassisted, they own CLO-1; combined with a pipeline+CV (CLO-2) and a
documented AI step (CLO-3), they own the course.

## 8. In-class activity

Session logistics as in section 3: presentations (0–50), exam (50–80),
wrap-up + submission confirmation (80–90). During the wrap-up, each student
writes one sentence: "the most useful thing I can now do that I couldn't in
Week 1" — shared aloud for a closing round.

## 9. Lab exercise

No lab — **final submission due today**: project repo (executed notebooks,
requirements.txt, README with "How to reproduce"), the final report/reflection
(five-part ethics structure from Session 30), and the presentation. Confirm the
push before leaving.

## 10. Common mistakes (exam + submission)

- Submitting the repo without `Restart & Run All` — stale outputs cost rubric points.
- Missing "How to reproduce" or `requirements.txt` in the repo (Session 24 checklist).
- Rushing the practical exam task and skipping labels/justifications.
- Leaving the AI-assisted component undocumented (no AI log) — CLO-3 points lost.
- Not re-reading the rubric before final submission.
- Forgetting that the reflection must be *specific* (name actual choices), not generic.

## 11. Short assessment questions

Final five self-checks before submission:
1. Does my repo run from a fresh environment (venv + requirements + Run All)?
2. Can I defend my top cleaning decision and my model choice in two sentences each?
3. Is every AI-assisted step logged (tool, prompt, verification)?
4. Did I state at least one limitation and one bias consideration?
5. Does my README's "How to reproduce" actually work for a stranger?

## 12. CLO mapping

This session closes the loop on all three CLOs: presentations + final exam
verify CLO-1 (data workflow), CLO-2 (modeling), and CLO-3 (AI-assisted
workflows with reproducibility, ethics, and responsible use) — matching the
assessment plan's coverage matrix.

## 13. Suggested homework

- Congratulations — the course is complete. Optional next steps: (1) publish
  your project repo as a portfolio piece (add a screenshot/README polish first);
  (2) extend one project component with a tool from "what's next"; (3) keep the
  AI log habit — it will serve you in every future data role.
- Feedback: share one thing the course could improve (anonymous form) — it makes
  the next cohort's experience better.