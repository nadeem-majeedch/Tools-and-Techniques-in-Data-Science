# Session 23 — Final Project Kickoff

**Week 12 · Session 23 · Module B → C · 90 min · CLO-1, CLO-2, CLO-3**

## 1. Learning objectives

By the end of this session, students can:
- Turn a vague interest into a specific, answerable data question.
- Judge whether a dataset can answer the question (feasibility check).
- Plan a project into the lifecycle stages with milestones.
- Form teams and assign roles/milestones in the project repo.
- Submit the project proposal (due Session 26) with a clear structure.

## 2. Key concepts

- **A good project starts with a question**, not a dataset ("I want to use titanic" → "Does passenger class predict survival after controlling for age?").
- **Feasibility check:** can the data actually answer it? (Columns exist? Sample size? Time to clean?)
- **Scope discipline:** 6 weeks is short — one clear question, one dataset family, one model family beats three half-done ideas.
- **Milestones = lifecycle stages:** proposal (W13) → data + cleaning + EDA (W14) → modeling (W15) → presentation (W16).
- **Team mechanics:** 2–3 people, shared repo, clear division of labor, weekly check-ins.
- The project integrates **all three CLOs** — including an AI-assisted component (Module C's tools).

## 3. Detailed lecture notes

**Why a capstone project?** This is where the course's skills become *yours*:
a question of your choosing, messy real data, and a public artifact (repo +
presentation) that demonstrates CLO-1, CLO-2, and CLO-3 together. It's also the
best portfolio piece of the semester — recruiters look at exactly this kind of
work.

**From interest to question.** The #1 beginner mistake: start from a dataset and
hope a question appears. Invert it: start from a *question that matters to you*
(sports, campus life, food, games, health) and *then* find data. Use the
SMART-ish filter:
- **Answerable:** can be answered with the data you can get?
- **Specific:** "do teams with home advantage win more?" (one comparison) beats "analyze sports".
- **Measurable:** what column/number will decide it?
- **Bounded:** doable in 6 weeks by 2–3 students?
Draft three candidate questions in class; pick the one with the best data access.
Stress: the question can evolve after EDA — that's the lifecycle loop, and
Session 30's ethics work will add a "who is affected?" dimension.

**Feasibility check (do this before falling in love with a question).** For the
candidate dataset: (1) columns — is the target variable actually present?
(2) rows — enough observations for a basic model (≥ a few hundred for ML;
fewer is fine for EDA-heavy projects)? (3) quality — missingness, known
messiness, likely cleaning effort (Session 9's estimate); (4) provenance —
openly licensed, documented source (datasets/README conventions). Time-box this
to 30 minutes; it saves days later.

**Scoping for 6 weeks.** A common failure is ambition: "predict stock prices
with deep learning" (no — data leakage, random walk, and way beyond this
course). Right-size: one regression *or* classification *or* clustering task,
one cleaned dataset, and one AI-assisted or automated component. The rubric
(assessment-plan) rewards a *complete, honest* small project over an ambitious
broken one. If the data only supports EDA + one model, that's fine — say so.

**Milestones.** Map the lifecycle to weeks: **W13** proposal (question, data,
plan, risks) — due Session 26; **W14** data cleaned + EDA findings (check-in at
session start); **W15** model + AI-assisted component drafted; **W16**
presentation + final submission. Each milestone is a commit-able artifact —
progress must be visible in the repo, not just in chat.

**Team mechanics.** Teams of 2–3 (formed today). One shared repo; everyone
commits *their* parts (Git history is part of the grade — Session 4 pays off).
Recommended split: data/EDA owner, modeling owner, AI/automation + docs owner —
with everyone reviewing each other's code. Weekly check-in: 5-minute status
each (done / blocked / next). Conflicts → talk early, escalate to instructor.

**The AI-assisted component (preview).** Module C teaches the tools you'll use:
PandasAI or Ollama for an analysis step, or an n8n automation for data
collection/processing (Sessions 26–29), plus a written reflection on
reproducibility and ethics (Session 30). You don't need to finalize the choice
today — but note it in the proposal so the plan is realistic.

## 4. Important terminology

- **Problem statement** — one or two sentences: question + why it matters.
- **Feasibility** — can this data answer this question, in this time?
- **Milestone** — a checkpoint with a concrete deliverable.
- **Scope** — how much the project attempts; discipline = one clear question.
- **Proposal** — question, data source, plan, risks (due Session 26).
- **Target variable** — the thing you're predicting (CLO-2 part).
- **Provenance** — where the data came from and its license.
- **Portfolio artifact** — a public repo that demonstrates your skills.
- **Repo hygiene** — meaningful commits, README, `requirements.txt`, executed notebooks.

## 5. Python examples

A quick feasibility-screening snippet to run on candidate datasets:

```python
import pandas as pd

def screen(df, name):
    print(f"--- {name} ---")
    print("shape:", df.shape)
    print(df.dtypes.value_counts())
    print("missing:\n", df.isna().sum()[df.isna().sum() > 0])
    print("duplicates:", df.duplicated().sum())
    print("sample:\n", df.head(2).to_string())

# Run this on each candidate dataset before committing to a question
import seaborn as sns
screen(sns.load_dataset("penguins"), "penguins")
```

## 6. Beginner example

```python
# The question filter, as a checklist in code comments:
# q = "Do bigger parties tip a higher percentage?"
# data = tips  (columns needed: size, tip, total_bill  -> present? yes)
# measurable = tip/total_bill vs size  -> yes
# time = one afternoon -> yes
print("Question passes the 4-point filter")
```

## 7. Practical Data Science example

A worked mini-proposal (written on the board / in the brief):

> **Question:** Do weekend tables generate larger tips than weekday tables, and
> does party size explain the difference?
> **Data:** `tips` (seaborn) — 244 rows, columns `total_bill`, `tip`, `size`,
> `day`, `time`, `sex`, `smoker`. License: CC BY. No cleaning beyond a check.
> **Plan:** EDA (groupby + boxplots + correlation) → model: regression of `tip`
> on `total_bill` + `size` + `is_weekend` with CV → AI component: PandasAI
> natural-language summary of findings → reflection on bias (sex/smoker
> variables are observational).
> **Risks:** small sample; tips correlated with bill size — we report the
> limitation.

Show how each rubric line in `../assessment-plan.md` maps to a proposal line.

## 8. In-class activity (50 min)

1. **Question workshop (20 min):** individually, write two candidate questions
   (one sentence each) that you care about. Pair up; apply the 4-point filter;
   keep the strongest.
2. **Feasibility screen (15 min):** for your top question, find a candidate
   dataset (course registry, Kaggle, public API); run the `screen()` snippet;
   note 2 risks.
3. **Team formation (10 min):** form teams of 2–3 around shared interests;
   agree on roles and a shared repo name; create the repo with a README.
4. **Proposal sprint (5 min):** assign who drafts which section of the
   proposal by Session 26.

## 9. Lab exercise

No traditional lab — the **deliverable is the project proposal** (due Session
26): one page covering question, data (source + license), plan with milestones,
and risks. Template: `../projects/final-project-brief.md` (added with the
brief). **Quiz 3 today** (ML, Sessions 17–22). **Assignment 2 released** (due
Session 25).

## 10. Common mistakes

- Starting from a dataset instead of a question → aimless analysis.
- Choosing a question the data can't answer (target column missing, tiny sample).
- Over-scoping: "predict and classify and cluster and automate everything".
- Procrastinating the proposal → a rushed, unclear plan that costs time in W14–15.
- One teammate doing all commits → invisible contribution, lower project grade.
- Picking a dataset requiring a license/agreement you can't share publicly.
- Ignoring the AI component until Week 16 — plan it now.

## 11. Short assessment questions

1. Rewrite "analyze the titanic dataset" as an answerable question.
2. What are the four feasibility checks for a dataset?
3. Why is "one clear question" better than "three half-done ideas" for a 6-week project?
4. What should a milestone look like in the repo? (A commit-able deliverable.)
5. Which CLOs must the final project demonstrate, and where?
6. What is the danger of "predict stock prices with deep learning" as a course project? (Leakage, unrealistic scope, beyond course tools.)

## 12. CLO mapping

The project integrates **CLO-1** (data + EDA), **CLO-2** (model + CV), and
**CLO-3** (AI-assisted component + reproducibility/ethics reflection). This
session sets up the planning and scoping that make all three achievable.

## 13. Suggested homework

- Finalize your candidate question + dataset; run the feasibility screen and save the output in your repo.
- Agree on team roles and create the shared repo with a README.
- Read: `../projects/README.md` and the rubric sketch in `../assessment-plan.md` — know how you'll be graded.
- Preview: Session 24 makes your project *reproducible* — environments, seeds, project layout, and documentation habits.