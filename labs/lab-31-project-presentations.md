# Lab 31 — Project Presentations: Prep & Peer Review

**Session:** Week 16 · Session 31 · 90 min
**CLO:** CLO-3 (presentation + review)
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Structure a 6-minute project talk: question → data → method → results →
   limits.
2. Prepare a demo that survives (fallbacks, cached data, printed outputs).
3. Give and receive structured peer feedback using a rubric.
4. Turn feedback into a concrete fix list for the final submission.

## Problem statement

Presentations start **this session**. Half the teams present today, the
rest next session; everyone reviews. This lab is the rehearsal + review
workbook: each team prepares its 6-minute talk, presents (or rehearses
against the clock), reviews two other teams with the rubric below, and
leaves with a prioritized fix list.

## Dataset requirements

Your own project (dataset, model, results from Labs 23–30). Nothing new to
load — the point is *communication*.

## Step-by-step tasks

1. **Talk skeleton (10 min):** fill in the 5 slides:
   - Slide 1 — question + why it matters (one sentence each),
   - Slide 2 — data: source, shape, license, one quality issue you fixed,
   - Slide 3 — method: model(s), metric, one line on why this method,
   - Slide 4 — results: ONE chart + the number that answers the question,
   - Slide 5 — limits + what you would do next.
   Write the skeleton as markdown in `projects/final/presentation.md`.
2. **Demo dry-run (15 min):** run your notebook top-to-bottom **once more**
   and confirm the key outputs (the chart, the metric) appear. Note one
   fallback if the live demo fails (e.g., print a cached number).
3. **Timed rehearsal (15 min):** present to your team; hard stop at 6
   minutes. Record where you overran (intro? method?) and cut accordingly.
4. **Peer review (30 min):** review **two** other teams using the rubric
   below. Write 3 strengths and 2 improvements per team, with specific
   evidence ("slide 3 had no axis label" not "good job").
5. **Fix list (10 min):** merge the feedback into a prioritized list
   (`must-fix` / `nice-to-have`) in `presentation.md`. Anything in
   must-fix that touches code goes into your notebook **today**.
6. **Commit:** push `presentation.md` and any notebook changes.

## Starter code

```markdown
# Presentation — <project title>
**Team:** ...   **Presenting session:** 31 / 32

## Slide 1 — Question
<one sentence> · Why it matters: <one sentence>

## Slide 2 — Data
Source: ... | License: ... | Shape: ... | Fixed: <one quality issue>

## Slide 3 — Method
Model: ... | Metric: ... | Why: <one line>

## Slide 4 — Results
Chart: <file> | Answer: <the number>

## Slide 5 — Limits & next
<2 bullets>

## Peer feedback received
| From | Strengths (3) | Improvements (2) |
|---|---|---|

## Fix list
- [ ] must-fix: ...
- [ ] nice-to-have: ...
```

## Expected output

- `presentation.md` committed with all 5 slides filled, peer-feedback
  table, and a fix list with at least 2 must-fix items.
- Evidence of the dry run: the notebook was re-run and the key output cell
  is fresh (or a cached fallback noted).
- Two completed peer reviews delivered (3 strengths + 2 improvements each,
  specific).
- One must-fix item actually fixed in the notebook.

## Peer-review rubric (use for steps 4–5)

| Criterion | 1 (weak) | 3 (solid) | 5 (excellent) |
|---|---|---|---|
| Question clarity | vague or absent | clear, stated once | clear AND motivates method |
| Data transparency | no source/license | source named | source + license + one limitation |
| Method fit | model unexplained | model named + metric | metric choice justified |
| Results shown | no chart/no number | chart or number | chart AND number that answers the question |
| Limits | none | one limit | limits + what you'd do next |

## Questions

1. Why should slide 2 mention a data *limitation* you fixed rather than
   hiding it?
2. What is the one number a stakeholder remembers from your talk? How did
   you choose it?
3. Why practice with a hard time stop before the real talk?
4. What makes feedback actionable (vs. "nice job")?
5. A demo fails live. What is your fallback, and why plan it in advance?

## Challenge task

Write the **1-line takeaway** that your team will say last:
"<dataset> shows <finding>, so <decision>." Then rehearse the talk once
more and record (in `presentation.md`) your final time and which slide
still needs trimming.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| 5-slide skeleton complete | 5 | all sections filled |
| Dry-run evidence + fallback | 3 | re-run or cached note |
| Timed rehearsal recorded | 3 | overrun noted + cut |
| Two peer reviews (3+2, specific) | 6 | evidence cited |
| Fix list prioritized | 3 | ≥2 must-fix |
| One must-fix implemented | 4 | in notebook, committed |
| Answers to questions | 3 | Q1, Q3, Q4 correct |
| Challenge: takeaway + final time | 3 | 1-liner + time |
| **Total** | **30** | |