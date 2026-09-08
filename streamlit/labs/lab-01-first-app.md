# Streamlit Lab 1 — My First App with Widgets

**Week:** Module C (Streamlit module) · **CLO-1, CLO-3** · **Time:** ~60 min

## Learning objectives

- Run a Streamlit app from a `.py` script.
- Use `st.title`, `st.header`, `st.write`, `st.markdown`.
- Use `st.button`, `st.checkbox`, `st.selectbox`, `st.text_input`.
- Understand the rerun model and use `st.session_state` for a counter.

## Problem statement

Build **one app** (`app.py`) with two sections:

1. **About me** — title, a short markdown bio, and a text input that greets
   the user by name.
2. **Button lab** — a button that increments a counter, a checkbox that
   reveals/hides a secret message, and a selectbox that changes a welcome
   sentence ("Good morning/afternoon/evening").

## Tasks

1. Create `streamlit-lab1/app.py`.
2. **About me section:**
   - `st.title("My First App")`
   - `st.markdown` with one sentence about you (bold + italic somewhere).
   - `st.text_input("Your name?")` — greet only when a name is typed:
     `if name:` → `st.write(f"Hello, {name}!")`.
3. **Button lab section:**
   - A counter that survives reruns:
     ```python
     if "clicks" not in st.session_state:
         st.session_state.clicks = 0
     if st.button("Click me"):
         st.session_state.clicks += 1
     st.write(f"Clicks: {st.session_state.clicks}")
     ```
   - `st.checkbox("Show secret")` → reveal a hidden message when checked.
   - `st.selectbox("Time of day", ["morning", "afternoon", "evening"])` →
     show `f"Good {choice}!"`.
4. Run `streamlit run app.py`, verify every interaction, take a screenshot.
5. Answer the questions in §Expected output.

## Expected output (verify all)

- App opens at http://localhost:8501 with both sections visible.
- Typing a name shows a greeting immediately (no button needed).
- Clicking "Click me" 5 times shows `Clicks: 5` — and **stays** at 5 on
  further interactions (session state).
- Checking the checkbox shows the secret; unchecking hides it.
- Changing the selectbox changes the greeting.

**Questions to answer in your submission:**

1. What would happen to the counter if you used a normal variable
   (`clicks = 0` inside the script) instead of `st.session_state`?
2. Why does the greeting update as you type, without clicking anything?

## Challenge

Add a second counter that resets after 10 clicks: when the counter reaches
10, show `st.warning("Reached 10!")` and reset it to 0 automatically. (You
may also use `st.balloons()` when it resets.)