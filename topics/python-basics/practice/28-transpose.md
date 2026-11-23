---
id: transpose
title: Transpose a matrix
topic: enumerate, zip and sorted
difficulty: easy
lesson: 15
---

## Prompt
Write `transpose(matrix)` that turns rows into columns. The input is a list of equal-length lists; return a list of lists.

`transpose([[1, 2, 3], [4, 5, 6]])` returns `[[1, 4], [2, 5], [3, 6]]`.

There's a one-line answer using `zip` and `*` unpacking.

## Starter
```python
def transpose(matrix):
    pass
```

## Examples
```python
assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
```

## Tests
```python
assert transpose([]) == []
assert transpose([[1]]) == [[1]]
assert transpose([[1, 2]]) == [[1], [2]]
assert transpose([[1], [2], [3]]) == [[1, 2, 3]]
m = [[1, 2], [3, 4]]
assert transpose(transpose(m)) == m
assert all(isinstance(row, list) for row in transpose([[1, 2], [3, 4]]))
```

## Hints
- `zip(*matrix)` is `zip(matrix[0], matrix[1], ...)`, which pairs up the first items of each row, then the second items, and so on.
- `zip` yields tuples; convert each with `list(...)`.

## Solution
```python
def transpose(matrix):
    return [list(col) for col in zip(*matrix)]
```

## Explanation
`*` at a call site unpacks a list into separate arguments. `zip` stops at the shortest input; `itertools.zip_longest` pads instead. Python 3.10+ also accepts `zip(a, b, strict=True)` to raise if lengths differ.
