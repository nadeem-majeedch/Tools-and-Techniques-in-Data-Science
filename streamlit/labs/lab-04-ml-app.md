# Streamlit Lab 4 — ML Prediction App

**Week:** Module C (Streamlit module) · **CLO-1, CLO-2, CLO-3** · **Time:**
~90 min

## Learning objectives

- Cache model training with `@st.cache_data` so the app never retrains on
  widget changes.
- Turn model inputs into sliders and predictions into readable output.
- Show honest evaluation (test accuracy) alongside the prediction.
- Add `st.session_state` for a prediction counter.

## Problem statement

Build **one app** (`app.py`) — a penguin species predictor:

1. Train a k-NN classifier (Module B) on the penguins dataset to predict
   `species` from bill length, bill depth, flipper length, and body mass.
2. Show test accuracy honestly (train/test split, seed 42).
3. Four sliders for the measurements → prediction + confidence.
4. A `st.session_state` counter of how many predictions the user has made.

## Tasks

1. Create `streamlit-lab4/app.py`.
2. **Prepare data once** (cached):
   ```python
   @st.cache_data
   def load_data():
       df = sns.load_dataset("penguins").dropna()
       return df
   ```
3. **Train once** (cached): split (test_size=0.3, random_state=42), fit
   `KNeighborsClassifier(n_neighbors=5)`.
4. **Features as sliders** — realistic ranges from the data:
   - bill length: 30–60 mm (default ~44)
   - bill depth: 13–22 mm (default ~17)
   - flipper length: 170–235 mm (default ~201)
   - body mass: 2700–6300 g (default ~4200)
5. **Predict** (cheap, every rerun): build a one-row DataFrame with the
   same column names, `model.predict` + `predict_proba`.
6. **Display**: `st.success(f"Predicted species: {species}")` +
   `st.metric("Confidence", f"{conf:.1%}")` + the full probability list.
7. **Counter**: increment `st.session_state.predictions` on each rerun
   where a prediction is shown (hint: any slider move counts as a new
   prediction — initialize in session state and increment once per rerun
   after the prediction block).

## Expected output (verify all)

- Accuracy caption with the true test accuracy (with seed 42 you should see
  a realistic value — report it).
- Default sliders predict the most common penguin species with high
  confidence (the defaults are dataset means).
- Changing one slider updates the prediction instantly and the counter goes
  up — and the app never hesitates (no retraining).
- The counter survives further interactions.

**Questions to answer in your submission:**

1. Why is it correct for the model to be cached but wrong for the
   prediction to be cached?
2. What would happen if the training function took the slider values as
   arguments? (Think about cache keys.)

## Challenge

Add a `st.selectbox` to switch the model between **k-NN** and
**LogisticRegression**, retraining only when the model choice changes
(hint: make the model name an argument of the cached training function —
now the cache key changes only when the model changes, not when sliders
move). Compare the two accuracies and explain which you would ship.