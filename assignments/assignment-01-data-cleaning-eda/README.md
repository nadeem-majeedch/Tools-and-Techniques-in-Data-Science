# Assignment 1 — Data Cleaning + Exploratory Data Analysis

**Released:** W6 S12 · **Due:** W8 S15 (before session start) · **Individual**
**Weight:** 5% of course grade (part of the 10% assignments component)
**CLO mapping:** CLO-1 (primary)

---

## 1. Learning objectives

By completing this assignment you can:

1. Audit a messy real-world-style dataset for missing values, duplicates,
   inconsistent text, wrong dtypes, mixed date formats, and outliers.
2. Make and **document** cleaning decisions (drop vs. fill, dedupe on which
   keys, how to normalize text) instead of applying functions blindly.
3. Convert dtypes and parse dates correctly, verifying the result after
   every step.
4. Run a structured EDA: univariate summaries and histograms, group
   comparisons, and correlations.
5. Produce 3–4 publication-quality visualizations that answer specific
   questions.
6. Write three evidence-backed findings (claim → number → plot).
7. Deliver a restart-safe, reproducible notebook plus a README that a
   stranger can follow.

## 2. Problem statement

The Registrar's office exported a student-records file and "it's a bit
messy — nobody has cleaned it since 2023." Your job: turn
`student-records-dirty.csv` into a defensible, analyzed dataset and tell the
Registrar three things they didn't know about their students. There is no
single "correct" cleaned file — there is a *justified* one. Every cleaning
decision you make must be recorded with a reason, because the grade rests on
the quality of your decisions and your ability to explain them, not on
matching a hidden answer key.

## 3. Requirements

- Python 3 + the course environment (`pip install -r ../requirements.txt`).
- Deliverables in a **private GitHub repository** named
  `assignment-01-data-cleaning` (see GitHub requirements).
- The notebook must run top-to-bottom (Restart & Run All) with no errors.
- No internet required — everything uses the provided CSV.
- You may use AI assistance **only** under the academic-integrity rules in
  §11.

## 4. Dataset requirements

- File: `student-records-dirty.csv` (in this folder; ~200 rows, 10 columns).
- Columns: `student_id`, `name`, `gender`, `program`, `semester`, `gpa`,
  `attendance_pct`, `email`, `enrolled_date`, `study_hours`.
- The data contains (deliberately): missing values, complete and
  near-duplicate rows, mixed-case and whitespace-padded text, stringy
  numbers, two date formats, and impossible values (GPA > 4.0, attendance
  outside 0–100, extreme study hours).
- Do **not** modify the original CSV; read it and write your cleaned version
  to `data/student-records-clean.csv` inside your repo.

## 5. Tasks

### Part A — Quality audit (20%)
1. Load the CSV and print `shape`, `info()`, `head()`, `describe()`.
2. Produce a missing-value table (per column: count + %).
3. Find complete duplicates (`duplicated()`) and near-duplicates on `email`
   and `student_id`.
4. List every column whose dtype is wrong for its content, and why.

### Part B — Cleaning (30%)
5. Handle missing values per column — for each column state **drop or fill
   and why** (e.g., GPA missing at random vs. attendance missing).
6. Remove complete duplicates; deduplicate on `email` keeping the first
   occurrence; decide what to do with duplicate `student_id`s and justify.
7. Normalize text: `gender`, `program`, `semester` (strip, case, and map
   variants to canonical values).
8. Convert `gpa` and `attendance_pct` (and `study_hours`) to proper dtypes;
   handle stringy numbers (commas/whitespace) if present.
9. Parse `enrolled_date` to `datetime` and extract `enroll_year`,
   `enroll_month` (or semester mapping) columns.
10. Flag and decide on impossible values (GPA > 4.0, attendance outside
    0–100). Justify keep vs. remove for each.
11. Save the cleaned frame to `data/student-records-clean.csv`
    (`index=False`) and **verify** the round-trip (shape + dtypes).

### Part C — EDA (30%)
12. Univariate: histograms for `gpa`, `attendance_pct`, `study_hours`;
    `value_counts` for `program`, `gender`, `semester`.
