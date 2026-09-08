"""Generate the dirty dataset used by Assignment 1 (data cleaning + EDA).

Writes assignments/assignment-01-data-cleaning-eda/student-records-dirty.csv.

The dataset is intentionally messy — missing values, duplicates, inconsistent
text, stringy numbers, mixed date formats, and outliers — and deterministic:
run with any Python 3.x and you get the same 200 rows.

Usage:
    python scripts/make_assignment1_dataset.py
"""
import csv
import random
from pathlib import Path

random.seed(2026)

OUT = (Path(__file__).resolve().parent.parent
       / "assignments" / "assignment-01-data-cleaning-eda"
       / "student-records-dirty.csv")

FIRST = ["Ali", "Ayesha", "Bilal", "Daniyal", "Emaan", "Faraz", "Hina",
         "Iqra", "Junaid", "Kiran", "Laila", "Mubashir", "Nimra", "Omer",
         "Parveen", "Qasim", "Rania", "Sana", "Tariq", "Uzma", "Waqar",
         "Zainab", "Hamza", "Maryam", "Usman", "Fatima", "Ahmed", "Sara"]
LAST = ["Khan", "Ahmed", "Hussain", "Malik", "Shah", "Ali", "Raza", "Qureshi",
        "Siddiqui", "Butt", "Chaudhry", "Baig", "Ansari", "Javed", "Sheikh"]

# Normal distribution helpers
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

rows = []
used_ids = set()
used_emails = set()
n = 200

for i in range(n):
    sid = f"S{i + 1:03d}"
    # ~4% of IDs get duplicated (same student appears twice with variations)
    if i > 0 and random.random() < 0.04:
        sid = f"S{random.choice(list(used_ids))}"

    name = f"{random.choice(FIRST)} {random.choice(LAST)}"
    gender_r = random.random()
    gender = "M" if gender_r < 0.47 else ("F" if gender_r < 0.94 else "m ")
    program_r = random.random()
    program = ("DS" if program_r < 0.35 else
               ("AI" if program_r < 0.65 else "CS"))
    if random.random() < 0.06:          # inconsistent text
        program = {"DS": "ds", "AI": " Artificial Intelligence",
                   "CS": "CS "}[program]
    semester = random.choice(["Fall 2023", "Spring 2024", "Fall 2024"])
    if random.random() < 0.05:
        semester = random.choice(["fall2023", "Spring 2024 ", "Fall-2024"])

    gpa = clamp(round(random.gauss(3.0, 0.6), 2), 1.2, 4.0)
    if random.random() < 0.07:
        gpa = ""                        # missing
    elif random.random() < 0.03:
        gpa = 4.9                       # impossible outlier

    attendance = clamp(round(random.gauss(82, 10)), 40, 100)
    if random.random() < 0.08:
        attendance = ""                 # missing
    elif random.random() < 0.02:
        attendance = random.choice([125, -3])   # impossible values

    # emails: base + sometimes duplicate (same base, different case/spacing)
    base = f"{name.split()[0].lower()}.{name.split()[1].lower()}"
    email = f"{base}@student.example.edu"
    if random.random() < 0.08:
        email = email.title().replace(" ", "")   # "Ali.Khan@Student..."
    if random.random() < 0.05:
        email = ""                       # missing

    date_r = random.random()
    if date_r < 0.5:
        enrolled = f"2023-09-0{random.randint(1, 9)}"
    elif date_r < 0.75:
        enrolled = f"0{random.randint(1, 9)}/09/2023"
    else:
        enrolled = f"Sept {random.randint(1, 9)}, 2023"

    hours = clamp(round(random.gauss(18, 8)), 1, 40)
    if random.random() < 0.06:
        hours = ""                       # missing
    elif random.random() < 0.02:
        hours = 99                       # outlier

    rows.append([sid, name, gender, program, semester, gpa, attendance,
                 email, enrolled, hours])
    used_ids.add(sid)

# sprinkle exact duplicate rows (complete copies)
for _ in range(4):
    rows.append(list(random.choice(rows)))

# header + sort by student_id for a natural look
rows.sort(key=lambda r: r[0])
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["student_id", "name", "gender", "program", "semester",
                     "gpa", "attendance_pct", "email", "enrolled_date",
                     "study_hours"])
    writer.writerows(rows)

print(f"wrote {OUT}")
print(f"rows: {len(rows)} (200 base + 4 exact duplicates)")