# Streamlit · 06 — Caching, Session State, and an ML Prediction App

**Time:** ~75 min · **CLOs:** CLO-1, CLO-2, CLO-3 · **Level:** Intermediate
**Prerequisite:** a basic scikit-learn model (Module B, e.g. k-NN from
Session 19).

---

## 1. The two problems every app hits

Because the script re-runs on **every interaction**, two things happen that
surprise beginners:

1. **Expensive work repeats.** Training a model, loading a big CSV, or
   computing a correlation runs again on *every slider move*.
2. **Variables reset.** Any normal variable is recomputed from scratch on
   every rerun — so "remember the user's name" doesn't work with plain
   variables.

Streamlit gives you exactly two tools for these two problems:
**caching** (problem 1) and **session state** (problem 2).

## 2. Caching — run expensive work once: `@st.cache_data`

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """Runs ONCE, then the result is reused on every rerun."""
    return pd.read_csv("big_file.csv")

df = load_data()
```

**What happens:** the first rerun calls `load_data()` and stores the result.
Every later rerun (new slider value, new click) reuses the stored result —
**as long as the arguments are the same.** If you call with different
arguments, it caches each combination separately.

**The rule:** cache *data loading* and *model training* (pure functions that
return data). Don't cache things that depend on widgets:

```python
@st.cache_data
def train_model(X, y):
    """Trains once per (X, y) combination — not on every rerun."""
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X, y)
    return model
```

## 3. Session state — remember things across reruns: `st.session_state`

`st.session_state` is a dictionary that **survives reruns** for the current
browser session:

```python
if "counter" not in st.session_state:     # first run: create it
    st.session_state.counter = 0

if st.button("Increment"):
    st.session_state.counter += 1         # persists across reruns

st.write("Count:", st.session_state.counter)
```

**The pattern:** initialize *if missing*, then read/write freely. Without
session state, `counter = 0` would reset to 0 on every rerun and the count
could never grow.

When do you need it in this module?

- counters and toggles that must persist;
- chat history (Module C topic 11);
- a model that should be trained *once per session* rather than per rerun
  (caching already covers this — session state is for *user-specific*
  memory, caching is for *expensive computation*).

## 4. Displaying ML predictions

A prediction app = widgets for features → `model.predict` → display:

```python
st.success(f"The predicted species is **{prediction}**")
st.metric("Confidence", f"{probability:.1%}")
```

Use `st.metric` for a single number and `st.success`/`st.info` for
sentences. Never display a bare array — format it for humans.

---

# Example 5 — ML Prediction Application

A complete app: train a k-NN classifier on the iris dataset once (cached),
let the user set the four flower measurements with sliders, and show the
predicted species with confidence.

## Explanation

The app separates the two jobs: **training** (expensive, cached, happens
once) and **prediction** (cheap, runs on every slider move). The sliders
are the features; the model predicts the species and the probability of
each class. Because training is cached, moving a slider never retrains —
only the prediction line re-runs.

## Code

Save as `app.py`:

```python
import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

st.title("🌸 Iris Flower Predictor")
st.markdown("Set the four measurements and predict the iris species.")

# 1) Load + train ONCE (cached — not on every rerun)
@st.cache_data
def load_data():
    data = load_iris(as_frame=True)
    return data.frame

@st.cache_data
def train_model():
    df = load_data()
    X = df[["sepal length (cm)", "sepal width (cm)",
            "petal length (cm)", "petal width (cm)"]]
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    return model, X_test, y_test

model, X_test, y_test = train_model()

# 2) Show a little honesty: how good is the model?
accuracy = model.score(X_test, y_test)
st.caption(f"Model accuracy on held-out test data: {accuracy:.1%}")

# 3) Features as sliders
st.header("Set the measurements")
sepal_length = st.slider("Sepal length (cm)", 4.0, 8.0, 5.8, step=0.1)
sepal_width = st.slider("Sepal width (cm)", 2.0, 4.5, 3.0, step=0.1)
petal_length = st.slider("Petal length (cm)", 1.0, 7.0, 3.8, step=0.1)
petal_width = st.slider("Petal width (cm)", 0.1, 2.5, 1.2, step=0.1)

# 4) Predict (cheap — runs on every rerun)
features = pd.DataFrame([[sepal_length, sepal_width,
                          petal_length, petal_width]],
                        columns=X_test.columns)
prediction = model.predict(features)[0]
probabilities = model.predict_proba(features)[0]
species = ["setosa", "versicolor", "virginica"]

st.header("Prediction")
st.success(f"Predicted species: **{species[prediction]}**")
st.metric("Confidence", f"{max(probabilities):.1%}")
```

## Expected result

- A caption with test accuracy (with `random_state=42`: ≈ 97.8%).
- Four sliders with sensible defaults (5.8, 3.0, 3.8, 1.2 — the dataset
  means), so the very first prediction is already meaningful.
- A green success line with the predicted species and a confidence metric.
- Move one slider → the prediction updates instantly, **without retraining**
  (you can tell: the app never hesitates).

## Exercise

1. Add a `st.selectbox` for `n_neighbors` (1–15) that *retrains* the model
   when changed — remove the cache from `train_model` (or add
   `n_neighbors` as a parameter) and watch the accuracy caption change.
2. Show the full probability breakdown:
   ```python
   for s, p in zip(species, probabilities):
       st.write(f"{s}: {p:.1%}")
   ```
3. Add `st.progress(max(probabilities))` under the confidence metric.

## Challenge

Replace the dataset: switch to `sns.load_dataset("penguins")` and predict
**species from bill length, bill depth, flipper length, and body mass**
(drop rows with missing values first — penguins has some!). Keep caching,
add a `st.selectbox` for the model (`KNeighborsClassifier` vs
`LogisticRegression`), and display test accuracy for the chosen model. You
have just built a model-comparison app.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Model retrains on every slider move | cache `train_model` with `@st.cache_data` |
| Cache "not working" | arguments changed (e.g. a widget value) — cache by *data*, not by widget |
| Counter resets to 0 | use `st.session_state`, not a plain variable |
| `st.session_state` KeyError | initialize first: `if "key" not in st.session_state` |
| Prediction app crashes on empty dataframe | check `len(X_test)` after dropping missing values |
| Showing raw probabilities array | format with f-strings / `st.metric` |

## Checkpoint questions

1. What is the difference between `@st.cache_data` and
   `st.session_state`? **CLO-1 · Understand · Medium**
   **Answer:** caching stores the *result of an expensive function* keyed by
   its arguments (shared, computation-focused); session state stores
   *variables across reruns* per user session (memory-focused). Caching
   stops repeated work; session state stops resetting values.
2. Why is it safe for the model to be cached but the sliders to re-run the
   prediction? **CLO-2 · Analyze · Medium**
   **Answer:** training is the expensive, dataset-dependent step and is
   identical every rerun; prediction is cheap, instant, and depends on the
   current widget values — so only it should re-run.
3. Your cache "doesn't work" — the model retrains every time you move a
   slider. What's the most likely cause? **CLO-2 · Evaluate · Medium**
   **Answer:** the cached function receives widget-dependent arguments
   (e.g. `n_neighbors` from a selectbox), so every change creates a new
   cache entry — cache training on fixed inputs, or only the data loading.