# Sessions — Teaching Material

One markdown file per session (32 total), with everything a professor needs to
prepare and teach a 90-minute class. Files are named `session-NN-topic.md` and
map 1:1 to the sessions in `../weekly-schedule.md`.

## How a 90-minute session is structured

| Block | Time | Material used |
|---|---|---|
| Lecture | ~25 min | `Learning objectives`, `Key concepts`, `Detailed lecture notes`, `Important terminology` |
| Hands-on | ~50 min | `Python examples`, `Beginner example`, `Practical Data Science example`, `In-class activity` |
| Wrap-up | ~15 min | `Lab exercise` kickoff, `Short assessment questions` discussion, `Suggested homework` |

## Template — every session file contains these 13 sections

1. **Learning objectives** — measurable outcomes for the session.
2. **Key concepts** — the 4–8 ideas the lecture revolves around.
3. **Detailed lecture notes** — the teachable narrative: *why* before *how*.
4. **Important terminology** — the vocabulary students must use correctly.
5. **Python examples** — code with brief explanations (the core API of the session).
6. **Beginner example** — the smallest possible working illustration.
7. **Practical Data Science example** — a realistic dataset task tying the topic to real work.
8. **In-class activity** — the 50-minute hands-on block, with concrete steps.
9. **Lab exercise** — the weekly lab (from `../labs/`), with tasks and submission notes.
10. **Common mistakes** — frequent errors and how to avoid them.
11. **Short assessment questions** — quick checks; usable as quiz/exit-ticket items.
12. **CLO mapping** — which course learning outcome(s) this session serves and how.
13. **Suggested homework** — reading and practice before the next session.

## Conventions

- **Audience:** BS Data Science 3rd-semester beginners. Concepts are introduced
  with intuition and plain language first; formal/mathematical detail is added
  only when it aids understanding.
- **Datasets:** prefer built-in data (`sns.load_dataset`, `sklearn.datasets`)
  so examples run without downloads; live APIs are used in session 11.
- **Code style:** every example must run as shown; random seeds are set wherever
  randomness appears.
- **Assessments:** `Short assessment questions` across sessions feed the three
  module quizzes in `../quizzes/`; sample exam tasks come from the
  `Practical Data Science example` sections of sessions 7–15, 17–22.
- **Exam/presentation sessions** (16, 31, 32) use the same 13-section template
  adapted to review, exam, and presentation logistics.

## Session index

| Session | File | CLO |
|---|---|---|
| 1 — What is Data Science? | `session-01-what-is-data-science.md` | 1 |
| 2 — Python Refresher | `session-02-python-refresher.md` | 1 |
| 3 — Jupyter in Depth | `session-03-jupyter-in-depth.md` | 1 |
| 4 — Git & GitHub | `session-04-git-and-github.md` | 1 |
| 5 — NumPy I | `session-05-numpy-part-1.md` | 1 |
| 6 — NumPy II | `session-06-numpy-part-2.md` | 1 |
| 7 — Pandas I | `session-07-pandas-part-1.md` | 1 |
| 8 — Pandas II | `session-08-pandas-part-2.md` | 1 |
| 9 — Data Cleaning I | `session-09-data-cleaning-1.md` | 1 |
| 10 — Data Cleaning II | `session-10-data-cleaning-2.md` | 1 |
| 11 — Data Acquisition | `session-11-data-acquisition.md` | 1 |
| 12 — Combining Data | `session-12-combining-data.md` | 1 |
| 13 — Matplotlib | `session-13-matplotlib.md` | 1 |
| 14 — Seaborn | `session-14-seaborn.md` | 1 |
| 15 — EDA Workflow | `session-15-eda-workflow.md` | 1 |
| 16 — Midterm Exam | `session-16-midterm-exam.md` | 1, 2 |
| 17 — Intro to ML | `session-17-intro-to-machine-learning.md` | 2 |
| 18 — Linear Regression | `session-18-linear-regression.md` | 2 |
| 19 — Classification I | `session-19-classification-1.md` | 2 |
| 20 — Classification II | `session-20-classification-2.md` | 2 |
| 21 — Clustering | `session-21-clustering.md` | 2 |
| 22 — Pipelines & CV | `session-22-pipelines-and-cross-validation.md` | 2 |
| 23 — Project Kickoff | `session-23-project-kickoff.md` | 1, 2, 3 |
| 24 — Reproducible Workflows | `session-24-reproducible-workflows.md` | 3 |
| 25 — LLMs for Data Science | `session-25-llms-for-data-science.md` | 3 |
| 26 — PandasAI | `session-26-pandasai.md` | 3 |
| 27 — Ollama Local Models | `session-27-ollama-local-models.md` | 3 |
| 28 — Simple AI Agents | `session-28-ai-agents.md` | 3 |
| 29 — n8n Automation | `session-29-n8n-automation.md` | 3 |
| 30 — Ethics & Responsible AI | `session-30-ethics-and-responsible-ai.md` | 3 |
| 31 — Project Presentations I | `session-31-project-presentations-1.md` | 1, 2, 3 |
| 32 — Project Presentations II & Final | `session-32-project-presentations-2-and-final-exam.md` | 1, 2, 3 |