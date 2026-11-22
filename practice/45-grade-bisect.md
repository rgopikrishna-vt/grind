---
id: grade-bisect
title: Letter grades with bisect
topic: The bisect module
difficulty: easy
---

## Prompt
Map a numeric score to a letter grade:

- below 60 → `F`, 60–69 → `D`, 70–79 → `C`, 80–89 → `B`, 90 and above → `A`

Write `letter(score)` using `bisect.bisect` on the breakpoints `[60, 70, 80, 90]` and the string `"FDCBA"`, with no chain of `if` statements. Then write `letters(scores)` returning the list of grades.

## Starter
```python
import bisect

BREAKPOINTS = [60, 70, 80, 90]
GRADES = "FDCBA"

def letter(score):
    pass


def letters(scores):
    pass
```

## Examples
```python
assert letter(85) == "B"
assert letters([33, 99, 77, 70, 89, 90, 100]) == ["F", "A", "C", "C", "B", "A", "A"]
```

## Tests
```python
assert letter(0) == "F"
assert letter(59.9) == "F"
assert letter(60) == "D"
assert letter(69) == "D"
assert letter(79.5) == "C"
assert letter(80) == "B"
assert letters([]) == []
```

## Hints
- `bisect.bisect(BREAKPOINTS, score)` returns how many breakpoints are `<=` score: 0 to 4.
- That number is exactly the index into `GRADES`.
- `bisect` is `bisect_right`, so a score equal to a breakpoint lands in the higher grade, which is what you want here.

## Solution
```python
import bisect

BREAKPOINTS = [60, 70, 80, 90]
GRADES = "FDCBA"

def letter(score):
    return GRADES[bisect.bisect(BREAKPOINTS, score)]


def letters(scores):
    return [letter(s) for s in scores]
```

## Explanation
This lookup-table pattern comes straight from the `bisect` docs, and it works for tax brackets, shipping tiers and any other ranges. `bisect_left` versus `bisect_right` only matters when the value equals a breakpoint: left puts it before equal items, right after.
