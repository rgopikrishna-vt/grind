---
id: flatten-deep
title: Deep flatten
topic: Recursion
difficulty: medium
---

## Prompt
Write `flatten_deep(items)` that flattens arbitrarily nested lists into one flat list, keeping order.

`flatten_deep([1, [2, [3, [4]], 5]])` returns `[1, 2, 3, 4, 5]`.

Only `list` counts as nesting. Strings, tuples and everything else are kept as single values.

## Starter
```python
def flatten_deep(items):
    pass
```

## Examples
```python
assert flatten_deep([1, [2, [3, [4]], 5]]) == [1, 2, 3, 4, 5]
```

## Tests
```python
assert flatten_deep([]) == []
assert flatten_deep([[], [[]], [[[]]]]) == []
assert flatten_deep([1, 2, 3]) == [1, 2, 3]
assert flatten_deep(["ab", ["cd"]]) == ["ab", "cd"]
assert flatten_deep([(1, 2), [3]]) == [(1, 2), 3]
assert flatten_deep([[[[[[["deep"]]]]]]]) == ["deep"]
```

## Hints
- Base case: a non-list value is just appended. Recursive case: a list is flattened and its result added.
- `isinstance(x, list)` tells you which case you're in.
- `result.extend(flatten_deep(x))` adds all items from the recursive call.

## Solution
```python
def flatten_deep(items):
    result = []
    for x in items:
        if isinstance(x, list):
            result.extend(flatten_deep(x))
        else:
            result.append(x)
    return result
```

## Explanation
Every recursive function needs a base case that stops the recursion. Python's default recursion limit is about 1000 frames, so for very deep input you'd switch to an explicit stack: pop an item, and if it's a list push its children in reverse.
