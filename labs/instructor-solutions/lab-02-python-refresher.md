# Lab 02 — Solution: Python Refresher

**Session:** W1 S2 · **CLO:** CLO-1

## Complete solution

```python
# sales.py
def parse_line(line):
    """'coffee,3,2.50' -> ('coffee', 3, 2.5). Return None for blank lines."""
    line = line.strip()
    if not line:
        return None
    product, units, price = line.split(",")
    return (product, int(units), float(price))   # tuple: mixed types OK


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
        revenue = units * price
        totals[product] = totals.get(product, 0) + revenue
    return totals


def print_report(totals):
    # sorted by revenue descending; unpack items for readability
    ordered = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    for product, revenue in ordered:
        print(f"{product:<10} {revenue:>7.2f}")
    print(f"{'grand total':<10} {sum(totals.values()):>7.2f}")


if __name__ == "__main__":
    rows = read_sales("sales.txt")
    totals = totals_by_product(rows)
    print_report(totals)
```

Expected run:

```
cake         12.00
juice        12.00
coffee       15.00
tea           8.40
grand total  47.40
```

## Model answers

1. **Tuple** — fixed number of heterogeneous values (str, int, float) in a
   fixed order; good for "one row" records. A list would also work but a
   tuple signals "this record's shape never changes."
2. **Header skip** — the first line names columns, not data; parsing it
   would crash `int("product")`.
3. **String math** — `"3" * 2.5` raises `TypeError`; even `"3" + "2"` would
   concatenate. Types must be converted (`int`/`float`) before arithmetic.
4. **defaultdict version:**

```python
from collections import defaultdict

def totals_by_product(rows):
    totals = defaultdict(float)
    for product, units, price in rows:
        totals[product] += units * price
    return dict(totals)
```

5. **Zero units** — the row contributes 0.0 to `tea`; report still shows
   `tea 8.40` only from the other two rows. No crash.

## Challenge solution

```python
import sys

def max_units(rows):
    units = {}
    for product, qty, _ in rows:
        units[product] = units.get(product, 0) + qty
    return max(units, key=units.get)     # product with most units

# in main():
if "--sort" in sys.argv and sys.argv[sys.argv.index("--sort") + 1] == "alpha":
    ordered = sorted(totals.items())     # alphabetical
else:
    ordered = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
```

Output for the units part: `best by units: coffee` (3+2+1 = 6 units vs.
cake 3, tea 7 — with this data tea actually wins with 7 units; the expected
line in the student lab is illustrative — grade on correctness of the
computed answer).