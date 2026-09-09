# Introduction to Data Science

**Tools and Techniques in Data Science** — BS Data Science, 3rd semester · 16 weeks · 2 sessions/week · 90-minute sessions · Python

> From messy CSV files to a working data app: this site collects every lecture,
> lab, assignment, and guide for the course in one place. Follow the learning
> path below in order, or jump to any section from the menu.

---

## Course at a glance

| | |
|---|---|
| **Program** | BS Data Science — 3rd Semester |
| **Format** | 16 weeks × 2 sessions/week × 90 min (32 sessions) |
| **Language / stack** | Python · Jupyter · Git/GitHub · NumPy · Pandas · Matplotlib · Seaborn · scikit-learn · Streamlit · PandasAI · Ollama · n8n |
| **Modules** | A — Data handling & EDA (Weeks 1–8, CLO-1) · B — Machine learning basics (Weeks 9–12, CLO-2) · C — AI-assisted workflows (Weeks 13–16, CLO-3) |

Start with the [Course Overview](course-outline.md), the [CLOs](CLOs.md), and
the [Course Schedule](weekly-schedule.md) to see how the semester is organized.

## The learning path

The course is deliberately progressive — each stage builds on the last. Work
through the path top to bottom; links open the session, its notebook, or the
guide you need at that point.

1. **Python** — types, control flow, functions, comprehensions
   → [Session 2](sessions/session-02-python-refresher.md)
   · [Notebook 01](course-notebooks/01-python-for-data-science.ipynb)
   · [Python Setup](resources/setup-guide.md)
2. **NumPy** — arrays, indexing, universal functions, masks, random
   → [Sessions 5–6](sessions/session-05-numpy-part-1.md)
   · [Notebook 02](course-notebooks/02-numpy.ipynb)
3. **Pandas** — Series, DataFrames, filtering, reading/writing files
   → [Sessions 7–8](sessions/session-07-pandas-part-1.md)
   · [Notebook 03](course-notebooks/03-pandas.ipynb)
4. **Data Cleaning** — missing values, duplicates, dtypes, string methods, reshaping
   → [Sessions 9–10](sessions/session-09-data-cleaning-1.md)
   · [Notebook 04](course-notebooks/04-data-cleaning.ipynb)
   · [Assignment 1](assignments/assignment-01-data-cleaning-eda/README.md)
5. **EDA** — summary stats, distributions, correlations, the EDA workflow
   → [Session 15](sessions/session-15-eda-workflow.md)
   · [Notebook 07](course-notebooks/07-eda.ipynb)
6. **Visualization** — Matplotlib & Seaborn
   → [Sessions 13–14](sessions/session-13-matplotlib.md)
   · [Notebook 06](course-notebooks/06-data-visualization.ipynb)
7. **Git** — version control & GitHub workflow
   → [Session 4](sessions/session-04-git-and-github.md)
   · [Notebook 08](course-notebooks/08-git-github-workflow.ipynb)
   · [Git & GitHub Guide](guides/git-github-guide.md)
8. **APIs** — data acquisition with `requests`, JSON, scraping ethics
   → [Session 11](sessions/session-11-data-acquisition.md)
   · [Notebook 09](course-notebooks/09-apis-and-data-acquisition.ipynb)
9. **Machine Learning** — scikit-learn, regression, classification, clustering, evaluation
   → [Sessions 17–22](sessions/session-17-intro-to-machine-learning.md)
   · [Notebooks 10–13](course-notebooks/10-intro-to-machine-learning.ipynb)
   · [Assignment 2](assignments/assignment-02-api-streamlit-app/README.md)
10. **Streamlit** — turn Python scripts into interactive data apps
    → [Streamlit Guide](streamlit/streamlit-introduction.md) (full module)
11. **PandasAI** — ask questions about your data in plain language
    → [PandasAI Guide](guides/pandasai-guide.md) · [Session 26](sessions/session-26-pandasai.md)
12. **LLMs** — how large language models work, prompting, and their limits
    → [LLM & Ollama Guide](guides/llm-ollama-guide.md) · [Session 25](sessions/session-25-llms-for-data-science.md)
13. **Ollama** — run models locally on your own machine
    → [LLM & Ollama Guide](guides/llm-ollama-guide.md) · [Session 27](sessions/session-27-ollama-local-models.md)
14. **AI Agents** — tool calling and simple agent loops
    → [AI Agents Guide](guides/ai-agents-guide.md) · [Session 28](sessions/session-28-ai-agents.md)
15. **n8n** — visual automation workflows
    → [n8n Guide](guides/n8n-guide.md) · [Session 29](sessions/session-29-n8n-automation.md)
16. **Final Project** — everything end to end, presented in Week 16
    → [Project overview](projects/README.md) · [Kickoff session](sessions/session-23-project-kickoff.md)

??? tip "Why this order?"
    You first learn to **read** data (Pandas), then to **fix** it (cleaning),
    **look** at it (EDA + visualization), **model** it (machine learning), and
    finally to **share** it (Streamlit apps). Only after all that do we add
    AI assistance (PandasAI → LLMs → Ollama → agents → n8n) — because AI
    tools are only trustworthy once you can verify their output yourself.

## Where to go next

| I want to… | Start here |
|---|---|
| See the whole semester | [Course Schedule](weekly-schedule.md) |
| Prepare one lecture or catch up | [Weekly Lectures](sessions/README.md) |
| Practice coding | [Labs](labs/README.md) |
| Check graded work | [Assignments](assignments/README.md) · [Quizzes](assessments/quizzes.md) · [Exams](assessments/exams.md) |
| Build the capstone | [Final Project](projects/README.md) |
| Set up my computer | [Python Setup](resources/setup-guide.md) |
| Fix a common problem | [FAQ](guides/faq.md) |
| Add AI to a data app | [Streamlit Guide](streamlit/streamlit-introduction.md) · [Module C](module-c/README.md) |

## Who this site is for

- **Students** — follow the learning path, do every [lab](labs/README.md)
  week by week, and submit work through Git/GitHub as each deliverable
  describes. Answer keys and instructor solutions are intentionally **not**
  published here; they are distributed separately by your instructor.
- **Instructors** — the full teaching pack (sessions, notebooks, module C,
  assessment banks, project rubric) lives in the same repository; see
  [Publish this Website](DEPLOYING.md) to host or customize this site.

Course materials are offered under **CC BY 4.0** unless stated otherwise per
file — see the repository README for the full license note.
