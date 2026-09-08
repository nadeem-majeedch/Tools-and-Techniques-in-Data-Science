# Lab 4 — Solution: ML Prediction App (Penguins)

## Complete app.py

```python
import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

st.title("Penguin Species Predictor")

# ---------- Data: loaded once ----------
@st.cache_data
def load_data():
    df = sns.load_dataset("penguins").dropna()   # 2 rows have missing values
    return df

# ---------- Training: cached on (model_name) — NOT on slider values ----------
@st.cache_data
def train_model(model_name):
    df = load_data()
    features = ["bill_length_mm", "bill_depth_mm",
                "flipper_length_mm", "body_mass_g"]
    X = df[features]
    y = df["species"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    if model_name == "k-NN":
        model = KNeighborsClassifier(n_neighbors=5)
    else:
        model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model, X_test, y_test

# ---------- Model choice (cache key) + honest accuracy ----------
model_name = st.selectbox("Model", ["k-NN", "LogisticRegression"])
model, X_test, y_test = train_model(model_name)
accuracy = model.score(X_test, y_test)
st.caption(f"Model: {model_name} · Test accuracy: {accuracy:.1%}")

# ---------- Features as sliders (means of the data as defaults) ----------
st.header("Measurements")
bill_length = st.slider("Bill length (mm)", 30.0, 60.0, 43.9, step=0.1)
bill_depth = st.slider("Bill depth (mm)", 13.0, 22.0, 17.2, step=0.1)
flipper = st.slider("Flipper length (mm)", 170, 235, 201, step=1)
mass = st.slider("Body mass (g)", 2700, 6300, 4200, step=50)

features = ["bill_length_mm", "bill_depth_mm",
            "flipper_length_mm", "body_mass_g"]
row = pd.DataFrame([[bill_length, bill_depth, flipper, mass]],
                   columns=features)
prediction = model.predict(row)[0]
probabilities = model.predict_proba(row)[0]
classes = model.classes_

# ---------- Prediction counter (session state) ----------
if "predictions" not in st.session_state:
    st.session_state.predictions = 0
st.session_state.predictions += 1

# ---------- Output ----------
st.header("Prediction")
st.success(f"Predicted species: **{prediction}**")
st.metric("Confidence", f"{max(probabilities):.1%}")
for cls, prob in zip(classes, probabilities):
    st.write(f"{cls}: {prob:.1%}")
st.caption(f"Predictions made this session: {st.session_state.predictions}")
```

## Expected numbers (seed 42, test_size 0.3)

- k-NN(5): test accuracy ≈ 0.971 (97.1%) on the 103-row test set.
- LogisticRegression: test accuracy ≈ 1.000 (100%) — easy, well-separated
  classes. Either is fine to report; the point is the honest caption.
- Default sliders (dataset means) predict **Adelie** (the most common
  species) with high confidence.
- The counter increments on every slider move and persists — session state.

## Model answers to the questions

1. **Why cache training but not prediction?** Training is the expensive,
   dataset-dependent step and is identical every rerun — caching it once
   per (model, data) combo removes the only slow part. Prediction is cheap
   and must reflect the current slider values, so it must re-run every
   time; caching it would freeze the answer at the first slider position.
2. **If training took slider values as arguments?** Every slider change
   would produce a new cache key and **retrain the model** — the exact
   slowdown caching is meant to prevent. Cache on stable inputs (model
   name, dataset), not on widget values.

## Challenge solution (model comparison)

Already included above: `train_model(model_name)` takes the model name as
its only argument, so switching the selectbox retrains (new cache key) while
moving sliders does not (same key). Students should report that
LogisticRegression achieves 100% here but k-NN generalizes the story better
— either conclusion is acceptable if argued from the numbers.