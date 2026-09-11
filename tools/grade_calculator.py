"""Pure mark-calculation logic for the course grade calculator.

This module deliberately contains no Streamlit code so it can be unit-tested
and reused (e.g. in a notebook or a marking script).

CONFIRMED institutional scheme (total = 100 marks):

    Sessional  = 25 marks
    Mid Exam   = 35 marks
    Final Exam = 40 marks

Final Percentage = Sessional + Mid Exam + Final Exam

Because the maximum is exactly 100, no normalization is required: the total
out of 100 IS the percentage. The letter grade and grade points come from the
official scale in GRADE_SCALE below (and in assessment-plan.md).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    """One component of the confirmed institutional scheme."""

    key: str
    label: str
    max_marks: float  # raw marks available: 25, 35 or 40


# The confirmed institutional scheme, exactly as documented in
# assessment-plan.md. Totals are fixed: 25 + 35 + 40 = 100.
COMPONENTS: tuple[Component, ...] = (
    Component("sessional",  "Sessional",  25.0),
    Component("mid_exam",   "Mid Exam",   35.0),
    Component("final_exam", "Final Exam", 40.0),
)

TOTAL_MARKS = 100.0  # 25 + 35 + 40

# Official grading scale: (minimum percentage, letter, grade points, display range).
GRADE_SCALE: tuple[tuple[float, str, float, str], ...] = (
    (85.0, "A",  4.00, "85% and above"),
    (80.0, "A-", 3.70, "80–84%"),
    (75.0, "B+", 3.30, "75–79%"),
    (70.0, "B",  3.00, "70–74%"),
    (65.0, "B-", 2.70, "65–69%"),
    (61.0, "C+", 2.30, "61–64%"),
    (58.0, "C",  2.00, "58–60%"),   # 58–60 for C
    (55.0, "C-", 1.70, "55–57%"),
    (50.0, "D",  1.00, "50–54%"),
    (0.0,  "F",  0.00, "below 50%"),
)


class ValidationError(ValueError):
    """Raised when an input mark is impossible (negative, above max, non-numeric)."""


def calculate(marks: dict[str, float | None]) -> dict:
    """Compute the total, percentage, letter grade and grade points.

    marks maps component key -> raw marks obtained. Components may be omitted
    (treated as not yet assessed) or given as None.

    Returns a dict with per-component rows, the total out of 100, the
    percentage, letter, grade points and the best score still reachable.
    Raises ValidationError for impossible marks.
    """
    rows = []
    for comp in COMPONENTS:
        raw = marks.get(comp.key)
        if raw is None:
            rows.append({
                "key": comp.key, "label": comp.label,
                "raw": None, "max": comp.max_marks,
                "assessed": False,
            })
            continue
        raw = _validate(comp, raw)
        rows.append({
            "key": comp.key, "label": comp.label,
            "raw": raw, "max": comp.max_marks,
            "assessed": True,
        })

    total = sum(r["raw"] for r in rows if r["assessed"])
    max_possible = total + sum(
        r["max"] for r in rows if not r["assessed"]
    )
    letter, points = letter_grade(total)
    return {
        "rows": rows,
        "total": total,                # out of 100
        "percentage": total,           # max is exactly 100 → no normalization
        "letter": letter,
        "points": points,
        "max_possible": max_possible,  # best still reachable with remaining components
    }


def letter_grade(score: float) -> tuple[str, float]:
    """Return (letter, grade points) for a score out of 100, per the official scale."""
    for floor, letter, points, _range in GRADE_SCALE:
        if score >= floor:
            return letter, points
    return "F", 0.00


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


def _self_test() -> None:
    """Verify arithmetic, the official scale and validation; run directly."""
    # Example 1 (from assessment-plan.md): 20 + 28 + 33 = 81 → A- · 3.70
    res = calculate({"sessional": 20.0, "mid_exam": 28.0, "final_exam": 33.0})
    assert res["total"] == 81.0, res["total"]
    assert res["percentage"] == 81.0
    assert res["letter"] == "A-", res["letter"]
    assert res["points"] == 3.70, res["points"]
    assert res["max_possible"] == 81.0  # nothing unassessed → best reachable = 81

    # Example 2: perfect record 100/100 → A · 4.00
    perfect = calculate({"sessional": 25.0, "mid_exam": 35.0, "final_exam": 40.0})
    assert perfect["total"] == 100.0
    assert perfect["letter"] == "A", perfect["letter"]
    assert perfect["points"] == 4.00, perfect["points"]

    # Official scale boundaries (score → letter · points).
    for score, want_letter, want_points in [
        (85.0, "A", 4.00), (84.99, "A-", 3.70),
        (80.0, "A-", 3.70), (79.99, "B+", 3.30),
        (75.0, "B+", 3.30), (70.0, "B", 3.00),
        (65.0, "B-", 2.70), (64.99, "C+", 2.30),
        (61.0, "C+", 2.30), (60.0, "C", 2.00), (58.0, "C", 2.00),
        (57.99, "C-", 1.70), (55.0, "C-", 1.70),
        (54.99, "D", 1.00), (50.0, "D", 1.00),
        (49.99, "F", 0.00), (0.0, "F", 0.00),
    ]:
        letter, points = letter_grade(score)
        assert (letter, points) == (want_letter, want_points), \
            f"{score}: got {letter} · {points}, want {want_letter} · {want_points}"

    # Partial record: only Sessional assessed so far.
    partial = calculate({"sessional": 20.0})
    assert partial["total"] == 20.0
    # 5 sessional marks are gone forever → best reachable is 95, not 100.
    assert partial["max_possible"] == 95.0, partial["max_possible"]

    # Validation: impossible marks must raise.
    for bad in ({"sessional": 26}, {"mid_exam": -1}, {"final_exam": 41},
                {"sessional": "twenty"}):
        try:
            calculate(bad)
        except ValidationError:
            pass
        else:
            raise AssertionError(f"expected ValidationError for {bad}")

    # The display ranges must match the official notifications exactly.
    assert GRADE_SCALE[6][3] == "58–60%", GRADE_SCALE[6][3]
    assert GRADE_SCALE[1][3] == "80–84%"
    assert GRADE_SCALE[-1][3] == "below 50%"

    print("grade calculator self-test passed")


if __name__ == "__main__":
    _self_test()
