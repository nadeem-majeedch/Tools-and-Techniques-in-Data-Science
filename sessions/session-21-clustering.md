# Session 21 — Unsupervised Learning: k-Means Clustering

**Week 11 · Session 21 · Module B · 90 min · CLO-2**

## 1. Learning objectives

By the end of this session, students can:
- Explain unsupervised learning and how it differs from supervised learning.
- Explain what k-means does: assign points to k centers, iteratively.
- Fit `KMeans` with scikit-learn and inspect `labels_` and `cluster_centers_`.
- Choose k with the elbow method and interpret the result.
- Scale features before clustering and explain why.
- Judge when clusters are meaningful vs. an artifact of the algorithm.

## 2. Key concepts

- **Unsupervised learning = no labels**: the algorithm finds structure (groups) on its own.
- **k-means:** pick k centers → assign each point to its nearest center → move centers to the group mean → repeat.
- **`inertia`** = total squared distance of points to their center — the number the elbow plot reads.
- **The elbow method:** plot k vs. inertia; the "bend" suggests a sensible k.
- **Scale first:** k-means uses distance — a feature in big units silently dominates.
- Clusters are *descriptive*, not proven truths — validate with domain knowledge and plots.

## 3. Detailed lecture notes

**Why unsupervised?** Supervised learning needs answers (labels) for training —
but often nobody has labeled the data. Who labeled millions of customers as
"segment A"? Instead, clustering finds groups *from the data alone*: similar
observations, no ground truth required. This is how market segmentation, anomaly
detection (points far from any cluster), and document grouping work. The trade:
there's no accuracy score — "good clusters" is a judgment call, which is why
visualization and domain sense matter here more than anywhere in Module B.

**How k-means works (the algorithm).** Four steps, repeat until stable:
1. Choose k and place k initial centers (randomly; scikit-learn does this smartly).
2. **Assign** each point to its nearest center.
3. **Update** each center to the mean of its assigned points.
4. Repeat 2–3 until assignments stop changing.
Walk this by hand on 6 points with k=2 on the whiteboard (or a slow-motion demo
with `max_iter=1, 2, 3`). The name finally makes sense: the *mean* of a group
becomes the new center; the groups are the *k* clusters. Sensitive to starting
centers → `random_state` matters; scikit-learn runs several initializations by
default (`n_init`).

**Picking k — the elbow method.** `KMeans(n_clusters=k).fit(X)`; read
`model.inertia_` (sum of squared distances to centers). More clusters always
lower inertia (each point closer to its center). Plot k vs. inertia: the curve
falls steeply, then bends — the "elbow" — and the bend is your k. Why? Before
the elbow each added cluster buys a big drop (real structure); after, you're
splitting noise for small gains. Caveat to teach honestly: elbows are often
*rounded* — treat k as a recommendation, then look at the actual clusters and
ask "do they tell a useful story?"

**Scaling — the distance problem.** k-means assigns by Euclidean distance. A
feature measured in rupees (0–50,000) swamps a feature in hours (0–24); the
"distance" is basically the salary column alone. Fix: `StandardScaler` — subtract
mean, divide by std, every feature now lives in comparable units (z-scores from
Session 6!). The scaler must be fit on data *before* clustering (Session 22
formalizes this into pipelines). Demonstrate: cluster `penguins` measurements
scaled vs. unscaled and show how the clusters shift.

**Are the clusters real?** k-means always finds k groups — even in pure noise.
Checks: (1) plot the clusters on a 2-D projection (first two features, or a
scatter of the two most informative); do they look separated or smeared?
(2) Cross-tabulate clusters against a *known* label if you have one
(`pd.crosstab(clusters, species)`) — for penguins the clusters should line up
with species; (3) sanity-check the cluster centers against domain knowledge.
This skepticism — "the algorithm found something; is it *meaningful*?" — is
exactly the critical thinking CLO-2 wants.

## 4. Important terminology

- **Unsupervised learning** — finding structure without labels.
- **Clustering** — grouping similar observations.
- **k-means** — center-based clustering: assign → update → repeat.
- **Centroid / cluster center** — the mean of a cluster's points.
- **`labels_`** — cluster assignment per point.
- **`inertia`** — sum of squared distances of points to their centers.
- **Elbow method** — choosing k at the bend of the inertia curve.
- **`n_init`** — number of random restarts (scikit-learn picks the best).
- **`StandardScaler`** — z-score transform so features are comparable.
- **Feature scaling** — standardizing units before distance-based methods.
- **Cross-tabulation** — comparing clusters to known labels (`pd.crosstab`).

## 5. Python examples

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
%matplotlib inline

np.random.seed(42)
# Two obvious blobs + a cloud: k=2 should find the blobs
X = np.vstack([np.random.normal([0, 0], 0.4, (100, 2)),
               np.random.normal([4, 4], 0.4, (100, 2))])

