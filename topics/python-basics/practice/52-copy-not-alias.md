---
id: copy-not-alias
title: Copy, don't alias
topic: Python gotchas
difficulty: easy
lesson: 30
---

## Prompt
`b = a` doesn't copy a list; both names point to the same object. Fix these two functions so they **never modify their input**:

- `with_item(items, x)` returns a new list with `x` appended.
- `with_cell(board, r, c, value)` takes a list of lists and returns a new board with one cell changed. The original board, **including its inner rows**, must stay unchanged.

## Starter
```python
def with_item(items, x):
    result = items
    result.append(x)
    return result


def with_cell(board, r, c, value):
    new_board = board.copy()
    new_board[r][c] = value
    return new_board
```

## Examples
```python
a = [1, 2]
assert with_item(a, 3) == [1, 2, 3]
assert a == [1, 2]
```

## Tests
```python
board = [[0, 0], [0, 0]]
new = with_cell(board, 0, 1, 5)
assert new == [[0, 5], [0, 0]]
assert board == [[0, 0], [0, 0]], "the original board changed: copy the inner rows too"
assert new is not board
empty = []
assert with_item(empty, "x") == ["x"] and empty == []
assert with_item((), 1) == [1]
```

## Hints
- `list(items)`, `items[:]` and `items.copy()` all make a **shallow** copy: a new outer list holding the same elements.
- `board.copy()` copies only the outer list; the rows inside are shared. Copy each row: `[row[:] for row in board]`.
- `copy.deepcopy(board)` also works for arbitrarily nested data.

## Solution
```python
def with_item(items, x):
    return list(items) + [x]


def with_cell(board, r, c, value):
    new_board = [row[:] for row in board]
    new_board[r][c] = value
    return new_board
```

## Explanation
Assignment never copies in Python; it binds another name to the same object. A shallow copy duplicates one level; a deep copy (`copy.deepcopy`) duplicates everything reachable. Know which one you need: interviewers love asking what `a` looks like after `b = a; b.append(4)`.
