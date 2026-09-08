# Lab 32 — Final Submission & Exam Review

**Session:** Week 16 · Session 32 · 90 min
**CLO:** CLO-1, CLO-2, CLO-3 (all)
**Difficulty:** Advanced

## Learning objectives

By the end of this lab you can:

1. Audit your project repo against the final submission checklist.
2. Self-assess your work against the project rubric honestly.
3. Review all three modules for the final exam in one pass.
4. Hand in a submission that a stranger can run.

## Problem statement

Today is the last session: final project submission AND final exam. This
lab is the pre-flight checklist + exam review. Do the checklist **before**
submitting — each unchecked item is a mark you are choosing to lose.

## Dataset requirements

Your own project (final state). No new data.

## Step-by-step tasks (use the checklist first — 30 min)

1. **Repo audit** — mark ✓/✗ for each:
   - [ ] `README.md` names team, question, dataset, license
   - [ ] `requirements.txt` present with version header
   - [ ] notebooks run top-to-bottom (Restart & Run All)
   - [ ] every randomized call seeded (`SEED` or `random_state`)
   - [ ] results reproducible: the metric in the README matches the
         notebook's last run
   - [ ] AI disclosure included (from Lab 30)
   - [ ] data sheet / provenance included
   - [ ] presentation.md from Lab 31 committed
2. **Fix anything ✗** — at minimum: re-run notebooks, update README
   numbers, add the disclosure if missing. Commit and push.
3. **Self-assessment (15 min):** score your project 1–5 on: question
   clarity, data transparency, method fit, results communication, limits.
   Write one sentence per score, and one sentence on what you would change
   with one more week.
4. **Final commit:** `git log --oneline` should tell the project's story;
   make one last commit ("final submission") if anything is uncommitted.

## Exam review — Module A (10 min)

In one markdown cell, write from memory (then check):
- the 4 pandas selection tools and when each is used,
- the difference between `isna()` and `dropna()`,
- what `groupby(...).agg(...)` returns and its shape.

## Exam review — Module B (10 min)

Write from memory:
- the 4-step sklearn API,
- what `train_test_split` protects against and what `random_state` does,
- the meaning of accuracy vs. precision/recall, MAE vs. R².

## Exam review — Module C (10 min)

Write from memory:
- the agent loop (reason → call → observe → decide),
- two guarantees the registered-tools boundary provides,
- the AI-use disclosure policy's three requirements (from
  `assessment-plan.md`),
- the n8n three-part structure (trigger → processing → output).

## Starter code

```markdown
## Submission checklist
| Item | ✓/✗ |
|---|---|
| README: team, question, dataset, license | |
| requirements.txt with version header | |
| notebooks run top-to-bottom | |
| all random calls seeded | |
| README metric matches notebook | |
| AI disclosure included | |
| data sheet included | |
| presentation.md committed | |

## Self-assessment (1-5)
- Question clarity: ...
- Data transparency: ...
- Method fit: ...
- Results communication: ...
- Limits: ...
- With one more week I would: ...
```

## Expected output

- Checklist with all 8 items ✓ (or ✗ with the fix noted and done).
- Self-assessment with scores + the "one more week" sentence.
- Final commit pushed; `git status` clean.
- Three exam-review cells written **from memory first**, then corrected.

## Questions

1. Which checklist item protects you from the "works on my machine" grade
   complaint? Why?
2. Why must the README's headline metric match the notebook's last run?
3. During an exam, what would you check first when a model errors with a
   shape mismatch in `train_test_split`?
4. You used AI to write your EDA code. What does the disclosure require,
   and what is the consequence of omitting it?
5. Name the single most valuable habit from this course for your next data
   project — and why.

## Challenge task

Write the **course retrospective** (5 sentences): one thing that clicked
early, one thing you'd warn a next-semester student about, one skill you'll
use immediately in another course, and one skill you want to go deeper on.
Commit it as `retrospective.md` in your repo — your future self will thank
you.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Checklist completed (8 items) | 8 | ✓/✗ per item |
| Fixes executed | 4 | ✗ items addressed |
| Self-assessment with scores | 4 | 5 scores + sentence |
| Final commit + clean status | 3 | log tells the story |
| Module A review | 4 | correct, from memory |
| Module B review | 4 | correct, from memory |
| Module C review | 4 | correct, from memory |
| Answers to questions | 4 | Q1, Q3, Q4 correct |
| Challenge: retrospective | 3 | 5 sentences, committed |
| **Total** | **38** | |