"""Streamlit front end for the course grade calculator (25 / 35 / 40 scheme).

Run it with:

    streamlit run tools/grade_app.py

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
    BUCKET_WEIGHTS,
    COMPONENTS,
    ValidationError,
    calculate,
)

st.set_page_config(page_title="Grade Calculator — 25/35/40", page_icon="🎓")

st.title("🎓 Grade Calculator")
st.caption(
    "Institutional scheme — Continuous 25% (Labs 10 · Quizzes 5 · Assignments 10) "
    "· Midterm 35% · Final 40% (Final exam 25 · Final project 15). "
    "Leave a component empty if it has not been assessed yet."
)

st.divider()

# ---------------------------------------------------------------- input form
with st.form("marks"):
    cols = st.columns(3)
    inputs: dict[str, float | None] = {}
    for i, comp in enumerate(COMPONENTS):
        with cols[i % 3]:
            inputs[comp.key] = st.number_input(
                f"{comp.label} — weight {comp.weight:g}%",
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
    example = {"labs": 8.0, "quizzes": 4.0, "assignments": 8.5,
               "midterm": 28.0, "final_exam": 20.0, "project": 12.5}
    st.markdown("**Worked example** — raw marks used below:")
    inputs = {k: example.get(k) for k in inputs}

# Validate + compute (user inputs after submit, example otherwise).
try:
    result = calculate({k: v for k, v in inputs.items() if v is not None})
except ValidationError as err:
    st.error(f"Impossible marks: {err}")
    st.stop()

# ---------------------------------------------------------------- breakdown
st.subheader("Component breakdown")

table = [
    {
        "Component": r["label"],
        "Bucket": r["bucket"],
        "Raw marks": "—" if r["raw"] is None else f"{r['raw']:g} / {r['max']:g}",
        "Weight": f"{r['weight']:g}%",
        "Weighted contribution": "—" if r["weighted"] is None else f"{r['weighted']:.2f}",
    }
    for r in result["rows"]
]
st.dataframe(table, width="stretch", hide_index=True)

st.caption("Weighted contribution = (your marks ÷ maximum marks) × component weight.")

# ---------------------------------------------------------------- buckets
st.subheader("Buckets (25 / 35 / 40)")
bcols = st.columns(3)
for col, (bucket, info) in zip(bcols, BUCKET_WEIGHTS.items()):
    b = result["buckets"][bucket]
    if b["assessed_weight"]:
        col.metric(
            bucket,
            f"{b['earned']:.2f} / {b['weight']:g}",
            f"{b['percent']:.1f}% of bucket so far",
        )
    else:
        col.metric(bucket, f"0 / {b['weight']:g}", "not yet assessed")

# ---------------------------------------------------------------- final score
st.divider()
score = result["final_score"]
c1, c2, c3 = st.columns(3)
c1.metric("Final score (out of 100)", f"{score:.2f}")
c2.metric("Letter grade (indicative)", result["letter"])
c3.metric("Best still reachable", f"{result['max_possible']:.1f}")

st.progress(min(score / 100.0, 1.0))

st.caption(
    "Letter grade is indicative only — your university's official scale and "
    "rounding policy always take precedence. See `assessment-plan.md` for the "
    "full formula."
)
