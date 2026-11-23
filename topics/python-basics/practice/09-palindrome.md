---
id: palindrome
title: Valid palindrome
topic: Strings
difficulty: easy
lesson: 6
---

## Prompt
Write `is_palindrome(s)` that returns `True` if `s` reads the same forwards and backwards, **ignoring case and any character that isn't a letter or digit**.

`"A man, a plan, a canal: Panama"` is a palindrome. `"race a car"` is not. An empty string counts as a palindrome.

## Starter
```python
def is_palindrome(s):
    pass
```

## Examples
```python
assert is_palindrome("A man, a plan, a canal: Panama") == True
assert is_palindrome("race a car") == False
```

## Tests
```python
assert is_palindrome("") == True
assert is_palindrome(" ") == True
assert is_palindrome("ab") == False
assert is_palindrome("No 'x' in Nixon") == True
assert is_palindrome("0P") == False
assert is_palindrome("Was it a car or a cat I saw?") == True
```

## Hints
- `ch.isalnum()` tells you whether a character is a letter or digit.
- Build a cleaned string: `"".join(ch.lower() for ch in s if ch.isalnum())`.
- A string is a palindrome if it equals its reverse, `cleaned[::-1]`.

## Solution
```python
def is_palindrome(s):
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```

## Explanation
`[::-1]` is a slice with step -1, which reverses a sequence. In an interview you may be asked for O(1) extra space: use two pointers `i` and `j` moving inward, skipping non-alphanumeric characters, and compare `s[i].lower()` with `s[j].lower()`.
