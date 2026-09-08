# Lab 21 — Solution: Clustering

**Session:** W11 S21 · **CLO:** CLO-2

## Complete solution

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
# scaling: k-means minimizes Euclidean distance; unscaled body_mass_g
# (range ~2700-6300) would dwarf bill_depth_mm (range ~13-21).

# elbow sweep
inertias = []
ks = range(1, 9)
for k in ks:
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
    inertias.append(km.inertia_)
plt.plot(list(ks), inertias, marker="o")
plt.xlabel("k"); plt.ylabel("inertia")
plt.title("Elbow plot")
plt.show()

# chosen k
k = 3
km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
labels = km.labels_

plt.figure()
sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette="Set2")
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
            marker="X", s=200, color="black", label="centers")
plt.xlabel("scaled bill_length_mm"); plt.ylabel("scaled bill_depth_mm")
plt.legend()
plt.show()

print(pd.crosstab(penguins["species"], labels))
```

## Expected output

- Inertia drops fast 1→3 then flattens: elbow at k=3.
- Scatter: 2–3 blobs; centers at the blob centers.
- Crosstab ≈ diagonal: e.g., species Adelie → cluster 1, Chinstrap → 2,
  Gentoo → 0 (permutation varies) — clusters match species.

## Model answers

1. **inertia_** — sum of squared distances from each point to its cluster
   center; adding clusters always lets points sit closer to a center, so
   inertia always decreases with k.
2. **Scale for distances** — k-means assigns by Euclidean distance; a
   feature with a large range dominates the distance and the other
   features effectively get ignored.
3. **n_init=10** — k-means starts from random centers and can land in a
   poor local optimum; running 10 restarts and keeping the best makes the
   result stable and reproducible.
4. **If clusters ≠ species** — the measurements don't separate the groups
   cleanly (or the "natural" grouping isn't species); you'd investigate
   which variables drive the clusters instead.
5. **k-means failures** — non-spherical/elongated clusters, nested or
   overlapping groups, and very different cluster densities all break the
   spherical, equal-variance assumption.

## Challenge solution

```python
X_raw = penguins[features].values
inertias_raw = [KMeans(n_clusters=k, random_state=42, n_init=10)
                .fit(X_raw).inertia_ for k in range(1, 9)]
# plot both curves on one figure; the scaled elbow at 3 is clearer; the
# unscaled curve bends less sharply.

# agreement: map each cluster to its majority species
cross = pd.crosstab(penguins["species"], km.labels_)
species_of_cluster = cross.idxmax(axis=0)      # species per cluster
predicted = species_of_cluster[km.labels_].values
agreement = (predicted == penguins["species"].values).mean()
print("cluster-species agreement:", round(agreement, 3))   # ~0.94-0.98
```