---
id: grid-aliasing
title: The shared-rows grid bug
topic: Python gotchas
difficulty: easy
---

## Prompt
This looks like it makes a 3×4 grid of zeros, but setting one cell changes a whole column:

```python
def make_grid(rows, cols, fill=0):
    return [[fill] * cols] * rows

g = make_grid(3, 4)
g[0][0] = 1
g   # [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]  <- every row changed!
```

Fix `make_grid` so every row is an **independent** list.

## Starter
```python
def make_grid(rows, cols, fill=0):
    return [[fill] * cols] * rows
```

## Examples
```python
g = make_grid(3, 4)
g[0][0] = 1
assert g == [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
```

## Tests
```python
assert make_grid(0, 5) == []
assert make_grid(2, 0) == [[], []]
assert make_grid(1, 2, ".") == [[".", "."]]
h = make_grid(4, 2)
assert len({id(row) for row in h}) == 4, "each row must be its own list"
h[3][1] = 9
assert sum(map(sum, h)) == 9
```

## Hints
- `[row] * 3` makes a list holding the **same** row object three times; that's aliasing.
- Build a new row on every iteration with a comprehension: `[[fill] * cols for _ in range(rows)]`.

## Solution
```python
def make_grid(rows, cols, fill=0):
    return [[fill] * cols for _ in range(rows)]
```

## Explanation
`*` on a list copies references, not objects. `[0] * 4` is fine because ints are immutable, but `[[0] * 4] * 3` repeats one inner list. The comprehension runs `[fill] * cols` fresh each time. (If `fill` itself were a mutable object, you'd need to create it inside the loop too.)
