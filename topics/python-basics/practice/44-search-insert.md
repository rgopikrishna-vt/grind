---
id: search-insert
title: Search insert position
topic: The bisect module
difficulty: easy
lesson: 25
---

## Prompt
Given a **sorted** list `nums` and a `target`, write `insert_position(nums, target)` that returns the index of `target` if it's present (the first one, if repeated), or the index where it would be inserted to keep the list sorted.

Write the binary search yourself, then compare with `bisect.bisect_left`.

## Starter
```python
def insert_position(nums, target):
    pass
```

## Examples
```python
assert insert_position([1, 3, 5, 6], 5) == 2
assert insert_position([1, 3, 5, 6], 2) == 1
```

## Tests
```python
assert insert_position([], 4) == 0
assert insert_position([1, 3, 5, 6], 7) == 4
assert insert_position([1, 3, 5, 6], 0) == 0
assert insert_position([2, 2, 2, 3], 2) == 0
assert insert_position([1, 2, 4, 4, 5], 4) == 2
import bisect
big = list(range(0, 2000000, 2))
assert insert_position(big, 1234567) == bisect.bisect_left(big, 1234567)
```

## Hints
- Keep a range `lo, hi = 0, len(nums)` that always contains the answer.
- Look at `mid = (lo + hi) // 2`. If `nums[mid] < target`, the answer is to the right (`lo = mid + 1`); otherwise it's at `mid` or to the left (`hi = mid`).
- Stop when `lo == hi`; that's the answer.

## Solution
```python
def insert_position(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

## Explanation
This is exactly `bisect.bisect_left`. `bisect_right` returns the position *after* any equal elements, and `bisect.insort` inserts while keeping order. Binary search is O(log n) but only works on sorted data; off-by-one errors in `lo`/`hi` are the usual bug.
