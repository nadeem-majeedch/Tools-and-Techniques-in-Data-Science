# Lab 23 — Project Kickoff: Proposal Workbook

**Session:** Week 12 · Session 23 · 90 min
**CLO:** CLO-2, CLO-3
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Turn a vague interest into a specific, answerable data question.
2. Choose a dataset that actually exists and is licensed for use.
3. Define a success metric before building anything.
4. Draft the first version of the project proposal (due Session 26).

## Problem statement

Your final project (teams of 2–3, see `projects/README.md` and
`assessment-plan.md`) starts now. This lab is a **workbook**: by the end of
this session each team has a one-page proposal draft with a dataset
verified to load, a target variable, and a success metric. The real
proposal (due W13 S26) will be this draft, polished.

## Dataset requirements

Any public dataset your team can actually load today. Options that load
with one line: seaborn built-ins (`penguins`, `tips`, `flights`,
`diamonds`, `titanic`), or anything reachable via a keyless API (Open-Meteo
pattern from Lab 11). Verify it loads **in this session** — an unloadable
dataset is a failing proposal.

## Step-by-step tasks

1. **Team + question (15 min):** write one sentence each:
   - the question (must be answerable with data),
   - who cares about the answer,
   - what decision the answer would inform.
2. **Dataset check (20 min):** load the dataset; print `shape`, `info()`,
   `head()`. Confirm: it exists, loads offline (or caches), and you know
   its license/provenance (write it down).
3. **Framing (15 min):** write down:
   - target variable (what you predict/describe),
   - feature candidates,
   - supervised or unsupervised? regression or classification?
4. **Success metric (10 min):** one line: "success = test MAE ≤ X" or
   "success = CV accuracy ≥ Y" — pick a number you can check in Lab 24.
5. **Risk list (10 min):** list the top 3 things that could go wrong (bad
   data, metric too optimistic, time) and one mitigation each.
6. **Repo setup (20 min):** in your course repo, create `projects/final/`
   with: `README.md` (the draft proposal), `data/` (or a `data_loader.py`
   that fetches the dataset), and a first `eda.ipynb` with the task-2
   verification. Commit and push.

## Starter code

```markdown
# Project Proposal (draft)

**Team:** <names>   **Date:** <date>

## Question
<one sentence: answerable with data>

## Audience & decision
<who cares, what decision>

## Dataset
- Source: <name / URL>
- License / provenance: <...>
- Shape: <rows, cols>   Verified loads: yes/no

## Framing
- Target: <...>
- Features: <...>
- Type: supervised/unsupervised · regression/classification

## Success metric
- <one number, checkable>

## Top risks
1. <risk> -> <mitigation>
2. ...
3. ...
```

## Expected output

- `projects/final/README.md` committed with all 7 sections filled.
- `projects/final/eda.ipynb` committed showing the dataset loads
  (shape/info/head cells executed).
- A one-sentence status: "proposal draft done, pending instructor review".

## Questions

1. Why must the question be answerable *with the data you have*? Give an
   example of a great question and an unanswerable one.
2. What is the difference between the target and a feature?
3. Why define the success metric before building the model?
4. Why does dataset provenance/license matter for a graded project?
5. Your metric is "CV accuracy ≥ 90%". What is one way that number could
   be misleading?

## Challenge task

Write the **threats-to-validity** paragraph (5–6 sentences): under what
conditions would your conclusion be wrong? Include at least one data
problem (missingness, bias in sampling) and one modeling problem
(overfitting, leakage). This paragraph becomes part of the final report
(Session 32).

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Question + audience + decision | 4 | specific, answerable |
| Dataset verified loading | 4 | shape/info/head executed |
| Provenance/license recorded | 2 | stated in README |
| Framing (target/features/type) | 3 | correct terminology |
| Success metric with number | 3 | checkable |
| Risks with mitigations | 3 | 3 risks, 3 mitigations |
| Repo structure + commit | 4 | README + eda.ipynb pushed |
| Answers to questions | 3 | Q1, Q3, Q5 correct |
| Challenge: validity paragraph | 4 | ≥2 problem types |
| **Total** | **30** | |