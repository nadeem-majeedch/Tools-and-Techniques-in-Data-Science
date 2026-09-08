# Lab 02 — Python Refresher

**Session:** Week 1 · Session 2 · 90 min
**CLO:** CLO-1
**Difficulty:** Beginner

## Learning objectives

By the end of this lab you can:

1. Work fluently with lists, dicts, tuples, and sets.
2. Write `for` loops, conditionals, and list comprehensions.
3. Define and call functions with default arguments.
4. Read a small data file and do simple summary math in pure Python.

## Problem statement

You receive sales records as a plain-text file (one row per line,
`product,units,price`). Before anyone introduces pandas, the team wants a
**pure-Python** script that reads the file, computes totals per product, and
prints a clean report — so the logic is fully understood by hand.

## Dataset requirements

Create `sales.txt` yourself with the starter code below (or type it by
hand). It is a small, hand-made dataset — 8 rows.

## Step-by-step tasks

1. Write a function `parse_line(line)` that turns
   `"coffee,3,2.50"` into `("coffee", 3, 2.5)` — a tuple.
2. Write a function `read_sales(path)` that reads the file, skips the
   header line, and returns a list of parsed tuples. Handle a blank line
   gracefully.
3. Write `totals_by_product(rows)` returning a dict
   `product -> total revenue` (units × price).
4. Write `print_report(totals)` that prints one line per product sorted by
   revenue (highest first) plus a grand total line.
5. Use a list comprehension somewhere in steps 1–4 and comment it.
6. Run the full script; compare your output with the expected output.

## Starter code

```python
# sales.py
def parse_line(line):
    """'coffee,3,2.50' -> ('coffee', 3, 2.5). Return None for blank lines."""
    line = line.strip()
    if not line:
        return None
    # your code here: split on ',', convert types, return a tuple


def read_sales(path):
    rows = []
    with open(path) as f:
        next(f)                     # skip header
        for line in f:
            row = parse_line(line)
            if row is not None:
                rows.append(row)
    return rows


def totals_by_product(rows):
    totals = {}
    for product, units, price in rows:
        # your code here: accumulate units * price per product
        pass
    return totals


def print_report(totals):
    # your code here: sort by revenue descending, print, grand total
    pass


if __name__ == "__main__":
    rows = read_sales("sales.txt")
    totals = totals_by_product(rows)
    print_report(totals)
```

```text
# sales.txt (create this file)
product,units,price
coffee,3,2.50
tea,5,1.20
coffee,2,2.50
cake,1,4.00
tea,2,1.20
juice,4,3.00
cake,2,4.00
coffee,1,2.50
```

## Expected output

```
cake         12.00
juice        12.00
coffee       15.00
tea           8.40
grand total  47.40
```

(Sorting order: your choice between alphabetical and by revenue — say which
you used in a comment.)

## Questions

1. What type does `parse_line` return, and why is a tuple a good fit?
2. Why do we skip the first line of the file?
3. What does `units * price` produce if `units` is a string? Why must you
   convert types?
4. Rewrite `totals_by_product` with `defaultdict` — how does it change the
   code?
5. A customer buys `tea,0,1.20` — what should the report show?

## Challenge task

Extend the report with a `max_product(totals)` function that returns the
best-selling product **by units** (not revenue). Print it as
`best by units: coffee`. Then add a `--sort alpha` command-line flag
(`sys.argv`) that sorts the report alphabetically instead of by revenue.

## Marking rubric

| Criteria | Max | Notes |
|---|---|---|
| `parse_line` correct types & blank handling | 2 | returns tuple or None |
| `read_sales` skips header, no errors | 2 | 8 rows parsed |
| `totals_by_product` correct math | 3 | values match expected |
| `print_report` sorted + grand total | 3 | formatting close to expected |
| Comprehension used & commented | 1 | anywhere in script |
| Answers to questions | 2 | Q2, Q3 correct |
| Challenge: units max + `--sort` flag | 3 | both work |
| **Total** | **16** | |