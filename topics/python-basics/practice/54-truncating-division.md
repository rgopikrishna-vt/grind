---
id: truncating-division
title: Division that truncates toward zero
topic: Python gotchas
difficulty: medium
lesson: 30
---

## Prompt
Python's `//` rounds **down** (toward negative infinity): `-7 // 2` is `-4`, and `-7 % 2` is `1`. Languages like C, Java and JavaScript truncate toward zero instead (`-7 / 2` is `-3`, remainder `-1`).

Write `c_divmod(a, b)` that returns `(quotient, remainder)` the C way: the quotient truncated toward zero and `a == quotient * b + remainder`. Use only integer operations (no `float`, no `math.trunc(a / b)`) so it stays exact for huge numbers.

## Starter
```python
def c_divmod(a, b):
    pass
```

## Examples
```python
assert c_divmod(-7, 2) == (-3, -1)
assert c_divmod(7, 2) == (3, 1)
```

## Tests
```python
assert c_divmod(7, -2) == (-3, 1)
assert c_divmod(-7, -2) == (3, -1)
assert c_divmod(0, 5) == (0, 0)
assert c_divmod(-6, 3) == (-2, 0)
assert c_divmod(10 ** 30 + 1, -3) == (-(10 ** 30 // 3), 2)
for a in range(-20, 21):
    for b in (-7, -3, -1, 1, 4):
        q, r = c_divmod(a, b)
        assert q * b + r == a and abs(r) < abs(b) and (r == 0 or (r < 0) == (a < 0)), (a, b)
```

## Hints
- Truncating toward zero equals floor division on the absolute values, with the sign put back.
- `q = abs(a) // abs(b)`, then negate it if exactly one of `a`, `b` is negative.
- Get the remainder from the definition: `r = a - q * b`.

## Solution
```python
def c_divmod(a, b):
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return q, a - q * b
```

## Explanation
Python chose floor division so that `a % b` always has the sign of `b`, which makes things like `index % len(items)` work for negative indexes. When porting C or Java code, or with problems like "evaluate reverse Polish notation", you need truncation: `int(a / b)` works for small numbers but loses precision past 2**53.
