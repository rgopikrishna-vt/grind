---
id: flatten
title: Flatten and filter
topic: Comprehensions
difficulty: easy
lesson: 17
---

## Prompt
Two short functions, each one comprehension:

- `flatten(matrix)` turns a list of lists into one flat list: `[[1, 2], [3], []]` becomes `[1, 2, 3]`.
- `even_squares(nums)` returns the squares of the **even** numbers only, in order: `[1, 2, 3, 4]` becomes `[4, 16]`.

## Starter
```python
def flatten(matrix):
    pass


def even_squares(nums):
    pass
```

## Examples
```python
assert flatten([[1, 2], [3], []]) == [1, 2, 3]
assert even_squares([1, 2, 3, 4]) == [4, 16]
```

## Tests
```python
assert flatten([]) == []
assert flatten([[], []]) == []
assert flatten([["a"], ["b", "c"]]) == ["a", "b", "c"]
assert flatten([[[1]], [[2]]]) == [[1], [2]]
assert even_squares([]) == []
assert even_squares([1, 3, 5]) == []
assert even_squares([-2, 0, 7]) == [4, 0]
```

## Hints
- A nested comprehension reads in the same order as nested loops: `[x for row in matrix for x in row]`.
- Put the filter at the end: `[n * n for n in nums if n % 2 == 0]`.

## Solution
```python
def flatten(matrix):
    return [x for row in matrix for x in row]


def even_squares(nums):
    return [n * n for n in nums if n % 2 == 0]
```

## Explanation
In `[x for row in matrix for x in row]` the `for` clauses go outer to inner, exactly like writing the loops out. An `if` at the end filters; a conditional expression at the front (`a if c else b`) transforms. Swap the brackets for parentheses to get a lazy generator expression.
