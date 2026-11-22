---
id: kth-largest
title: Kth largest element
topic: The heapq module
difficulty: medium
---

## Prompt
Write `kth_largest(nums, k)` that returns the `k`-th largest value (1-based: `k = 1` is the maximum). Duplicates count separately, so in `[3, 3, 1]` the 2nd largest is `3`.

Do it with `heapq` by keeping a min-heap of size `k`, which is O(n log k), rather than sorting the whole list.

## Starter
```python
import heapq

def kth_largest(nums, k):
    pass
```

## Examples
```python
assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert kth_largest([3, 3, 1], 2) == 3
```

## Tests
```python
assert kth_largest([1], 1) == 1
assert kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
assert kth_largest([-1, -2, -3], 1) == -1
assert kth_largest([-1, -2, -3], 3) == -3
assert kth_largest(list(range(100000)), 10) == 99990
```

## Hints
- `heapq` keeps the **smallest** item at `heap[0]`.
- Push each number; when the heap grows past `k` items, pop the smallest. The `k` largest survive.
- Then `heap[0]` is the smallest of the `k` largest, which is the answer. (`heapq.heappushpop` does push-then-pop in one step.)

## Solution
```python
import heapq

def kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

## Explanation
Python only has a min-heap; for a max-heap push negated values. `heapq.nlargest(k, nums)[-1]` is the one-liner. Interviewers may also ask about quickselect, which averages O(n).
