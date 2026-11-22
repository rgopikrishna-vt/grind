---
id: reverse-words
title: Reverse the words
topic: Strings
difficulty: easy
---

## Prompt
Write `reverse_words(s)` that returns the words of `s` in reverse order, separated by single spaces. Leading, trailing and repeated spaces should disappear.

`reverse_words("  the sky   is blue ")` returns `"blue is sky the"`.

## Starter
```python
def reverse_words(s):
    pass
```

## Examples
```python
assert reverse_words("the sky is blue") == "blue is sky the"
assert reverse_words("  hello   world  ") == "world hello"
```

## Tests
```python
assert reverse_words("") == ""
assert reverse_words("one") == "one"
assert reverse_words("   ") == ""
assert reverse_words("a b c d") == "d c b a"
assert reverse_words("Python  is\tfun") == "fun is Python"
```

## Hints
- `s.split()` with no argument splits on any run of whitespace and drops empty strings.
- `reversed(words)` or `words[::-1]` gives the words backwards.
- `" ".join(...)` glues them back together.

## Solution
```python
def reverse_words(s):
    return " ".join(reversed(s.split()))
```

## Explanation
`split()` and `split(" ")` differ: `"a  b".split(" ")` gives `['a', '', 'b']`, but `"a  b".split()` gives `['a', 'b']`. The no-argument form is almost always what you want for words.
