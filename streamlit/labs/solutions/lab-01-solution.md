# Lab 1 — Solution: My First App with Widgets

## Complete app.py

```python
import streamlit as st

st.title("My First App")

# ---------- Section 1: About me ----------
st.header("About me")
st.markdown("I am a **Data Science** student who *loves* pandas and charts.")

name = st.text_input("Your name?")
if name:
    st.write(f"Hello, {name}!")
else:
    st.info("Type your name above to get a greeting.")

# ---------- Section 2: Button lab ----------
st.header("Button lab")

# Counter that survives reruns (session state)
if "clicks" not in st.session_state:
    st.session_state.clicks = 0

if st.button("Click me"):
    st.session_state.clicks += 1
st.write(f"Clicks: {st.session_state.clicks}")

# Checkbox reveals/hides a message
if st.checkbox("Show secret"):
    st.success("The secret: the script re-runs on every interaction!")

# Selectbox changes the greeting
time_of_day = st.selectbox("Time of day", ["morning", "afternoon", "evening"])
st.write(f"Good {time_of_day}!")
```

## Expected numbers

- Counter increments and **persists** across other interactions
  (typing in the name box does not reset it) — that is session state.
- Checkbox toggles the message on/off; selectbox swaps the greeting.

## Model answers to the questions

1. **What happens with a normal variable instead of session_state?**
   The script re-runs from the top on every interaction, so `clicks = 0`
   would reset before the button's `if` runs — the counter would always
   show 1 after a click and 0 otherwise. `st.session_state` is the only
   place a value survives a rerun.
2. **Why does the greeting update while typing?** Because every keystroke
   triggers a rerun: the script re-executes, `name` holds the new string,
   and `st.write` re-renders. There is no "submit" needed — continuous
   interactivity is Streamlit's default.

## Challenge solution (auto-reset at 10)

```python
if "clicks" not in st.session_state:
    st.session_state.clicks = 0

if st.button("Click me"):
    st.session_state.clicks += 1
    if st.session_state.clicks >= 10:
        st.balloons()
        st.warning("Reached 10! Resetting.")
        st.session_state.clicks = 0

st.write(f"Clicks: {st.session_state.clicks}")
```