"""Streamlit front end for the course grade calculator.

Run it with:

    streamlit run tools/grade_app.py

CONFIRMED institutional scheme (total = 100 marks):

    Sessional = 25 · Mid Exam = 35 · Final Exam = 40

Final Percentage = Sessional + Mid Exam + Final Exam (the maximum is exactly
100, so no normalization is needed). The letter grade and grade points come
from the official scale documented in assessment-plan.md.

The arithmetic lives in tools/grade_calculator.py (pure Python, self-tested);
this file only handles input widgets and presentation — the same logic/UI
split the course teaches in the Streamlit module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Allow running both as `streamlit run tools/grade_app.py` and as a plain script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from grade_calculator import (  # noqa: E402
    COMPONENTS,
    GRADE_SCALE,
    ValidationError,
    calculate,
)

st.set_page_config(page_title="Grade Calculator — Sessional/Mid/Final", page_icon="🎓")

st.title("🎓 Grade Calculator")
st.caption(
    "Confirmed institutional scheme — **Sessional 25 marks · Mid Exam 35 marks · "
    "Final Exam 40 marks** (total 100). Final Percentage = Sessional + Mid + Final. "
    "Leave a component empty if it has not been assessed yet."
)

st.divider()

# ---------------------------------------------------------------- input form
with st.form("marks"):
    cols = st.columns(3)
    inputs: dict[str, float | None] = {}
    for i, comp in enumerate(COMPONENTS):
        with cols[i]:
            inputs[comp.key] = st.number_input(
                f"{comp.label} (out of {comp.max_marks:g})",
                min_value=0.0,
                max_value=comp.max_marks,
                value=None,                      # empty = not yet assessed
                step=0.5,
                format="%.2f",
                key=comp.key,
                help=f"Raw marks out of {comp.max_marks:g}.",
            )
    submitted = st.form_submit_button("Calculate", type="primary", width="stretch")

# The form starts empty; until the student submits, show the worked example
# from the assessment plan so the app demonstrates itself.
if not submitted:
    st.info(
        "Tip: press **Calculate** with your own marks — the numbers below are the "
        "worked example from the assessment plan."
    )
    example = {"sessional": 20.0, "mid_exam": 28.0, "final_exam": 33.0}
    st.markdown("**Worked example** — 20/25 + 28/35 + 33/40:")
    inputs = {k: example.get(k) for k in inputs}

# Validate + compute (user inputs after submit, example otherwise).
try:
    result = calculate({k: v for k, v in inputs.items() if v is not None})
except ValidationError as err:
    st.error(f"Impossible marks: {err}")
    st.stop()

# ---------------------------------------------------------------- breakdown
st.subheader("Marks breakdown")

table = [
    {
        "Component": r["label"],
        "Max marks": f"{r['max']:g}",
        "Your marks": "—" if r["raw"] is None else f"{r['raw']:g}",
        "Status": "not yet assessed" if r["raw"] is None else "assessed",
    }
    for r in result["rows"]
]
st.dataframe(table, width="stretch", hide_index=True)

st.caption("Final Percentage = Sessional + Mid Exam + Final Exam (max = 100, so the total is the percentage).")

# ---------------------------------------------------------------- result
st.divider()
score = result["total"]
c1, c2, c3 = st.columns(3)
c1.metric("Total (out of 100)", f"{score:g}")
c2.metric("Letter grade", result["letter"])
c3.metric("Grade points", f"{result['points']:.2f}")

if score < result["max_possible"]:
    st.info(f"Assessed so far: **{score:g}** of the {result['max_possible']:g} marks "
            f"still reachable — best possible final total is **{result['max_possible']:g}/100**.")

st.progress(min(score / 100.0, 1.0))

# ---------------------------------------------------------------- scale
with st.expander("Official grading scale"):
    st.dataframe(
        [
            {"Grade": letter, "Percentage": pct_range, "Grade points": f"{points:.2f}"}
            for _floor, letter, points, pct_range in GRADE_SCALE
        ],
        width="stretch",
        hide_index=True,
    )
    st.caption("Your university's official notifications always take precedence over this calculator.")
