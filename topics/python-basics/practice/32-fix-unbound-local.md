---
id: fix-unbound-local
title: Fix the UnboundLocalError
topic: Scope and closures
difficulty: easy
lesson: 18
---

## Prompt
This code crashes with `UnboundLocalError: cannot access local variable 'total'` on the first call:

```python
total = 0

def add(n):
    total += n
    return total
```

Fix it so that `add` updates the **module-level** `total`. Calls accumulate: `add(5)` returns 5, then `add(3)` returns 8, and afterwards the global `total` is 8.

Then explain to yourself why the original fails. (Python decides a name is local if it is *assigned* anywhere in the function.)

## Starter
```python
total = 0

def add(n):
    total += n
    return total
```

## Examples
```python
assert add(5) == 5
assert add(3) == 8
```

## Tests
```python
assert total == 8
assert add(0) == 8
assert add(-10) == -2
assert total == -2
```

## Hints
- `total += n` is an assignment, so Python treats `total` as local to `add`, and it has no value yet when `+=` reads it.
- Declare `global total` as the first line of the function.

## Solution
```python
total = 0

def add(n):
    global total
    total += n
    return total
```

## Explanation
Name lookup follows LEGB: Local, Enclosing function, Global (module), Built-in. Reading a global needs no declaration, but assigning to one does: `global` for module names, `nonlocal` for an enclosing function's names. In real code prefer returning values or using a class over mutating globals.
