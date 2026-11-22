---
id: receipt
title: Format a receipt
topic: Input and f-strings
difficulty: medium
---

## Prompt
Write `receipt(items)` where `items` is a list of `(name, price)` tuples. Return a single string with one line per item, then a total line, joined with `"\n"`:

- the name left-aligned in a field 12 characters wide
- the price right-aligned in a field 8 characters wide, with 2 decimal places
- a last line `TOTAL` formatted the same way

```
Coffee          3.50
Bagel           2.25
TOTAL           5.75
```

Use f-string format specs like `{name:<12}` and `{price:>8.2f}`.

## Starter
```python
def receipt(items):
    lines = []
    # your code here
    return "\n".join(lines)
```

## Examples
```python
assert receipt([("Coffee", 3.5), ("Bagel", 2.25)]) == "Coffee          3.50\nBagel           2.25\nTOTAL           5.75"
```

## Tests
```python
assert receipt([]) == "TOTAL           0.00"
assert receipt([("Tea", 2)]) == "Tea             2.00\nTOTAL           2.00"
assert receipt([("Sandwich", 7.999)]).splitlines()[0] == "Sandwich        8.00"
assert all(len(line) == 20 for line in receipt([("A", 1), ("Long name", 123.4)]).splitlines())
assert receipt([("A", 1), ("B", 2), ("C", 3)]).splitlines()[-1] == "TOTAL           6.00"
```

## Hints
- `f"{name:<12}"` pads `name` with spaces on the right to 12 characters.
- `f"{price:>8.2f}"` right-aligns in 8 characters with 2 decimals.
- Keep a running `total` and add one more line for it after the loop.

## Solution
```python
def receipt(items):
    lines = []
    total = 0
    for name, price in items:
        lines.append(f"{name:<12}{price:>8.2f}")
        total += price
    lines.append(f"{'TOTAL':<12}{total:>8.2f}")
    return "\n".join(lines)
```

## Explanation
The format spec after the colon is `[fill][align][width][.precision][type]`: `<` left, `>` right, `^` center; `.2f` means fixed-point with 2 decimals. Other useful ones: `{n:,}` for thousands separators, `{x:.1%}` for percentages, `{n:05d}` for zero padding, and `{value!r}` for the repr.
