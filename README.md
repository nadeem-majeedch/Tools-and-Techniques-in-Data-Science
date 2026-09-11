# Introduction to Data Science
## Tools and Techniques in Data Science

| | |
|---|---|
| **Program** | BS Data Science — 3rd Semester |
| **Duration** | 16 weeks · 2 sessions per week · 90 minutes per session (32 sessions) |
| **Language** | Python |
| **Stack** | Jupyter · Git/GitHub · NumPy · Pandas · Matplotlib · Seaborn · Scikit-learn · PandasAI · Ollama · n8n |

---

## Course description

This course introduces the core tools and techniques used in modern data science.
Students learn to acquire, clean, manipulate, visualize, and explore real datasets
with Python, apply introductory machine learning techniques with scikit-learn, and
build simple AI-assisted workflows using LLMs, local models, and automation tools.
Throughout, the course emphasizes reproducibility, ethics, and the responsible use
of AI in data work.

## Learning outcomes (CLOs)

1. **CLO-1** — Apply Python and standard data science libraries to acquire, clean, manipulate, visualize and explore datasets.
2. **CLO-2** — Apply appropriate data science tools and basic machine learning techniques to solve introductory data-driven problems.
3. **CLO-3** — Develop simple AI-assisted data science workflows using LLMs, local models, automation tools and basic AI agents while considering reproducibility, ethics and responsible AI use.

Full CLO definitions, cognitive levels, and assessment mapping: [CLOs.md](CLOs.md)

## Modules

| Module | Weeks | Focus | CLO |
|---|---|---|---|
| **A — Data handling & EDA** | 1–8 | Python, Jupyter, Git, NumPy, Pandas, data acquisition & cleaning, Matplotlib/Seaborn, exploratory data analysis | CLO-1 |
| **B — Machine learning basics** | 9–12 | scikit-learn, regression, classification, clustering, model evaluation | CLO-2 |
| **C — AI-assisted workflows** | 13–16 | LLMs, PandasAI, Ollama, AI agents, n8n, reproducibility, ethics | CLO-3 |

Detailed week-by-week plan: [weekly-schedule.md](weekly-schedule.md)

## Assessment at a glance

| Component | Weight* | CLOs |
|---|---|---|
| Labs (32) | 10% | 1, 2, 3 |
| Quizzes (2) | 5% | 1, 2, 3 |
| Assignments (2) | 10% | 1, 3 |
| Midterm exam | 35% | 1, 2 |
| Final exam | 25% | 1, 2, 3 |
| Final project | 15% | 1, 2, 3 |
| **Continuous : Midterm : Final** | **25 : 35 : 40** | |

*Component weights roll up to the institutional 25% continuous (labs + quizzes +
assignments) / 35% midterm / 40% final (exam + project) distribution — see
[assessment-plan.md](assessment-plan.md) for details.

## Repository structure

```
.
├── README.md              # This file
├── index.md               # Website Home page
├── course-outline.md      # Full course outline & session format
├── CLOs.md                # CLO definitions and assessment mapping
├── weekly-schedule.md     # Week-by-week, session-by-session plan
├── assessment-plan.md     # Assessments, rubrics, policies
├── DEPLOYING.md           # How to publish/customize the GitHub Pages website
├── mkdocs.yml             # Website config (navigation, theme, what to publish)
├── website-requirements.txt
├── requirements.txt       # Python dependencies
├── .github/workflows/     # GitHub Actions (notebook CI, website build & deploy)
├── scripts/               # Build helpers (notebooks, website mirror, datasets)
├── sessions/              # Per-session teaching material (32 sessions)
├── course-notebooks/      # Executed Jupyter notebooks (20, numbered 01–20)
├── module-c/              # AI-assisted DS teaching pack (11 topics, CLO-3)
├── streamlit/             # Streamlit module (intro → dashboard project)
├── guides/                # Student quick guides (Git, PandasAI, LLMs, agents, n8n, FAQ)
├── assessments/           # Student-facing Quizzes & Exams info pages (no keys)
├── quizzes/               # Quiz banks (keys — instructor only)
├── exams/                 # Midterm + final exams (keys — instructor only)
├── assignments/           # 2 graded assignments (cleaning+EDA, API+Streamlit)
├── labs/                  # 32 lab exercises + instructor solutions
├── datasets/              # Dataset registry and small data files
├── tools/                 # Grade calculator (Streamlit app, 25/35/40 scheme)
├── projects/              # Final project framework (guidelines, rubric, templates)
└── resources/             # Setup guide, readings, cheatsheets
```

## Quick start

1. **Install Python 3.11+** and a code editor (VS Code recommended).
2. **Clone this repository** and create a virtual environment:
   ```bash
   git clone <repository-url> data-science-course
   cd data-science-course
   python -m venv .venv
   # Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Launch Jupyter**:
   ```bash
   jupyter lab
   ```
4. **Install the AI tools** used in Module C:
   - Ollama runtime: https://ollama.com — then `ollama pull llama3.2`
   - n8n: https://docs.n8n.io — e.g. `npx n8n` or Docker

Full step-by-step instructions: [resources/setup-guide.md](resources/setup-guide.md)

## Course website

This repository is also a GitHub Pages website built with MkDocs Material
(search, table of contents, responsive theme, Previous/Next reading order).
The site is student-facing — quiz/exam answer keys and instructor solutions
stay in the repo but are excluded from the published build.

- [index.md](index.md) — website Home page (course overview + learning path)
- [mkdocs.yml](mkdocs.yml) — site configuration (navigation & what to publish)
- [DEPLOYING.md](DEPLOYING.md) — publishing & customization instructions
- [scripts/build_site_src.py](scripts/build_site_src.py) — mirrors the repo
  content into `docs/` for the build (run before `mkdocs serve`/`build`)

## Who is this repository for

- **Students** follow the weekly schedule, complete labs/assignments, and submit
  work through Git/GitHub as described in each deliverable.
- **Instructors** can adapt the outline, schedule, weights, and materials. Each
  assessment folder documents its own submission and grading conventions.

## License

Course materials are offered under **CC BY 4.0** (attribution, non-restrictive
reuse) unless otherwise stated per file. Adjust or replace this license to match
your institution's policy before publishing.