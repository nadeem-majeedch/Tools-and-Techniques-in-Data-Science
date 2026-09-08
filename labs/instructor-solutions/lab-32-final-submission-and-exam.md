# Lab 32 — Solution: Final Submission & Exam

**Session:** W16 S32 · **CLO:** CLO-1, CLO-2, CLO-3

## Checklist (all ✓ expected)

| Item | ✓/✗ |
|---|---|
| README: team, question, dataset, license | ✓ |
| requirements.txt with version header | ✓ |
| notebooks run top-to-bottom | ✓ |
| all random calls seeded | ✓ |
| README metric matches notebook | ✓ |
| AI disclosure included | ✓ |
| data sheet included | ✓ |
| presentation.md committed | ✓ |

Fixes: re-ran `models.ipynb` (README said 0.96, notebook printed 0.97 —
updated README to 0.97); added AI disclosure section from Lab 30.

## Self-assessment (model answer)

- Question clarity: 4 — clear, but "why it matters" could be sharper.
- Data transparency: 5 — source, license, and limitation documented.
- Method fit: 4 — k-NN vs logistic with CV; could have tuned k.
- Results communication: 4 — one chart + one number; legend too small.
- Limits: 5 — three threats with mitigations.
- With one more week I would: run GridSearchCV and add a second dataset
  for a generalization check.

## Exam review (model answers — write from memory first)

**Module A**
- Selection: `[]` (one column), `.loc` (labels), `.iloc` (positions),
  boolean mask (conditions). Each answers a different "where is it"
  question.
- `isna()` *detects* missing cells (returns boolean mask); `dropna()`
  *removes* rows/columns with missing values. Detect before you drop.
- `groupby(...).agg(...)` returns one row per group with the aggregated
  columns — shape (n_groups, n_aggregations).

**Module B**
- 4-step API: choose model → `fit(X_train, y_train)` → `predict(X_test)`
  → evaluate (accuracy/MAE/R²/confusion matrix).
- `train_test_split` protects against evaluating on training data
  (memorization); `random_state` fixes the split for reproducibility.
- accuracy = correct/total; precision = true pos / predicted pos; recall =
  true pos / actual pos. MAE = mean absolute error in target units; R² =
  fraction of variance explained.

**Module C**
- Agent loop: reason → propose tool call → your code executes → result
  returned as message → decide/answer.
- Registered-tools boundary guarantees: (1) the model can only request
  whitelisted functions; (2) all execution stays in your code with a
  transcript.
- AI-use policy: disclose (what/when), verify (numbers against data),
  understand (you can explain the code you used).
- n8n structure: trigger (schedule/webhook) → processing (HTTP/Code/
  Filter) → output (file/email).

## Model answers

1. **"Works on my machine" item** — the restart-safe, seeded, pinned
   notebooks + README run instructions: it proves a stranger can
   reproduce, which is the reproducibility CLO.
2. **README metric must match notebook** — the README is the first thing
   graders check; a mismatch reads as sloppy or inflated and undermines
   every other claim.
3. **Shape mismatch first check** — verify `X` and `y` row counts match
   (`X.shape`, `len(y)`); the classic cause is reusing `y` from an earlier
   cell after redefining `X` (the exact bug in notebook 10 during
   development).
4. **Disclosure requirements** — record the tool, prompts, and what you
   verified; omitting it risks an academic-integrity penalty, since
   undisclosed AI use looks like uncredited work.
5. **Most valuable habit** — verification discipline ("compute ground
   truth, check every number") or reproducibility (seeds + pins + clean
   notebooks); any answer with a concrete reason is correct.

## Challenge solution

```markdown
# retrospective.md
- Clicked early: boolean masks/filters — one idea, endless power.
- Warn next semester: don't skip the git lab; the merge conflict WILL
  happen to you.
- Use immediately: reproducibility checklist for every other course
  project.
- Go deeper: cross-validation and honest metric choice.
```