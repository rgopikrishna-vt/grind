---
id: digit-sum
title: Sum of digits
topic: Operators
difficulty: easy
lesson: 4
---

## Prompt
Write `digit_sum(n)` that returns the sum of the decimal digits of the integer `n`. Negative numbers count their digits too, so `digit_sum(-123)` is `6`.

Try it **without** converting to a string: use `//` (floor division) and `%` (remainder).

## Starter
```python
def digit_sum(n):
    pass
```

## Examples
```python
assert digit_sum(123) == 6
assert digit_sum(-45) == 9
```

## Tests
```python
assert digit_sum(0) == 0
assert digit_sum(7) == 7
assert digit_sum(1000) == 1
assert digit_sum(99999) == 45
assert digit_sum(-123) == 6
assert digit_sum(10 ** 20) == 1
```

## Hints
- `n % 10` is the last digit and `n // 10` drops it.
- Repeat in a `while n > 0:` loop, adding each last digit to a total.
- Use `abs(n)` first. In Python, `-123 // 10` is `-13` and `-123 % 10` is `7`, because floor division rounds toward minus infinity.

## Solution
```python
def digit_sum(n):
    n = abs(n)
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total
```

## Explanation
`%` and `//` peel digits off the right. Interview gotcha: in Python, `//` floors toward negative infinity (`-7 // 2 == -4`) and `%` takes the sign of the divisor (`-7 % 2 == 1`). Taking `abs()` first avoids both. The one-liner is `sum(int(d) for d in str(abs(n)))`.
