---
id: two-sum
title: Two Sum
topic: Lists
difficulty: easy
---

## Prompt
The most famous interview question. Given a list `nums` and a `target`, return the **indexes** `[i, j]` (with `i < j`) of the two numbers that add up to `target`. Exactly one answer exists, and you may not use the same element twice.

Aim for a single pass with a dict, not two nested loops.

## Starter
```python
def two_sum(nums, target):
    pass
```

## Examples
```python
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
```

## Tests
```python
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([1, 5, 9, 13], 22) == [2, 3]
assert two_sum([-3, 4, 3, 90], 0) == [0, 2]
assert two_sum([0, 4, 3, 0], 0) == [0, 3]
assert two_sum(list(range(10000)), 19997) == [9998, 9999]
```

## Hints
- For each number `x`, the partner you need is `target - x`.
- Keep a dict of `value -> index` for the numbers you've already seen.
- Check whether the partner is in the dict *before* adding the current number, so you don't pair a number with itself.

## Solution
```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        partner = target - x
        if partner in seen:
            return [seen[partner], i]
        seen[x] = i
    return []
```

## Explanation
Dict lookups are O(1) on average, so this is O(n) time and O(n) space, versus O(n²) for checking every pair. Say the trade-off out loud in an interview.
