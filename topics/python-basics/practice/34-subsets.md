---
id: subsets
title: All subsets
topic: Recursion
difficulty: medium
lesson: 19
---

## Prompt
Write `subsets(nums)` that returns **every** subset of the list `nums` (the power set), each subset as a list.

The order matters for the tests: build them so that subsets **without** the first element come before subsets **with** it, recursively. For `[1, 2]`:

```python
[[], [2], [1], [1, 2]]
```

A list of `n` items has `2 ** n` subsets.

## Starter
```python
def subsets(nums):
    pass
```

## Examples
```python
assert subsets([1, 2]) == [[], [2], [1], [1, 2]]
```

## Tests
```python
assert subsets([]) == [[]]
assert subsets([7]) == [[], [7]]
assert subsets([1, 2, 3]) == [[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]
assert len(subsets(list(range(10)))) == 1024
assert sorted(map(sorted, subsets(["a", "b", "c"]))) == sorted(map(sorted, [[], ["a"], ["b"], ["c"], ["a", "b"], ["a", "c"], ["b", "c"], ["a", "b", "c"]]))
```

## Hints
- Base case: the empty list has exactly one subset, `[[]]`.
- Recursive case: compute `rest = subsets(nums[1:])`. Every subset either leaves out `nums[0]` (that's `rest`) or includes it.
- `return rest + [[nums[0]] + s for s in rest]`

## Solution
```python
def subsets(nums):
    if not nums:
        return [[]]
    rest = subsets(nums[1:])
    return rest + [[nums[0]] + s for s in rest]
```

## Explanation
Include-or-exclude is the core idea of most backtracking problems (combinations, permutations, N-queens). `itertools.combinations(nums, k)` generates subsets of one size `k` without writing recursion yourself.
