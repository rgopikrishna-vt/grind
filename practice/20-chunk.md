---
id: chunk
title: Split into chunks
topic: Slicing
difficulty: easy
---

## Prompt
Write `chunk(items, size)` that splits a list into consecutive pieces of length `size`. The last piece may be shorter.

`chunk([1, 2, 3, 4, 5], 2)` returns `[[1, 2], [3, 4], [5]]`.

If `size` is less than 1, raise `ValueError`.

## Starter
```python
def chunk(items, size):
    pass
```

## Examples
```python
assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
```

## Tests
```python
assert chunk([], 3) == []
assert chunk([1, 2, 3], 3) == [[1, 2, 3]]
assert chunk([1, 2, 3], 5) == [[1, 2, 3]]
assert chunk([1, 2, 3, 4], 1) == [[1], [2], [3], [4]]
assert chunk(list("abcdefg"), 3) == [["a", "b", "c"], ["d", "e", "f"], ["g"]]
try:
    chunk([1], 0)
    raised = False
except ValueError:
    raised = True
assert raised, "size 0 should raise ValueError"
```

## Hints
- `range(0, len(items), size)` gives the start index of every chunk.
- Slicing past the end is safe: `[1, 2, 3][2:10]` is `[3]`.
- `[items[i:i + size] for i in range(0, len(items), size)]`

## Solution
```python
def chunk(items, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    return [items[i:i + size] for i in range(0, len(items), size)]
```

## Explanation
Slices never raise `IndexError`; they clip to the sequence. `range`'s third argument is the step. Python 3.12 added `itertools.batched(items, size)`, which yields tuples.
