---
id: mutable-default
title: The mutable default trap
topic: Python gotchas
difficulty: easy
---

## Prompt
This function has a famous bug. Each call is supposed to start with a fresh list unless one is passed in:

```python
def append_to(item, target=[]):
    target.append(item)
    return target

append_to(1)   # [1]
append_to(2)   # [1, 2]  <- surprise!
```

Fix `append_to` so that calls without `target` each get a **new** list, while passing a list still appends to that list.

## Starter
```python
def append_to(item, target=[]):
    target.append(item)
    return target
```

## Examples
```python
assert append_to(1) == [1]
assert append_to(2) == [2]
```

## Tests
```python
first = append_to("a")
second = append_to("b")
assert first == ["a"]
assert second == ["b"]
assert first is not second
mine = [0]
assert append_to(1, mine) is mine
assert mine == [0, 1]
empty = []
append_to("x", empty)
assert empty == ["x"], "an empty list passed in must be used, not replaced"
```

## Hints
- Default values are evaluated **once**, when the `def` runs, not on every call. So every call shares the same list.
- Use `None` as the default: `def append_to(item, target=None):`.
- Inside, `if target is None: target = []`. Don't write `if not target:`, because an empty list passed by the caller would be replaced.

## Solution
```python
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

## Explanation
This is one of the most asked Python gotchas. The `None` sentinel is the standard fix. Use `is None` rather than truthiness, so a caller's empty list isn't silently swapped for a new one.
