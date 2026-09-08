# Assessment Plan

## 1. Components and weights

| Component | Count | Weight* | When | CLOs |
|---|---|---|---|---|
| Labs | 32 | 25% | Weekly, due before the next session | 1, 2, 3 |
| Quizzes | 2 | 10% | W8 S15, W15 S29 (session start, ~25 min) | 1, 2, 3 |
| Assignments | 2 | 15% | See schedule | 1, 3 |
| Midterm exam | 1 | 15% | W8 S16 | 1, 2 |
| Final exam | 1 | 15% | W16 S32 | 1, 2, 3 |
| Final project | 1 | 20% | Kickoff W12, presentations W16 | 1, 2, 3 |
| **Total** | | **100%** | | |

\* Weights are a **proposal** intended to balance continuous practice with
summative assessment; instructors should confirm them against program policy.

## 2. Component details

### Labs (32 × ~0.8% = 25%)
Hands-on exercises completed largely in class and finished at home. Each lab has
stated objectives, a starter notebook, tasks, and 2–3 checkpoint questions.
Graded for correctness of the notebook, code quality, and answers to checkpoint
questions. See `labs/`.

### Quizzes (2 × 5% = 10%)
Short, closed-notes, in-class quizzes (multiple choice, code tracing,
debugging, short answer, and scenario items) covering the preceding weeks:
Quiz 1 = Weeks 1–7, Quiz 2 = Weeks 8–14. Full question banks with keys in
`quizzes/` (quiz-1.md, quiz-2.md).

### Assignments (2 × 7.5% = 15%)
Larger individual tasks, submitted via a private GitHub repository (or as
specified by the instructor):

1. **Assignment 1 — Data cleaning & EDA (CLO-1):** clean a provided messy
   dataset with a documented cleaning log, run a structured EDA, and write
   evidence-backed findings. See `assignments/assignment-01-data-cleaning-eda/`.
2. **Assignment 2 — API + data acquisition + Streamlit app (CLO-1, CLO-3):**
   fetch data from an API/public dataset, clean and explore it, and ship an
   interactive Streamlit application with user controls, documented in a README
   and committed to GitHub. See `assignments/assignment-02-api-streamlit-app/`.

Machine-learning modeling is assessed through Labs 17–22, Quiz 2, the final
exam, and the final project's modeling component.

### Midterm exam (15%)
Written portion (concepts, code reading) + practical notebook task (CLO-1 with
an entry-level CLO-2 task). Open-notes notebook allowed for the practical part
as specified by the instructor.

### Final exam (15%)
Comprehensive: CLO-1, CLO-2, and CLO-3 concepts, including a short
AI-ethics/reproducibility section.

### Final project (20%)
Team of 2–3 students; end-to-end data science project from a problem statement
to an analysis with a basic model and an AI-assisted or automated component.
Deliverables: proposal (W13), GitHub repository, presentation (W16), final
submission with a reproducibility + ethics reflection. See `projects/`.

## 3. Rubric sketch

| Criterion | Weight (project) | Description |
|---|---|---|
| Problem framing & data acquisition | 20% | Clear question; appropriate, documented data sources |
| Cleaning & EDA | 25% | Sound cleaning steps; insightful exploration (CLO-1) |
| Modeling | 25% | Appropriate basic model; honest evaluation (CLO-2) |
| AI-assisted / automation component | 15% | Meaningful, working use of LLM/automation tools (CLO-3) |
| Reproducibility & ethics reflection | 10% | Environment, seeds, version control; bias/privacy considerations |
| Presentation & communication | 5% | Clear, well-paced presentation; answers questions |

Labs and assignments are graded on correctness, code quality, and completeness
of required outputs; rubrics are included in each deliverable folder.

## 4. Policies

### Submission
- All code-based deliverables are submitted via Git/GitHub (commit history
  visible). Notebooks must be **executed and saved** with visible outputs.
- Late submissions: −10% per day (or per program policy), up to 3 days; contact
  the instructor before the deadline for extensions (medical/family reasons).

### Academic integrity & AI use
- Submitted code must be understood by the student; the instructor may ask any
  student to explain their work.
- Because CLO-3 explicitly covers AI-assisted workflows, AI tools **may** be used,
  with these rules:
  1. **Disclose** any AI assistance (tool, prompt, and how output was used) in a
     short note attached to the deliverable.
  2. **Verify** AI-produced code: it must run, and you must be able to explain it.
  3. AI assistance for *exams and quizzes* is not permitted unless stated otherwise.
- Plagiarism of peers' or external code without attribution follows standard
  institutional policy.

### Attendance
2+ unexcused absences in the same module may require completion of a make-up
task; per program policy.

### Re-grading
Requests within 1 week of grade release, in writing, stating the specific issue.