13. Group comparisons: mean GPA by program; mean attendance by semester;
    study hours by program. Show as small tables.
14. Relationships: correlation heatmap of numeric columns; a scatter of
    `study_hours` vs. `gpa` (do hours correlate with grades?).
15. Three visualizations minimum (from: histogram, boxplot, bar, scatter,
    heatmap) — each with a title, axis labels, and a one-line caption.

### Part D — Findings & write-up (20%)
16. Write **three findings**, each in the pattern:
    *claim → evidence (exact number) → plot reference*.
    Example: "DS students average ~3.2 GPA vs ~2.9 for AI — the GPA gap is
    visible in the program boxplot (Fig 2)."
17. Write a **cleaning log**: one line per decision
    (`action | column | rows affected | reason`). This is a deliverable,
    not an afterthought.
18. A "limitations" paragraph: what could still be wrong with the data or
    your cleaning choices?

## 6. Expected deliverables

| # | Deliverable | Where |
|---|---|---|
| 1 | Executed, restart-safe notebook `analysis.ipynb` | repo root |
| 2 | Cleaned dataset `student-records-clean.csv` | `data/` |
| 3 | Cleaning log (markdown cell or `cleaning-log.md`) | notebook / repo |
| 4 | Three findings + limitations paragraph | `README.md` (summary) and notebook |
| 5 | `README.md` (see §8) | repo root |
| 6 | Regenerated figure files (optional, if saved) | `figures/` |

## 7. GitHub requirements

- Private repo: `assignment-01-data-cleaning` (invite your instructor).
- **At least 4 commits** spread over the working period (not one giant
  commit) — history shows your process.
- Meaningful commit messages (why, not just what).
- Push before the deadline; the version on `main` at the deadline is
  graded.
- Commit the generated cleaned CSV and figures, but **not** `.venv/`,
  `__pycache__/`, or `.ipynb_checkpoints/` (`.gitignore` provided in the
  course repo).

## 8. README requirements

Your repo's `README.md` must contain:

1. Assignment title, your name, and submission date.
2. A 3–4 sentence summary of what you did and what you found.
3. The three findings (claim + number + plot reference).
4. "How to run": exactly three commands (create venv, install
   requirements, open notebook).
5. A short "Known issues / limitations" section.
6. An **AI-use disclosure** line: if you used AI assistance, what for, and
   what you verified yourself (see §11).

## 9. Grading rubric

| Criterion | Max | Notes |
|---|---|---|
| Quality audit complete (missing, dup, dtypes) | 15 | all four sub-checks |
| Cleaning decisions justified | 20 | drop/fill + dedupe + normalization with reasons |
| Correctness: dtypes, dates, no data loss unexplained | 15 | verify round-trip |
| EDA depth (univariate + group + correlation) | 15 | tables + heatmap + scatter |
| Visualizations (3+, labeled, captioned) | 15 | quality over quantity |
| Findings (3, claim→number→plot) | 10 | evidence grounded |
| Cleaning log + limitations | 10 | every decision logged |
| **Total** | **100** | |

Deductions: unexecuted notebook (−10), no git history (−10), missing README
sections (−5 each), AI use without disclosure (see §11).

## 10. CLO mapping

| Task group | CLO | How |
|---|---|---|
| A, B | CLO-1 | acquire/clean/manipulate datasets with pandas |
| C | CLO-1 | visualize and explore datasets |
| D | CLO-1 | communicate findings; documentation discipline |
| §8 (README) | CLO-1, CLO-3 | reproducibility; documenting the workflow |

## 11. Academic integrity rules

- Work is **individual**. Discuss approaches with classmates freely, but
  write your own code and text.
- **AI use is permitted with disclosure** (course policy,
  `../assessment-plan.md`): you must (1) disclose the tool + prompts + how
  the output was used in the README, (2) verify that AI-generated code runs
  and you can explain every line you submit, (3) never submit AI-generated
  findings without checking them against the data.
- Submitting another student's cleaned file or copying code without
  attribution is plagiarism and follows institutional policy.
- You may be asked to explain your work in person; inability to explain is
  treated as unverified submission.