---
id: collatz
title: Collatz steps
topic: Loops and conditionals
difficulty: easy
---

## Prompt
Start from a positive integer `n`. If it is even, halve it; if it is odd, replace it with `3n + 1`. Repeat until you reach 1.

Write `collatz_steps(n)` that returns how many steps that takes. `collatz_steps(6)` is `8`:
`6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1`.

Use a `while` loop. If `n` is less than 1, raise `ValueError`.

## Starter
```python
def collatz_steps(n):
    pass
```

## Examples
```python
assert collatz_steps(6) == 8
assert collatz_steps(1) == 0
```

## Tests
```python
assert collatz_steps(2) == 1
assert collatz_steps(7) == 16
assert collatz_steps(27) == 111
assert collatz_steps(97) == 118
try:
    collatz_steps(0)
    raised = False
except ValueError:
    raised = True
assert raised, "collatz_steps(0) should raise ValueError"
```

## Hints
- `while n != 1:` and count each pass through the loop.
- Use `n //= 2` (not `/`) so `n` stays an int.
- Put the check `if n < 1: raise ValueError("n must be positive")` at the top.

## Solution
```python
def collatz_steps(n):
    if n < 1:
        raise ValueError("n must be positive")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps
```

## Explanation
`/` always returns a float in Python 3, even `6 / 2 == 3.0`. Use `//` for integer division. Raising `ValueError` for a bad argument is the Python convention.
