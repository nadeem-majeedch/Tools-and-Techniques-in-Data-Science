# Tools

Small student-facing utilities that support the course.

## Grade Calculator (25 / 35 / 40)

A friendly Streamlit app for answering "where do I stand?" — consistent with
the institutional scheme in [`assessment-plan.md`](../assessment-plan.md):

- **Continuous Assessment = 25%** — Labs 10% · Quizzes 5% · Assignments 10%
- **Midterm = 35%**
- **Final = 40%** — Final exam 25% · Final project 15%

```bash
streamlit run tools/grade_app.py
```

What you get:

- one number field per component (leave future components empty);
- a table of **raw marks → weight → weighted contribution**;
- bucket subtotals (Continuous / Midterm / Final) and the **final score out
  of 100** with an indicative letter grade;
- validation that rejects impossible marks (negative or above maximum);
- a built-in worked example (from the assessment plan) shown until you
  submit your own marks.

### Files

| File | Purpose |
|---|---|
| `grade_app.py` | Streamlit front end (widgets + presentation only) |
| `grade_calculator.py` | Pure calculation logic + validation, self-tested |

Run the logic self-test (no Streamlit needed):

```bash
python tools/grade_calculator.py
# -> grade calculator self-test passed
```

The formula is documented in [assessment-plan.md §2](../assessment-plan.md):
`weighted contribution = (your marks ÷ maximum marks) × component weight`,
final score = sum of contributions, out of 100.
