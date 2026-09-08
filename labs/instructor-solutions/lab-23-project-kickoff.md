# Lab 23 — Solution: Project Kickoff

**Session:** W12 S23 · **CLO:** CLO-2, CLO-3

## Worked example (penguins-based proposal)

```markdown
# Project Proposal (draft)
**Team:** A. Student, B. Student   **Date:** <date>

## Question
Can a penguin's body measurements predict its species, and which two
measurements separate the species most cleanly?

## Audience & decision
Biology lab technicians who currently identify species by hand; the
decision is which measurements to prioritize in field data collection.

## Dataset
- Source: Palmer Penguins (seaborn built-in; palmerpenguins package)
- License / provenance: CC0 public domain, collected by Dr. Kristen Gorman
- Shape: (344, 7)   Verified loads: yes

## Framing
- Target: species (3 classes)
- Features: bill length/depth, flipper length, body mass
- Type: supervised · classification

## Success metric
- CV accuracy >= 0.95 (5-fold) with a test-set check >= 0.90

## Top risks
1. Species overlap on available features -> mitigate: check pairplots and
   confusion matrix; may accept 2-class accuracy instead
2. Small dataset (333 rows after dropna) -> mitigate: stratified splits,
   report per-class recall, don't overclaim
3. Time spent on styling instead of analysis -> mitigate: analysis first,
   polish last
```

## Model answers

1. **Answerable with the data** — the question must be convertible into a
   computation on columns you have. Great: "does bill length differ by
   species?" Unanswerable: "why did penguin populations change?" (no time
   series / no causes measured).
2. **Target vs feature** — target = what you predict/explain (the
   answer); features = the inputs you use. Same row, different roles.
3. **Metric first** — it defines "done" objectively, prevents moving
   goalposts, and forces you to think about *what error costs* before you
   build anything.
4. **License/provenance** — a graded project must be reusable and legal:
   knowing the source lets you cite it, and public-domain/permissive data
   avoids plagiarism and redistribution problems.
5. **Misleading 90%** — on an imbalanced dataset, predicting the majority
   class can score >90% with zero learning; also, a single CV mean hides
   fold variance and leakage.

## Challenge solution

Threats-to-validity paragraph (model answer):

> Our conclusion — that two bill measurements separate the species — could
> be wrong if (1) the dataset is not a random sample: penguins were
> measured at three specific islands, so results may not generalize beyond
> those colonies; (2) missingness is not random: 11 rows dropped for sex
> could bias summaries; (3) our metric (accuracy) is misleading under
> class imbalance, hiding poor recall for the smallest class; (4) we tuned
> on the same split we evaluated, which leaks information; and (5) the
> "clusters" we see could be artifacts of the two features we chose to
> plot. Each risk has a mitigation: stratified CV, per-class metrics, a
> held-out test set used once, and robustness checks on different feature
> subsets.