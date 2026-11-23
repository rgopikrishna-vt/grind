---
id: missing-numbers
title: Missing numbers and pangrams
topic: Sets
difficulty: easy
lesson: 10
---

## Prompt
Two set exercises:

- `missing(nums, n)` returns a **sorted list** of the numbers from 1 to `n` that are not in `nums`. `missing([3, 1, 5], 5)` is `[2, 4]`.
- `is_pangram(sentence)` returns `True` if the sentence uses every letter `a` to `z` at least once, ignoring case.

## Starter
```python
import string

def missing(nums, n):
    pass


def is_pangram(sentence):
    pass
```

## Examples
```python
assert missing([3, 1, 5], 5) == [2, 4]
assert is_pangram("The quick brown fox jumps over the lazy dog") == True
```

## Tests
```python
assert missing([], 3) == [1, 2, 3]
assert missing([1, 2, 3], 3) == []
assert missing([2, 2, 2, 9, 0], 4) == [1, 3, 4]
assert missing([5], 0) == []
assert is_pangram("") == False
assert is_pangram("abcdefghijklmnopqrstuvwxy") == False
assert is_pangram("Pack my box with FIVE dozen liquor jugs!") == True
```

## Hints
- `set(range(1, n + 1)) - set(nums)` is exactly the missing numbers.
- `string.ascii_lowercase` is `"abcdefghijklmnopqrstuvwxyz"`.
- A set `a` is a subset of `b` when `a <= b` (or `a.issubset(b)`).

## Solution
```python
import string

def missing(nums, n):
    return sorted(set(range(1, n + 1)) - set(nums))


def is_pangram(sentence):
    return set(string.ascii_lowercase) <= set(sentence.lower())
```

## Explanation
Set difference (`-`) and subset (`<=`) turn what would be nested loops into single expressions. Building the sets is O(n), and the operations are linear in the set sizes.