model = KMeans(n_clusters=2, random_state=42, n_init=10)
model.fit(X)
print("Labels:", model.labels_[:5])
print("Centers:\n", model.cluster_centers_)
print("Inertia:", round(model.inertia_, 2))

plt.scatter(X[:, 0], X[:, 1], c=model.labels_, cmap="viridis", alpha=0.7)
plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1],
            marker="x", s=200, color="red", label="centers")
plt.legend()
plt.show()

# --- Elbow: how many clusters? ---
inertias = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X).inertia_
            for k in range(1, 9)]
plt.plot(range(1, 9), inertias, "o-")
plt.xlabel("k"); plt.ylabel("inertia"); plt.title("Elbow plot")
plt.show()
```

## 6. Beginner example

```python
from sklearn.cluster import KMeans
import numpy as np

X = np.array([[1, 1], [1, 2], [2, 1],    # group 1
              [10, 10], [11, 10], [10, 11]])  # group 2

km = KMeans(n_clusters=2, random_state=0, n_init=10).fit(X)
print(km.labels_)          # [0 0 0 1 1 1]
print(km.cluster_centers_) # two centers: ~(1.3, 1.3) and ~(10.3, 10.3)
```

Six obvious points, two clusters found — the entire k-means idea in five lines.

## 7. Practical Data Science example

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
%matplotlib inline

penguins = sns.load_dataset("penguins").dropna()

# Cluster on measurement columns — scale first so units are comparable
features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
X = penguins[features]
X_scaled = StandardScaler().fit_transform(X)

# Elbow
inertias = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled).inertia_
            for k in range(1, 8)]
plt.plot(range(1, 8), inertias, "o-")
plt.title("Elbow for penguins"); plt.xlabel("k"); plt.ylabel("inertia")
plt.show()

# k=3 (matches the three species)
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_scaled)
penguins["cluster"] = km.labels_

# Does the unsupervised grouping match the known species?
print(pd.crosstab(penguins["cluster"], penguins["species"]))

sns.scatterplot(data=penguins, x="bill_length_mm", y="flipper_length_mm",
                hue="cluster", style="species")
plt.title("Clusters (color) vs species (markers)")
plt.show()
```

## 8. In-class activity (50 min)

In `notebooks/week-11/session-21-clustering.ipynb`:

1. **Hand-run k-means (15 min):** on the two-blob example, fit with
   `max_iter=1` then `max_iter=3`; print `labels_` each time to watch the
   assignments settle (the slow-motion version of the algorithm).
2. **Elbow (15 min):** build the elbow plot for `penguins` (scaled). Where's the
   bend? Justify k=3 in one sentence.
3. **Scale experiment (10 min):** cluster *unscaled* penguins with k=3; cross-tab
   against species and compare with the scaled run. What changed and why?
4. **Skepticism (10 min):** cross-tab clusters vs. species; which species are
   confused? Link to the pairplot overlap from Session 14.

## 9. Lab exercise

**Lab 7** (due Session 22): `labs/lab-07/` — clustering & pipelines: k-means on
a scaled dataset, elbow plot, cluster-vs-label cross-tab, plus a first
`Pipeline` preview (scaler → k-means). Checkpoint questions included.

## 10. Common mistakes

- Clustering without scaling → one dominant feature drives everything.
- Reading clusters as "real" without plotting or validating against known labels.
- Choosing k by inertia alone — inertia always falls with k; read the *bend*.
- Forgetting `random_state`/`n_init` → different clusters across runs.
- Using clusters from k-means as features without checking stability.
- Thinking "no labels" means "no validation" — cross-tabs and domain sense still apply.
- Using `pd.crosstab` on clusters vs. species and expecting exact agreement — confusion is information, not failure.

## 11. Short assessment questions

1. What is the difference between supervised and unsupervised learning?
2. Describe k-means in four steps.
3. What does `inertia` measure, and why does it always decrease as k grows?
4. Why must features be scaled before k-means?
5. How do you check whether clusters are meaningful when you have a known label?
6. True/False: k-means can always find k clusters even in random noise. (True — that's why validation matters.)

## 12. CLO mapping

CLO-2: clustering completes the "basic machine learning techniques" (regression,
classification, clustering). The scale-first habit and cluster-validation
skepticism carry into pipelines (Session 22) and the final project's
exploratory modeling.

## 13. Suggested homework

- Finish Lab 7 and push before Session 22.
- Practice: cluster the `tips` dataset on `total_bill` and `tip` (scaled); interpret what the clusters mean to a restaurant.
- Read: scikit-learn docs — "Clustering" page (the k-means section only).
- Preview: `from sklearn.pipeline import Pipeline` — Session 22 wraps scaler + model into one object so you never forget scaling again.