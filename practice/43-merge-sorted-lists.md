---
id: merge-sorted-lists
title: Merge K sorted lists
topic: The heapq module
difficulty: medium
---

## Prompt
Write `merge_lists(lists)` that merges any number of **sorted** lists into one sorted list, using a heap of size *k* (one entry per list) rather than concatenating and sorting.

`merge_lists([[1, 4, 7], [2, 5], [3, 6, 9]])` returns `[1, 2, 3, 4, 5, 6, 7, 9]`.

Don't use `heapq.merge`; build it with `heappush` / `heappop`.

## Starter
```python
import heapq

def merge_lists(lists):
    pass
```

## Examples
```python
assert merge_lists([[1, 4, 7], [2, 5], [3, 6, 9]]) == [1, 2, 3, 4, 5, 6, 7, 9]
```

## Tests
```python
assert merge_lists([]) == []
assert merge_lists([[], []]) == []
assert merge_lists([[1, 2, 3]]) == [1, 2, 3]
assert merge_lists([[1, 1], [1], [0, 2]]) == [0, 1, 1, 1, 2]
assert merge_lists([[-5, 0], [-10, 10]]) == [-10, -5, 0, 10]
assert merge_lists([list(range(i, 3000, 7)) for i in range(7)]) == list(range(3000))
```

## Hints
- Push `(value, list_index, element_index)` for the first element of every non-empty list.
- Pop the smallest, append its value, then push the next element from the same list if there is one.
- The `list_index` in the tuple also breaks ties, so Python never has to compare anything else.

## Solution
```python
import heapq

def merge_lists(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    result = []
    while heap:
        value, i, j = heapq.heappop(heap)
        result.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return result
```

## Explanation
Each pop/push is O(log k), so merging N total items costs O(N log k). `heapify` builds a heap from a list in O(n). Putting a unique index in the tuple matters when the values themselves can't be compared, like dicts or custom objects.
