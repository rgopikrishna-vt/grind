---
id: max-subarray
title: Maximum subarray
topic: Lists
difficulty: medium
---

## Prompt
Given a non-empty list of integers, return the **largest sum** of any contiguous run of elements (at least one element).

For `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` the best run is `[4, -1, 2, 1]`, so the answer is `6`.

Can you do it in one pass (O(n))? This is Kadane's algorithm.

## Starter
```python
def max_subarray(nums):
    pass
```

## Examples
```python
assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert max_subarray([1]) == 1
```

## Tests
```python
assert max_subarray([5, 4, -1, 7, 8]) == 23
assert max_subarray([-3, -1, -2]) == -1
assert max_subarray([0, 0, 0]) == 0
assert max_subarray([2, -1, 2]) == 3
assert max_subarray([-1, 3, -2, 5, -10, 4]) == 6
assert max_subarray(list(range(-5000, 5001))) == sum(range(1, 5001))
```

## Hints
- At each position, the best run *ending here* either extends the previous best run or starts fresh at this element.
- `current = max(x, current + x)`.
- Track the best `current` ever seen. Start both at `nums[0]` so an all-negative list works.

## Solution
```python
def max_subarray(nums):
    current = best = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best
```

## Explanation
If the running sum goes negative, it can only hurt what comes next, so you drop it and start again. Initialising `best = 0` is a common bug: it gives the wrong answer for all-negative input.
