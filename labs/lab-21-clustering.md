# Lab 21 — Clustering: k-means & the Elbow

**Session:** Week 11 · Session 21 · 90 min
**CLO:** CLO-2
**Difficulty:** Intermediate

## Learning objectives

By the end of this lab you can:

1. Explain unsupervised learning and k-means in plain words.
2. Scale features before clustering and say why.
3. Choose k with the elbow method (and read its limits).
4. Validate clusters against known labels when available.

## Problem statement

No labels: the lab wants to know whether penguins *naturally* form groups
from body measurements alone. You must run k-means over k = 1..8, justify
a k with the elbow method, and then — because species labels actually exist
— check how well the discovered clusters match reality.

## Dataset requirements

Seaborn built-in `penguins`, `dropna()` (333 rows). Features:
`bill_length_mm`, `bill_depth_mm`, `flipper_length_mm`, `body_mass_g`.
Keep `species` aside as ground truth.

## Step-by-step tasks

1. **Prep:** dropna; `X = penguins[features]`; scale with
   `StandardScaler().fit_transform(X)`. Comment: why scale before k-means?
2. **Elbow:** for `k` in 1..8, fit `KMeans(n_clusters=k, random_state=42,
   n_init=10)` and record `kmeans.inertia_`. Plot inertia vs k (markers +
   line). Mark where the elbow is.
3. **Choose k** from the elbow; fit k-means with that k and
   `random_state=42`.
4. **Visualize:** `sns.scatterplot(x=scaled[:, 0], y=scaled[:, 1],
   hue=labels, palette="Set2")` plus cluster centers
   (`kmeans.cluster_centers_` as big markers). Scatter the *first two*
   scaled features — name them in the axis labels.
5. **Ground truth check:** build
   `pd.crosstab(penguins["species"], labels)` (species × cluster). If
   clusters align with species, each species row should concentrate in one
   cluster. Report the crosstab and say whether the discovered groups match
   the 3 species.
6. **Honest note:** write one sentence on what the elbow method can and
   cannot tell you (e.g., it's a heuristic; real-world clusters are rarely
   this clean).

## Starter code

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

penguins = sns.load_dataset("penguins").dropna()
features = ["bill_length_mm", "bill_depth_mm",
            "flipper_length_mm", "body_mass_g"]
X = StandardScaler().fit_transform(penguins[features])

# your code here: inertia sweep, elbow plot, chosen k, fit, scatter,
#                 crosstab, honest note
```

## Expected output

- Inertia decreases monotonically with k; the elbow is visible at k = 3
  (big drop from 1→3, then flattening) — possibly a slight bend at 2.
- Chosen k = 3 (or 4, if justified) with reasoning.
- Scatter of the two most informative scaled features showing 2–3 clear
  blobs; centers plotted.
- Crosstab: cluster 0 ≈ Adelie, cluster 1 ≈ Chinstrap, cluster 2 ≈ Gentoo
  (or a near-diagonal permutation) — clusters largely match species.
- One honest sentence about the elbow's limits.

## Questions

1. What does `inertia_` measure, and why does it always drop as k grows?
2. Why must features be scaled before k-means, given what the algorithm
   computes (distances)?
3. What does `n_init=10` do, and why is it needed (k-means is
   initialization-sensitive)?
4. Clusters match species almost perfectly here. What would it mean if they
   did *not*?
5. k-means finds spherical clusters. What kind of data would it fail on?

## Challenge task

Run k-means on **unscaled** features and show the elbow plot side by side
with the scaled one. Answer: does scaling change the elbow's location?
Then compute a simple agreement score: the fraction of rows where the
cluster label matches its species (after mapping clusters to species by
majority vote with `pd.crosstab(...).idxmax(axis=1)`). Report the fraction.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| Prep + scaling rationale | 4 | scale + comment |
| Elbow sweep + plot | 5 | 1..8, marked elbow |
| k chosen + reasoning | 3 | ties to plot |
| Cluster scatter + centers | 4 | labels + centers visible |
| Crosstab + species match verdict | 4 | diagonal reading |
| Honest note | 2 | limits of elbow |
| Answers to questions | 3 | Q1, Q2, Q4 correct |
| Challenge: unscaled comparison + agreement | 5 | side-by-side + fraction |
| **Total** | **30** | |