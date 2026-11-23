---
id: top-k-frequent
title: Top K frequent elements
topic: The collections module
difficulty: medium
lesson: 23
---

## Prompt
Write `top_k(nums, k)` that returns the `k` most frequent values, most frequent first. When two values have the same count, the one that **appears first** in `nums` comes first.

`top_k([1, 1, 1, 2, 2, 3], 2)` returns `[1, 2]`.

## Starter
```python
from collections import Counter

def top_k(nums, k):
    pass
```

## Examples
```python
assert top_k([1, 1, 1, 2, 2, 3], 2) == [1, 2]
```

## Tests
```python
assert top_k([5], 1) == [5]
assert top_k([4, 4, 1, 1, 2], 2) == [4, 1]
assert top_k([1, 2, 3], 3) == [1, 2, 3]
assert top_k(["b", "a", "a", "b", "c"], 1) == ["b"]
assert top_k([3, 3, 2, 2, 2, 1], 3) == [2, 3, 1]
assert top_k([1, 2], 0) == []
```

## Hints
- `Counter(nums)` counts everything in one line.
- `Counter.most_common(k)` returns `[(value, count), ...]`, most common first. Ties keep first-seen order.
- Keep just the values: `[value for value, count in ...]`.

## Solution
```python
from collections import Counter

def top_k(nums, k):
    return [value for value, _ in Counter(nums).most_common(k)]
```

## Explanation
`most_common` is O(n log k) using a heap internally. Interviewers sometimes ask for O(n) with *bucket sort*: make a list of buckets indexed by count, then read buckets from the highest count down.
