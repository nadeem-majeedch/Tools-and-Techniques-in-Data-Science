# Tools

Small student-facing utilities that support the course.

## Grade Calculator (Sessional 25 · Mid 35 · Final 40)

A friendly Streamlit app for answering "where do I stand?" — using the
**confirmed institutional scheme** documented in
[`assessment-plan.md`](../assessment-plan.md):

| Institutional component | Marks |
|---|---|
| Sessional | 25 |
| Mid Exam | 35 |
| Final Exam | 40 |
| **Total** | **100** |

Because the maximum is exactly 100 marks, **Final Percentage = Sessional +
Mid Exam + Final Exam** — no normalization is required. The app then maps
the percentage to a letter grade and grade points using the **official
grading scale** (A = 85%+ · 4.00 … F = below 50% · 0.00).

```bash
streamlit run tools/grade_app.py
```

What you get:

- one number field per institutional component
  (Sessional 0–25, Mid Exam 0–35, Final Exam 0–40; leave future components
  empty);
- the total out of 100 (= percentage), letter grade and grade points;
- validation that rejects impossible marks (negative or above maximum);
- a built-in worked example — **20 + 28 + 33 = 81 → A- (3.70)** — shown
  until you submit your own marks (a perfect 25 + 35 + 40 = 100 gives
  **A (4.00)**);
- the official grading scale in an expandable panel.

### Files

| File | Purpose |
|---|---|
| `grade_app.py` | Streamlit front end (widgets + presentation only) |
| `grade_calculator.py` | Pure calculation logic + official scale + validation, self-tested |

Run the logic self-test (no Streamlit needed):

```bash
python tools/grade_calculator.py
# -> grade calculator self-test passed
```

The scheme and the official grading scale are documented in
[assessment-plan.md §1–§3](../assessment-plan.md).
