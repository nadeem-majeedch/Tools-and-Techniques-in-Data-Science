# Content for notebook 01: Python for Data Science.
CELLS = [
    ("md", """# 01 — Python for Data Science

**Course:** Introduction to Data Science (BS Data Science, 3rd semester)
**CLO:** CLO-1 — Apply Python and standard data science libraries to datasets.

This notebook refreshes the Python you need *before* touching NumPy and Pandas.
Everything here is used again — every single day — in the rest of the course.

---
"""),
    ("md", """## Learning objectives

By the end of this notebook you will be able to:

1. Explain why Python is the standard language for data science.
2. Use the core types: `int`, `float`, `str`, `bool`, `list`, `dict`.
3. Write `if`/`elif`/`else`, `for` loops, and functions.
4. Use list comprehensions instead of longer loops.
5. Read data from a text file safely.
6. Build a tiny "question → code → answer" data pipeline.

---
"""),
    ("md", """## Theory: why Python for data science?

Three reasons, in order of importance:

1. **Readability** — data analyses are read by humans (colleagues, reviewers,
   future-you). Python reads almost like English.
2. **Ecosystem** — NumPy, Pandas, Matplotlib, scikit-learn are the standard
   tools of the field, and they are all Python libraries.
3. **Free and open** — no licences, huge community, endless tutorials.

Before any library, though, you need the language itself. That is this notebook.

### The three ideas that matter most

- **A variable is a name for a value.** `price = 250` stores the number 250
  under the name `price`.
- **A type is the kind of a value.** `3` is an `int`, `3.5` is a `float`,
  `"hello"` is a `str`, `True` is a `bool`.
- **A collection holds many values.** A `list` is ordered and changeable;
  a `dict` maps keys to values (like a phone book).

Python is *dynamically typed*: you don't declare types, Python figures them
out. But Python is *strict at runtime*: `"5" + 3` fails, because a string and
a number cannot be added. Know the type you are working with.

---
"""),
    ("code", """# Setup: nothing to install for this notebook - pure Python.
# We print a sanity line so you can confirm the kernel works.
print("Notebook ready - Python", 3 + 4)
# Expected output: Notebook ready - Python 7
"""),
    ("md", """## Types: numbers, strings, booleans

Numbers, text, and truth values are the atoms of data. In data science you
will mostly *measure* things (numbers) and *describe* things (strings), and
you will use booleans to *filter* data (much more on that in the Pandas
notebook).

---
"""),
    ("code", """# --- Numbers ---
age = 20            # int: whole number
gpa = 3.6           # float: number with decimals
print(type(age), type(gpa))

total = age + 1     # arithmetic works as expected
print("Next year:", total)

# --- Strings ---
name = "Ayesha"
course = 'Data Science'     # single or double quotes both work
print(type(name), name.upper(), len(name))

# --- Booleans ---
is_enrolled = True
passed = gpa >= 3.0          # comparison produces a bool
print(is_enrolled, passed, type(passed))

# Expected output:
#   <class 'int'> <class 'float'>
#   Next year: 21
#   <class 'str'> AYESHA 6
#   True True <class 'bool'>
"""),
    ("md", """## Collections: lists and dicts

A **list** is an ordered collection — the order matters and you can change it.
A **dict** (dictionary) maps *keys* to *values*: fast lookup by name, like a
phone book or a row of a table with named columns.

Why do these matter for data science? A Pandas **Series** is a list with
labels; a Pandas **DataFrame** is conceptually a dict of named columns.
Learning lists and dicts now makes Pandas feel familiar later.

---
"""),
    ("code", """# --- Lists ---
scores = [88, 92, 76, 95]
print(scores[0])        # first element (index 0)
print(scores[-1])       # last element
print(scores[1:3])      # slice: indexes 1 and 2 (stop is excluded)
scores.append(81)       # add to the end
print(scores)

# --- Dicts ---
student = {"name": "Ayesha", "age": 20, "gpa": 3.6}
print(student["name"])       # look up by key
student["gpa"] = 3.7         # update a value
print(student)

# Expected output:
#   88
#   95
#   [92, 76]
#   [88, 92, 76, 95, 81]
#   Ayesha
#   {'name': 'Ayesha', 'age': 20, 'gpa': 3.7}
"""),
    ("md", """## Control flow: if, for, while

- `if` / `elif` / `else` lets your code *decide*.
- `for` lets your code *repeat* over a collection.
- `while` repeats while a condition is true — use it sparingly (easy to write
  an infinite loop).

The `range(n)` function produces the numbers 0, 1, ..., n-1 — the classic
way to loop a fixed number of times.

---
"""),
    ("code", """# --- if / elif / else ---
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
print("Grade:", grade)

# --- for over a list ---
prices = [250, 120, 390]
total = 0
for p in prices:
    total = total + p          # accumulate
print("Total:", total)

# --- for with range ---
for i in range(3):             # 0, 1, 2
    print("day", i + 1)

# Expected output:
#   Grade: B
#   Total: 760
#   day 1
#   day 2
#   day 3
"""),
    ("md", """## Functions: reusable logic

A **function** packages logic under a name so you can reuse it — and reuse is
the seed of reproducibility (the same function gives the same answer every
time you call it). A function takes *parameters* (inputs) and returns a
*result*.

---
"""),
    ("code", """def average(nums):
    \"\"\"Return the mean of a list of numbers.\"\"\"
    return sum(nums) / len(nums)

def is_passing(score, minimum=60):
    \"\"\"Return True if score meets the minimum (default 60).\"\"\"
    return score >= minimum

print(average([10, 20, 30]))
print(is_passing(75))
print(is_passing(55, minimum=70))

# Expected output:
#   20.0
#   True
#   False
"""),
    ("md", """## List comprehensions

A **list comprehension** builds a new list from an old one in one line. It is
the Pythonic way to "transform every element" or "keep only some elements".
Both patterns below are the daily bread of data work — filtering and
transforming columns.

---
"""),
    ("code", """scores = [88, 92, 76, 95, 54]

# Transform: square every score
squares = [s * s for s in scores]

# Filter: keep only scores >= 60 (the same idea as a boolean mask later)
passed = [s for s in scores if s >= 60]

print("Squares:", squares)
print("Passed:", passed)

# Comprehension with an expression: grade each score
labels = ["pass" if s >= 60 else "fail" for s in scores]
print(labels)

# Expected output:
#   Squares: [7744, 8464, 5776, 9025, 2916]
#   Passed: [88, 92, 76, 95]
#   ['pass', 'pass', 'pass', 'pass', 'fail']
"""),
    ("md", """## Reading files: where real data lives

Real data usually lives in files, not in code. The safest way to open a file
in Python is `with open(...) as f:` — the file is guaranteed to be closed,
even if an error happens. This is the last piece of pure Python you need
before the data libraries take over.

---
"""),
    ("code", """import os

# Make sure the folder exists before writing (in real life it already does)
os.makedirs("resources/example", exist_ok=True)

# Write a tiny data file (in real life this file already exists)
with open("resources/example/names.txt", "w") as f:
    f.write("Ali\\nSara\\nUsman\\nZara\\n")

# Read it back, one line at a time
with open("resources/example/names.txt") as f:
    lines = [line.strip() for line in f]     # strip removes the newline

print(lines)
print("Number of names:", len(lines))

# Expected output:
#   ['Ali', 'Sara', 'Usman', 'Zara']
#   Number of names: 4
"""),
    ("md", """## Beginner example: the smallest data pipeline

The shape of *all* data work is: **question → data → answer**. Here is the
smallest complete version. We ask a question ("what fraction of students
passed?"), we have data (a list of scores), and we compute an answer.

---
"""),
    ("code", """# Data: one list of exam scores
scores = [45, 72, 88, 51, 93, 67]

# Question: what fraction of students passed (score >= 60)?
passed = [s for s in scores if s >= 60]
fraction = len(passed) / len(scores)

print(f"{passed} -> {fraction:.0%} of students passed")

# Expected output:
#   [72, 88, 93, 67] -> 67% of students passed
"""),
    ("md", """## Intermediate example: a mini survey analysis

Now the same idea with dicts and functions — the tools working together, the
way they will in every later notebook.

---
"""),
    ("code", """# Data: survey responses (name -> hours of study per week)
survey = {
    "Ali": 4, "Sara": 6, "Usman": 2, "Zara": 7,
    "Fatima": 3, "Bilal": 5, "Hina": 8,
}

def stats(data):
    \"\"\"Return (average, max, count above average) for a dict of numbers.\"\"\"
    values = list(data.values())
    avg = sum(values) / len(values)
    above = [name for name, v in data.items() if v > avg]
    return round(avg, 2), max(values), above

avg, best, above = stats(survey)
print("Average study hours:", avg)
print("Most dedicated:", best, "hours")
print("Above average:", above)

# Expected output:
#   Average study hours: 5.0
#   Most dedicated: 8 hours
#   Above average: ['Sara', 'Zara', 'Hina']
"""),
    ("md", """## Exercises

Try each one **before** looking at the solution cell below it. The starter
cell runs (it contains only comments), so the notebook stays executable even
before you fill in your answer.

---
"""),
    ("md", """### Exercise 1 — Filter and transform

Given `temps = [31, 28, 35, 26, 33]`, build a new list with the temperatures
above 30, converted to Fahrenheit (`c * 9/5 + 32`)."""),
    ("code", """temps = [31, 28, 35, 26, 33]

# your code here
"""),
    ("code", """# Solution
hot_f = [c * 9 / 5 + 32 for c in temps if c > 30]
print(hot_f)
# Expected output: [87.8, 95.0, 91.4]
"""),
    ("md", """### Exercise 2 — Function

Write a function `count_words(text)` that returns the number of words in a
string (hint: `text.split()` splits on spaces)."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
def count_words(text):
    return len(text.split())

print(count_words("data science is fun"))
# Expected output: 4
"""),
    ("md", """### Exercise 3 — Loop and accumulate

Sum the even numbers from 1 to 20 (inclusive) using a `for` loop with
`range`. The answer is 110."""),
    ("code", """# your code here
"""),
    ("code", """# Solution
total = 0
for n in range(1, 21):
    if n % 2 == 0:
        total += n
print(total)
# Expected output: 110
"""),
    ("md", """## Challenge exercise

A store's sales are recorded as a list of dicts, one per day:

```python
sales = [
    {"day": "Mon", "amount": 3200},
    {"day": "Tue", "amount": 4100},
    {"day": "Wed", "amount": 2800},
    {"day": "Thu", "amount": 4500},
    {"day": "Fri", "amount": 5300},
]
```

Tasks:

1. Compute the total sales for the week.
2. Find the best day (highest amount).
3. Build a new list of dicts with an added key `"status"` that is `"good"`
   when the amount is above the week's average, else `"ok"`.

Combine everything in one script. A solution is below — try it first."""),
    ("code", """sales = [
    {"day": "Mon", "amount": 3200},
    {"day": "Tue", "amount": 4100},
    {"day": "Wed", "amount": 2800},
    {"day": "Thu", "amount": 4500},
    {"day": "Fri", "amount": 5300},
]

# your code here
"""),
    ("code", """# Solution
total = sum(d["amount"] for d in sales)
avg = total / len(sales)
best = max(sales, key=lambda d: d["amount"])["day"]

enriched = [
    {**d, "status": "good" if d["amount"] > avg else "ok"}
    for d in sales
]

print("Total:", total)
print("Best day:", best)
for d in enriched:
    print(d["day"], d["amount"], d["status"])

# Expected output:
#   Total: 19900
#   Best day: Fri
#   Mon 3200 ok
#   Tue 4100 good
#   Wed 2800 ok
#   Thu 4500 good
#   Fri 5300 good
"""),
    ("md", """## Recap

- Python has a small set of core ideas: **variables, types, collections,
  control flow, functions, comprehensions** — master these and the libraries
  become easy.
- A **list** is ordered and changeable; a **dict** maps keys to values.
- A **comprehension** is the Pythonic way to transform or filter a list.
- `with open(...) as f:` is the safe way to read files.
- Every data analysis has the same shape: **question → data → answer**.

---
"""),
    ("md", """## Questions

1. What is the difference between a `list` and a `dict`?
2. What does `scores[1:3]` return for `scores = [10, 20, 30, 40]`?
3. Rewrite this loop as a comprehension: `evens = []; for n in range(10): if n % 2 == 0: evens.append(n)`.
4. Why is `"5" + 3` an error in Python?
5. Write a function `tip_amount(bill, percent=15)` that returns the tip.
6. Why does `with open(...)` beat calling `open()` without `with`?

---
**Next:** notebook 02 — NumPy: fast numerical arrays.
"""),
]