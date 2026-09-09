# Exams

Two summative exams bookend the second half of each module. They use the same
question styles as the quizzes, scaled up: **MCQ, code tracing, debugging,
short answer, practical coding, and scenario/problem-solving**. The practical
coding part is answered directly in a Jupyter notebook during the exam.

| Exam | When | Time | Covers | CLOs |
|---|---|---|---|---|
| **Midterm** | Week 8 · Session 16 | 90 min | Weeks 1–8 — the full CLO-1 workflow: Python → Jupyter → Git → NumPy → Pandas → cleaning → acquisition & combining → visualization → EDA | CLO-1 (+ entry-level CLO-2) |
| **Final** | Week 16 · Session 32 | 120 min | Weeks 9–16 — machine learning (CLO-2) and AI-assisted workflows (CLO-3), including a reproducibility & AI-ethics section | CLO-2, CLO-3 |

## Structure (both exams)

1. **Part A — Written** (~25–40 min): definitions, code-reading ("what does
   this output?"), one-liner code-writing, and *explain-why* questions.
2. **Part B — Practical notebook** (remaining time): a small, provided dataset
   and a task list — load → inspect → clean (with justification) → derive →
   filter/sort → charts → written findings with evidence.

The [midterm session page](../sessions/session-16-midterm-exam.md) and the
[session 32 page](../sessions/session-32-project-presentations-2-and-final-exam.md)
describe the exact rules and timing as students experience them.

## How to prepare

- **Midterm:** rework [Lab 16 · Midterm Review](../labs/lab-16-midterm-review.md)
  — it is a timed mock exam in the real shape. Review each session's key
  concepts and terminology for Sessions 1–15.
- **Final:** Modules B and C content (Sessions 17–30). Be ready to *explain*
  your models, not just fit them — expected questions include "why did you
  choose this metric?", "what does this confusion matrix cell mean?", and
  short ethics/reproducibility scenarios.
- Re-run the course notebooks (10–20) in a fresh environment so the ML and
  AI-tool code is familiar.
- Practice the *findings with evidence* style: every claim you make in the
  notebook exam should have the printed output beneath it.

## Exam-day rules

- Written part: closed notes. Practical part: official pandas / NumPy /
  scikit-learn reference docs allowed; **saved notebooks and AI assistants are
  not** — these exams assess individual skill (CLO-3 AI skills are assessed in
  Sessions 25–30, labs, and the final project instead).
- **Restart & Run All** your notebook before submitting, then push to the exam
  branch and note the commit hash.
- Justify every cleaning choice in one sentence — partial credit exists for
  reasoning, and unexplained `dropna()` calls lose marks.

## Related pages

- [Quizzes](quizzes.md) — the same question styles, in shorter form
- [Weekly Schedule](../weekly-schedule.md) · [Assessment Plan](../assessment-plan.md)
- [Final Project](../projects/README.md) — where CLO-3 skills are assessed in depth
