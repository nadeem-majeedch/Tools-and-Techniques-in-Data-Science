# Lab 31 — Solution: Project Presentations

**Session:** W16 S31 · **CLO:** CLO-3

## Worked example (skeleton)

```markdown
# Presentation — Predicting Penguin Species from Body Measurements
**Team:** A. Student, B. Student   **Presenting session:** 31

## Slide 1 — Question
Can two bill measurements predict penguin species?
Why it matters: field ID is manual; automation saves time and reduces error.

## Slide 2 — Data
Source: Palmer Penguins (seaborn, CC0) | License: public domain
Shape: 344 x 7 (333 after dropna) | Fixed: 11 missing sex rows dropped;
missingness was small and non-systematic.

## Slide 3 — Method
Model: k-NN (k=5) vs logistic regression, scaled features
Metric: test accuracy + per-class recall
Why: small dataset, 3 well-separated classes — these models suffice.

## Slide 4 — Results
Chart: scatter bill length vs depth colored by species
Answer: test accuracy 0.97 (logistic), Chinstrap recall 0.93

## Slide 5 — Limits & next
- Only 3 colonies sampled; may not generalize
- Next: flipper/mass features, cross-validation report

## Peer feedback received
| From | Strengths (3) | Improvements (2) |
|---|---|---|
| Team C | clear question; good chart; honest limits | slide 3 had no axis labels; define "recall" for the audience |

## Fix list
- [x] must-fix: add axis labels to slide-3 chart; re-export figure
- [x] must-fix: replace "accuracy 0.97" with "0.97 test accuracy, n=100"
- [ ] nice-to-have: animation on the scatter
```

## Dry-run evidence

Re-ran `models.ipynb` (Restart & Run All): chart re-rendered, accuracy
cell prints `0.97`. Fallback if live demo fails: show the saved PNG +
printed metric from the README.

## Model answers

1. **Show a limitation you fixed** — it demonstrates the data-quality
   workflow (a course learning outcome) and preempts the obvious
   question; hiding it looks like you missed it.
2. **The one number** — the single metric that directly answers the
   question (e.g., "0.97 test accuracy"); chosen because stakeholders
   remember one number, and it's the one tied to your success metric.
3. **Hard time stop** — talks overrun into the interesting middle
   (method/results); rehearsing with a stop reveals which section eats
   the clock so you can cut it.
4. **Actionable feedback** — specific, tied to evidence ("slide 3 chart
   has no y-axis label", "define recall") rather than global judgments;
   the receiver can act on it without guessing.
5. **Demo fallback** — a pre-saved figure and printed numbers let you
   continue without network/live execution; planned in advance because
   mid-talk improvisation is exactly when demos die.

## Challenge solution

> **Takeaway:** "Penguin species can be identified from two bill
> measurements with 97% test accuracy — the measurements are bill length
> and depth, which separate all three species."
> Final rehearsal: 5 min 40 s; slide 3 (method) still needs −20 s.

Peer-review scoring anchor: use the 1–5 rubric per criterion; a "3" needs
both chart AND number; a "5" needs justified metric choice plus limits.