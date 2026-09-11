"""Pure mark-calculation logic for the course grade calculator.

This module deliberately contains no Streamlit code so it can be unit-tested
and reused (e.g. in a notebook or a marking script).

Institutional scheme (25 : 35 : 40):

    Continuous Assessment = 25%  (Labs 10 + Quizzes 5 + Assignments 10)
    Midterm               = 35%
    Final                 = 40%  (Final exam 25 + Final project 15)

Final score = sum of every component's weighted contribution, where

    weighted contribution = (your marks / max marks) * component weight
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    """One assessable component of the course."""

    key: str
    label: str
    weight: float          # percentage of the final grade, e.g. 10.0
    max_marks: float       # raw marks available, e.g. 30
    bucket: str            # "Continuous", "Midterm" or "Final"


# The institutional scheme, exactly as documented in assessment-plan.md.
# Bucket totals are fixed: Continuous 25, Midterm 35, Final 40.
COMPONENTS: tuple[Component, ...] = (
    Component("labs",       "Labs (32)",        10.0, 10.0, "Continuous"),
    Component("quizzes",    "Quizzes (2)",       5.0,  5.0, "Continuous"),
    Component("assignments","Assignments (2)",  10.0, 10.0, "Continuous"),
    Component("midterm",    "Midterm exam",     35.0, 35.0, "Midterm"),
    Component("final_exam", "Final exam",       25.0, 25.0, "Final"),
    Component("project",    "Final project",    15.0, 15.0, "Final"),
)

BUCKET_WEIGHTS = {"Continuous": 25.0, "Midterm": 35.0, "Final": 40.0}


class ValidationError(ValueError):
    """Raised when an input mark is impossible (negative, above max, non-numeric)."""


def calculate(marks: dict[str, float]) -> dict:
    """Compute weighted contributions from raw marks.

    marks maps component key -> raw marks obtained. Components may be omitted
    (treated as not yet assessed) or given as None.

    Returns a dict with per-component rows, bucket subtotals and the final
    score out of 100. Raises ValidationError for impossible marks.
    """
    rows = []
    for comp in COMPONENTS:
        raw = marks.get(comp.key)
        if raw is None:
            rows.append({
                "key": comp.key, "label": comp.label, "bucket": comp.bucket,
                "raw": None, "max": comp.max_marks, "weight": comp.weight,
                "weighted": None, "assessed": False,
            })
            continue
        raw = _validate(comp, raw)
        rows.append({
            "key": comp.key, "label": comp.label, "bucket": comp.bucket,
            "raw": raw, "max": comp.max_marks, "weight": comp.weight,
            "weighted": raw / comp.max_marks * comp.weight, "assessed": True,
        })

    buckets = {}
    for bucket, total_weight in BUCKET_WEIGHTS.items():
        earned = sum(r["weighted"] for r in rows if r["bucket"] == bucket and r["assessed"])
        assessed_weight = sum(r["weight"] for r in rows if r["bucket"] == bucket and r["assessed"])
        buckets[bucket] = {
            "weight": total_weight,
            "earned": earned,
            "assessed_weight": assessed_weight,
            # Share of the bucket achieved so far (None if nothing assessed yet).
            "percent": (earned / assessed_weight * 100.0) if assessed_weight else None,
        }

    final_score = sum(r["weighted"] for r in rows if r["assessed"])
    max_possible = final_score + sum(
        r["weight"] for r in rows if not r["assessed"]
    )
    return {
        "rows": rows,
        "buckets": buckets,
        "final_score": final_score,          # out of 100
        "max_possible": max_possible,        # what a perfect remaining record could reach
        "letter": letter_grade(final_score),
    }


def _validate(comp: Component, raw: float) -> float:
    """Reject impossible marks with a clear, student-friendly message."""
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        raise ValidationError(f"{comp.label}: enter a number (got {raw!r}).")
    raw = float(raw)
    if raw < 0:
        raise ValidationError(f"{comp.label}: marks cannot be negative (got {raw:g}).")
    if raw > comp.max_marks:
        raise ValidationError(
            f"{comp.label}: maximum is {comp.max_marks:g} (got {raw:g})."
        )
    return raw


def letter_grade(score: float) -> str:
    """Common Pakistani-university letter scale. Adjust to your program's policy."""
    thresholds = [(85, "A"), (80, "A-"), (75, "B+"), (70, "B"),
                  (65, "B-"), (61, "C+"), (58, "C"), (55, "C-"),
                  (50, "D"), (0, "F")]
    for floor, letter in thresholds:
        if score >= floor:
            return letter
    return "F"


def _self_test() -> None:
    """Verify the arithmetic and validation; runs with `python tools/grade_calculator.py`."""
    # Example from assessment-plan.md: a consistent full record.
    example = {
        "labs": 8.0, "quizzes": 4.0, "assignments": 8.5,
        "midterm": 28.0, "final_exam": 20.0, "project": 12.5,
    }
    res = calculate(example)
    expected = (8.0 + 4.0 + 8.5) + 28.0 + 20.0 + 12.5  # weights == max marks here
    assert abs(res["final_score"] - expected) < 1e-9, res["final_score"]
    assert res["letter"] == "A-", res["letter"]  # 81 points -> A- on this scale

    # Partial record: only some components assessed.
    partial = calculate({"labs": 9.0, "midterm": 30.0})
    assert abs(partial["final_score"] - (9.0 + 30.0)) < 1e-9
    # 1 lab mark and 5 midterm marks are gone forever, so the best reachable
    # score is 100 - 1 - 5 = 94.
    assert abs(partial["max_possible"] - 94.0) < 1e-9, partial["max_possible"]
    assert partial["buckets"]["Continuous"]["percent"] == 90.0

    # Validation: impossible marks must raise.
    for bad in ({"labs": -1}, {"midterm": 36}, {"project": 99}):
        try:
            calculate(bad)
        except ValidationError:
            pass
        else:
            raise AssertionError(f"expected ValidationError for {bad}")

    print("grade calculator self-test passed")


if __name__ == "__main__":
    _self_test()
