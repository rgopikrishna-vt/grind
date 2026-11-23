---
id: generators
title: Generators and dict comprehensions
topic: Comprehensions
difficulty: medium
lesson: 17
---

## Prompt
Three short pieces:

- `fib()` is an **infinite generator** (use `yield`) producing 0, 1, 1, 2, 3, 5, ...
- `lengths(words)` returns a **dict comprehension** mapping each word to its length, skipping words shorter than 3 characters.
- `total_squares(n)` returns the sum of squares of 1..n using a **generator expression** (no list).

```python
from itertools import islice
list(islice(fib(), 6))     # [0, 1, 1, 2, 3, 5]
lengths(["a", "tree", "sky"])   # {"tree": 4, "sky": 3}
```

## Starter
```python
def fib():
    pass


def lengths(words):
    pass


def total_squares(n):
    pass
```

## Examples
```python
from itertools import islice
assert list(islice(fib(), 6)) == [0, 1, 1, 2, 3, 5]
assert lengths(["a", "tree", "sky"]) == {"tree": 4, "sky": 3}
```

## Tests
```python
import inspect
assert inspect.isgeneratorfunction(fib), "fib must use yield"
assert list(islice(fib(), 12))[-1] == 89
g = fib()
assert [next(g) for _ in range(3)] == [0, 1, 1]
assert lengths([]) == {}
assert lengths(["ab", "abc", "abc"]) == {"abc": 3}
assert total_squares(0) == 0
assert total_squares(3) == 14
assert total_squares(1000) == 333833500
```

## Hints
- A generator function is just a function with `yield` in it: `a, b = 0, 1` then `while True: yield a` and `a, b = b, a + b`.
- Dict comprehension: `{w: len(w) for w in words if len(w) >= 3}`.
- `sum(i * i for i in range(1, n + 1))`: when a generator expression is the only argument, it needs no extra parentheses.

## Solution
```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def lengths(words):
    return {w: len(w) for w in words if len(w) >= 3}


def total_squares(n):
    return sum(i * i for i in range(1, n + 1))
```

## Explanation
Generators produce values lazily, one at a time, so `fib()` can be infinite and `sum(... for ...)` never builds a list in memory. A generator can be consumed only once. Set comprehensions use braces without a colon: `{w[0] for w in words}`.
