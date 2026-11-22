---
id: common-elements
title: Common elements
topic: Sets
difficulty: easy
---

## Prompt
Write `common(a, b)` that returns a **sorted list** of the values that appear in both lists, without duplicates.

`common([1, 2, 2, 3, 4], [2, 4, 4, 6])` returns `[2, 4]`.

Write `has_duplicates(items)` too: it returns `True` if any value appears more than once.

## Starter
```python
def common(a, b):
    pass


def has_duplicates(items):
    pass
```

## Examples
```python
assert common([1, 2, 2, 3, 4], [2, 4, 4, 6]) == [2, 4]
assert has_duplicates([1, 2, 3, 1]) == True
```

## Tests
```python
assert common([], [1, 2]) == []
assert common([1, 2, 3], [4, 5]) == []
assert common(["b", "a", "c"], ["c", "b"]) == ["b", "c"]
assert common([5, 5, 5], [5]) == [5]
assert has_duplicates([]) == False
assert has_duplicates([1, 2, 3]) == False
assert has_duplicates(["a", "b", "a"]) == True
```

## Hints
- `set(a) & set(b)` is the intersection.
- `sorted()` turns any iterable into a sorted list.
- A list has duplicates when converting it to a set makes it shorter.

## Solution
```python
def common(a, b):
    return sorted(set(a) & set(b))


def has_duplicates(items):
    return len(set(items)) != len(items)
```

## Explanation
Set operations: `|` union, `&` intersection, `-` difference, `^` symmetric difference. Membership tests (`x in s`) are O(1) on average for sets but O(n) for lists, which is often the whole point of reaching for a set.
