---
id: invert-dict
title: Invert a dictionary
topic: Dictionaries
difficulty: easy
---

## Prompt
Write `invert(d)` that swaps keys and values. Several keys can share a value, so each new value is a **list** of the original keys, in their original order.

`invert({"a": 1, "b": 2, "c": 1})` returns `{1: ["a", "c"], 2: ["b"]}`.

## Starter
```python
def invert(d):
    pass
```

## Examples
```python
assert invert({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}
```

## Tests
```python
assert invert({}) == {}
assert invert({"x": "y"}) == {"y": ["x"]}
assert invert({1: "odd", 2: "even", 3: "odd", 4: "even"}) == {"odd": [1, 3], "even": [2, 4]}
original = {"a": 1}
invert(original)
assert original == {"a": 1}
```

## Hints
- Loop with `for key, value in d.items():`.
- `result.setdefault(value, []).append(key)` creates the list the first time a value is seen.

## Solution
```python
def invert(d):
    result = {}
    for key, value in d.items():
        result.setdefault(value, []).append(key)
    return result
```

## Explanation
If all values were unique you could write `{v: k for k, v in d.items()}`, but with duplicates that comprehension silently keeps only the last key. `setdefault` (or `defaultdict(list)`) is the pattern for grouping.
