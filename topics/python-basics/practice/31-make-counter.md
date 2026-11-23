---
id: make-counter
title: Counter with a closure
topic: Scope and closures
difficulty: medium
lesson: 18
---

## Prompt
Write `make_counter(start=0, step=1)` that returns a **function**. Each call to that function returns the next value: first `start`, then `start + step`, and so on. Separate counters must not share state.

```python
c = make_counter()
c(), c(), c()     # 0, 1, 2
d = make_counter(10, 5)
d(), d()          # 10, 15
c()               # 3
```

Use a nested function and `nonlocal`. Don't use a class or a global.

## Starter
```python
def make_counter(start=0, step=1):
    pass
```

## Examples
```python
c = make_counter()
assert [c(), c(), c()] == [0, 1, 2]
```

## Tests
```python
d = make_counter(10, 5)
assert d() == 10
assert d() == 15
a = make_counter()
b = make_counter()
a(); a(); a()
assert b() == 0
assert a() == 3
neg = make_counter(0, -2)
assert [neg() for _ in range(3)] == [0, -2, -4]
assert callable(make_counter())
```

## Hints
- Define `def counter():` inside `make_counter` and `return counter` (no parentheses).
- The inner function needs to *reassign* a variable from the outer function, which needs `nonlocal current`.
- Return the current value, then advance it. Saving `value = current` before adding `step` helps.

## Solution
```python
def make_counter(start=0, step=1):
    current = start

    def counter():
        nonlocal current
        value = current
        current += step
        return value

    return counter
```

## Explanation
A closure remembers the variables of the function it was created in. Reading them needs nothing special, but assigning to one makes Python treat it as a new local unless you declare `nonlocal`. Without it you get `UnboundLocalError`, a common interview question.
