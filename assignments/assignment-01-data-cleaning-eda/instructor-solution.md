# Assignment 1 — Instructor Solution

**CLO-1** · Complete cleaning + EDA solution for
`student-records-dirty.csv`. All numbers below are verified against the
generated dataset (`python scripts/make_assignment1_dataset.py`, seed 2026).

Also provided: `instructor-clean.csv` (the cleaned output of this exact
pipeline) — useful for spot-checking student `data/student-records-clean.csv`.

---

## 1. Quality audit (answers)

- `shape: (204, 10)` — 200 base rows + 4 exact duplicates.
- Missing values: `gpa` 10, `attendance_pct` 13, `email` 8, `study_hours`
  12 (name/id/date: 0). Note: empty cells arrive as `NaN` via `read_csv`.
- Complete duplicates: **4**. Near-duplicates: `email` 46 (case/whitespace
  variants + name collisions from duplicated IDs), `student_id` 5.
- Wrong dtypes: `gpa`, `attendance_pct`, `study_hours` are `object`
  (stringy numbers, e.g. `"4.9"`, `""`); `enrolled_date` is `object`
  (mixed `2023-09-01`, `05/09/2023`, `Sept 9, 2023`).
- Impossible values: `gpa` > 4 → 4 rows (max 4.9); `attendance_pct`
  outside [0, 100] → 2 rows (125, −3); `study_hours` > 60 → 3 rows (99).

## 2. Cleaning code (canonical pipeline)

```python
import pandas as pd

df = pd.read_csv("student-records-dirty.csv")

# --- text normalization (strip FIRST, then map canonical values) ---
df["gender"] = df["gender"].str.strip().str.upper().replace({"FEMALE": "F", "MALE": "M"})
df["program"] = (df["program"].str.strip()
                 .replace({"ds": "DS", "Data Science": "DS",
                           "Artificial Intelligence": "AI"}))
df["semester"] = (df["semester"].str.strip()
                  .replace({"fall2023": "Fall 2023", "Fall-2024": "Fall 2024"}))
df["email"] = df["email"].str.strip().str.lower()

# --- dtypes (coerce, don't crash) ---
df["gpa"] = pd.to_numeric(df["gpa"], errors="coerce")
df["attendance_pct"] = pd.to_numeric(df["attendance_pct"], errors="coerce")
df["study_hours"] = pd.to_numeric(df["study_hours"], errors="coerce")

# --- impossible values: flag -> NaN -> impute (measurement errors) ---
df["gpa"] = df["gpa"].where(df["gpa"] <= 4.0)
df["attendance_pct"] = df["attendance_pct"].where(df["attendance_pct"].between(0, 100))
df["study_hours"] = df["study_hours"].where(df["study_hours"] <= 60)

# --- missing values: fill numeric with mean (light, random missingness) ---
for col, mean in [("gpa", df["gpa"].mean()),
                  ("attendance_pct", df["attendance_pct"].mean()),
                  ("study_hours", df["study_hours"].mean())]:
    df[col] = df[col].fillna(round(mean, 2))

# --- duplicates: complete, then email, then student_id (keep first) ---
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["email"], keep="first")
df = df.drop_duplicates(subset=["student_id"], keep="first")

# --- unidentifiable row: drop (NaN email after dedupe) ---
df = df.dropna(subset=["email"])

# --- dates ---
df["enrolled_date"] = pd.to_datetime(df["enrolled_date"], format="mixed", errors="coerce")
df["enroll_year"] = df["enrolled_date"].dt.year
df = df.dropna(subset=["enrolled_date"])

df.to_csv("data/student-records-clean.csv", index=False)
print(df.shape, df.isna().sum().sum())      # (149, 11)  0
```

## 3. Cleaning log (deliverable model answer)

