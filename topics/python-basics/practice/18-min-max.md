---
id: min-max
title: Min and max in one pass
topic: Tuples
difficulty: easy
lesson: 8
---

## Prompt
Write `min_max(nums)` that returns a **tuple** `(smallest, largest)` from a non-empty list, walking the list only once. Don't use the built-in `min()` or `max()` on the list.

Then the caller can unpack it: `lo, hi = min_max([3, 1, 4])`.

## Starter
```python
def min_max(nums):
    pass
```

## Examples
```python
assert min_max([3, 1, 4, 1, 5, 9, 2, 6]) == (1, 9)
assert min_max([7]) == (7, 7)
```

## Tests
```python
assert min_max([-5, -1, -10]) == (-10, -1)
assert min_max([2, 2, 2]) == (2, 2)
assert isinstance(min_max([1, 2]), tuple)
lo, hi = min_max([10, 0, 5])
assert (lo, hi) == (0, 10)
assert min_max([1.5, -0.5]) == (-0.5, 1.5)
```

## Hints
- Start with `lo = hi = nums[0]`.
- Loop over the rest and update `lo` or `hi` when you see something smaller or bigger.
- `return lo, hi` already makes a tuple. The comma creates it, not the parentheses.

## Solution
```python
def min_max(nums):
    lo = hi = nums[0]
    for x in nums[1:]:
        if x < lo:
            lo = x
        elif x > hi:
            hi = x
    return lo, hi
```

## Explanation
Tuples are how Python functions return several values. `return a, b` builds a tuple and `x, y = f()` unpacks it. Remember that a one-element tuple needs a trailing comma: `(5,)`.
