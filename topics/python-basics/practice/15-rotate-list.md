---
id: rotate-list
title: Rotate a list
topic: Lists
difficulty: easy
lesson: 7
---

## Prompt
Write `rotate(nums, k)` that returns a **new** list with the elements rotated `k` steps to the right. `k` can be larger than the list length, and can be negative (rotate left).

`rotate([1, 2, 3, 4, 5], 2)` returns `[4, 5, 1, 2, 3]`.

## Starter
```python
def rotate(nums, k):
    pass
```

## Examples
```python
assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
assert rotate([1, 2, 3], 4) == [3, 1, 2]
```

## Tests
```python
assert rotate([], 3) == []
assert rotate([1], 100) == [1]
assert rotate([1, 2, 3], 0) == [1, 2, 3]
assert rotate([1, 2, 3], 3) == [1, 2, 3]
assert rotate([1, 2, 3, 4], -1) == [2, 3, 4, 1]
original = [1, 2, 3]
rotate(original, 1)
assert original == [1, 2, 3]
```

## Hints
- Rotating by `len(nums)` gives the same list back, so reduce `k` with `k % len(nums)`. Python's `%` turns a negative `k` into the equivalent right rotation.
- Watch out for the empty list: `% 0` raises `ZeroDivisionError`.
- The answer is two slices glued together: the last `k` elements, then the rest.

## Solution
```python
def rotate(nums, k):
    if not nums:
        return []
    k %= len(nums)
    return nums[-k:] + nums[:-k] if k else nums[:]
```

## Explanation
Careful with `k == 0`: `nums[-0:]` is `nums[0:]`, the whole list, so `nums[-0:] + nums[:-0]` would be the whole list plus nothing. That happens to work, but only by luck; handling `k == 0` explicitly is clearer. `collections.deque` also has a `rotate(k)` method.