| Action | Column(s) | Rows affected | Reason |
|---|---|---|---|
| strip + case-normalize | gender | all | one canonical code (M/F) |
| strip + map variants | program | 7 | "ds", " Data Science", " Artificial Intelligence" → DS/DS/AI |
| strip + map variants | semester | ~10 | "fall2023", "Fall-2024" → canonical labels |
| coerce to numeric | gpa, attendance_pct, study_hours | all | fix stringy numbers |
| flag + impute (mean) | gpa > 4 | 4 | impossible values are measurement errors; mean imputation is transparent |
| flag + impute (mean) | attendance outside 0–100 | 2 | same reasoning |
| flag + impute (mean) | study_hours > 60 | 3 | 99 is a typo; winsorize-by-imputation |
| fill missing with mean | gpa/attendance/study_hours | 10/13/12 | light, plausibly-random missingness; keeping rows > losing them |
| drop complete duplicates | all | 4 | exact copies carry no information |
| dedupe on email, keep first | email | 46 → kept 1 | near-duplicate submissions (case variants, name collisions) |
| dedupe on student_id, keep first | student_id | 5 | same student entered twice |
| drop unidentifiable | email (NaN) | 1 | cannot verify identity — safer to exclude |
| parse mixed dates | enrolled_date | all | unify formats; extract enroll_year |

Final: **204 → 149 rows, 11 columns, 0 missing values.**

## 4. EDA (code + expected output)

```python
import seaborn as sns
import matplotlib.pyplot as plt

print(df.groupby("program")["gpa"].mean().round(2))
# AI 2.97  CS 3.05  DS 2.93
print(df.groupby("semester")["attendance_pct"].mean().round(1))
# Fall 2023 85.0  Fall 2024 81.4  Spring 2024 81.5
print(df.groupby("program")["study_hours"].mean().round(1))
# AI 20.0  CS 17.8  DS 18.3

sns.heatmap(df[["gpa", "attendance_pct", "study_hours"]].corr(),
            annot=True, cmap="coolwarm")
sns.scatterplot(data=df, x="study_hours", y="gpa")
sns.boxplot(data=df, x="program", y="gpa")
sns.histplot(df["gpa"], bins=20)
```

Key numbers: `study_hours`–`gpa` correlation **−0.113**; `attendance`–`gpa`
**−0.092**; GPA distribution roughly normal around 3.0.

## 5. Model findings (claim → evidence → plot)

1. **CS students have the highest mean GPA.** Mean GPA 3.05 (CS) vs 2.97
   (AI) and 2.93 (DS) — program boxplot, Fig. 2.
2. **Attendance has drifted down across semesters.** Mean attendance 85.0%
   (Fall 2023) → 81.5% (Spring 2024) → 81.4% (Fall 2024) — bar table in
   Part C.
3. **Study hours barely correlate with GPA.** r = −0.113 — the scatter
   shows a flat cloud; hours alone explain ~1% of GPA variance.

Limitations paragraph (model answer): the cleaned file reflects our
imputation choices (means fill ~35 cells, which shrinks variance slightly);
missingness may not be random (registrar exports often drop rows for
inactive students); email-based dedupe assumes emails are unique
identifiers; enrollment dates were simplified to a year, hiding
intra-year patterns.

## 6. Rubric application notes

| Criterion | Max | What "full marks" looks like |
|---|---|---|
| Quality audit | 15 | missing table with %, dup counts per key, dtype table |
| Justified cleaning | 20 | log entry per decision with a *reason*, not just the command |
| Correctness | 15 | clean file round-trips (149 × 11), dtypes verified, 0 missing |
| EDA depth | 15 | univariate + groupby + heatmap + at least one scatter |
| Visualizations | 15 | 3+ labeled, titled, captioned figures |
| Findings | 10 | 3 findings each with an exact number + plot reference |
| Log + limitations | 10 | every step logged; limitations paragraph present |

Common deductions: students who fill everything with the mean without
justifying it (no log), who drop 54 rows silently (data loss without
explanation), who never check dtypes after `to_csv`/`read_csv`, or whose
notebook has unexecuted cells.

## 7. Common student pitfalls to watch for

- `str.replace` on the *pre-strip* string (misses `" Artificial
  Intelligence"`).
- Dedupe order: deduping on `email` before normalizing case/whitespace
  leaves variants behind.
- Forgetting that empty CSV cells arrive as `NaN` (so `isna()` counts
  them, `""` checks don't).
- Using `fillna(mean)` without logging the rows affected.
- Reporting `204 → 149` as "data loss" — the log explains it; silence is
  the problem, not the drop.