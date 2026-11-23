---
id: permutations-copy
title: Backtracking: append a copy
topic: Python gotchas
difficulty: medium
lesson: 30
---

## Prompt
This backtracking code should return every permutation of `nums`, but it returns a list of **empty** lists:

```python
def permutations(nums):
    results, current = [], []
    def backtrack():
        if len(current) == len(nums):
            results.append(current)
            return
        ...
```

`results.append(current)` stores a reference to the one `current` list, which is empty again by the end. Finish the function and fix the bug. Produce the permutations in this order: pick unused elements from left to right.

## Starter
```python
def permutations(nums):
    results, current = [], []
    used = [False] * len(nums)

    def backtrack():
        if len(current) == len(nums):
            results.append(current)
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                backtrack()
                current.pop()
                used[i] = False

    backtrack()
    return results
```

## Examples
```python
assert permutations([1, 2, 3]) == [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```

## Tests
```python
assert permutations([]) == [[]]
assert permutations([7]) == [[7]]
assert permutations(["a", "b"]) == [["a", "b"], ["b", "a"]]
res = permutations([1, 2, 3, 4])
assert len(res) == 24 and len({tuple(p) for p in res}) == 24
assert len({id(p) for p in res}) == 24, "each result must be its own list"
```

## Hints
- The search logic is already right; the only bug is on the `append` line.
- Append a snapshot: `results.append(current.copy())` (or `current[:]`, or `list(current)`).

## Solution
```python
def permutations(nums):
    results, current = [], []
    used = [False] * len(nums)

    def backtrack():
        if len(current) == len(nums):
            results.append(current.copy())
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                backtrack()
                current.pop()
                used[i] = False

    backtrack()
    return results
```

## Explanation
Backtracking mutates one working list (choose, explore, un-choose), so every saved result must be a copy taken at that moment. The same bug shows up with subsets, combinations and N-queens. `itertools.permutations(nums)` gives tuples in this same order.
