---
id: valid-parentheses
title: Valid parentheses
topic: Lists
difficulty: medium
---

## Prompt
Write `is_valid(s)` that checks whether the brackets in `s` are balanced and properly nested. The string contains only `()[]{}`.

- `"()[]{}"` and `"{[()]}"` are valid
- `"(]"` and `"([)]"` are not
- the empty string is valid

This is the textbook use of a stack.

## Starter
```python
def is_valid(s):
    pass
```

## Examples
```python
assert is_valid("()[]{}") == True
assert is_valid("([)]") == False
```

## Tests
```python
assert is_valid("") == True
assert is_valid("{[()]}") == True
assert is_valid("(]") == False
assert is_valid("(") == False
assert is_valid(")") == False
assert is_valid("((()))[]") == True
assert is_valid("){") == False
assert is_valid("(" * 5000 + ")" * 5000) == True
```

## Hints
- Push every opening bracket onto a list. On a closing bracket, the top of the stack must be its matching opener.
- A dict maps closers to openers: `pairs = {")": "(", "]": "[", "}": "{"}`.
- Two easy-to-miss failures: a closer when the stack is empty, and leftover openers at the end.

## Solution
```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```

## Explanation
Last opened, first closed: that's exactly a stack's LIFO order. `return not stack` covers the leftover-openers case in one expression.
