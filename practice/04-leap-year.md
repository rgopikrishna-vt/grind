---
id: leap-year
title: Leap year
topic: Operators
difficulty: easy
---

## Prompt
Write `is_leap(year)` that returns `True` if `year` is a leap year in the Gregorian calendar:

- divisible by 4, **except**
- years divisible by 100 are not leap years, **unless**
- they are also divisible by 400.

So 2024 and 2000 are leap years; 1900 and 2023 are not. Try to write it as a single boolean expression with `and` / `or`.

## Starter
```python
def is_leap(year):
    pass
```

## Examples
```python
assert is_leap(2024) == True
assert is_leap(1900) == False
```

## Tests
```python
assert is_leap(2000) == True
assert is_leap(2023) == False
assert is_leap(2100) == False
assert is_leap(2400) == True
assert is_leap(4) == True
assert is_leap(1) == False
```

## Hints
- "Divisible by 4" is `year % 4 == 0`.
- Leap if: divisible by 4 and not by 100, **or** divisible by 400.
- `return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0`

## Solution
```python
def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
```

## Explanation
Comparisons already produce `True`/`False`, so return the expression directly instead of writing `if ...: return True else: return False`. `and` binds tighter than `or`, but the parentheses make the intent obvious. The standard library has this too: `calendar.isleap`.
