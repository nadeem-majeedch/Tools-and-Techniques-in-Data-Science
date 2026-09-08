# Instructor Solutions

Complete worked solutions for all 32 labs — one file per lab, mirroring
`labs/lab-NN-*.md`. **Do not commit this directory to a student-facing
repository.**

## Contents

| File | Covers |
|---|---|
| `lab-01-*.md` … `lab-32-*.md` | Full code, expected outputs, model answers, and challenge solutions for every lab |

## How each solution is organized

- **Complete code** — every task's working code, executable against the
  course's built-in datasets (seaborn/sklearn) or the inline data in the
  lab.
- **Expected output** — the exact numbers a correct run produces (where
  deterministic; otherwise the correct range/structure).
- **Model answers** — the "Questions" section answered.
- **Challenge solutions** — worked code for the challenge task.

## Notes

- Labs 11, 16, 29 hit the keyless Open-Meteo API; solutions cache results,
  so a rerun offline still reproduces the numbers.
- Labs 25–30 (LLM-dependent) always include the **mock/sample-output
  path**, so the solution is verifiable with no model installed. Real-model
  answers vary by model; the grading target is the verification, not the
  reply.
- All code is written for beginner clarity first: explicit steps, no
  unexplained advanced constructs.
- To distribute labs to students: share the `labs/` folder **excluding**
  this directory.