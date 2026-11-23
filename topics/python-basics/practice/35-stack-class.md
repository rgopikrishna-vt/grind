---
id: stack-class
title: Build a Stack class
topic: Classes
difficulty: easy
lesson: 20
---

## Prompt
Write a `Stack` class backed by a list:

- `push(x)` adds to the top
- `pop()` removes and returns the top item; on an empty stack raise `IndexError("pop from empty stack")`
- `peek()` returns the top item without removing it (also `IndexError` when empty)
- `is_empty()` returns `True` or `False`
- `len(stack)` works (define `__len__`)
- `repr(stack)` looks like `Stack([1, 2, 3])` (define `__repr__`)

## Starter
```python
class Stack:
    def __init__(self):
        self._items = []

    # your methods here
```

## Examples
```python
s = Stack()
s.push(1)
s.push(2)
assert s.pop() == 2
assert len(s) == 1
```

## Tests
```python
s = Stack()
assert s.is_empty() == True
assert len(s) == 0
for x in "abc":
    s.push(x)
assert s.peek() == "c"
assert len(s) == 3
assert repr(s) == "Stack(['a', 'b', 'c'])"
assert [s.pop(), s.pop(), s.pop()] == ["c", "b", "a"]
assert s.is_empty() == True
try:
    s.pop()
    raised = False
except IndexError:
    raised = True
assert raised, "pop() on an empty stack should raise IndexError"
try:
    Stack().peek()
    raised = False
except IndexError:
    raised = True
assert raised, "peek() on an empty stack should raise IndexError"
t = Stack()
t.push(1)
assert len(s) == 0, "two stacks must not share items"
```

## Hints
- Every method takes `self` first; use `self._items.append(x)` and `self._items.pop()`.
- `self._items[-1]` is the top. Check `if not self._items:` before reading it.
- `def __repr__(self): return f"Stack({self._items!r})"`

## Solution
```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items!r})"
```

## Explanation
Dunder methods plug your class into Python's syntax: `__len__` for `len()`, `__repr__` for the REPL and debugging, `__eq__` for `==`, `__iter__` for `for` loops. Creating `self._items` inside `__init__` (not as a class attribute) is what keeps each stack's items separate.
