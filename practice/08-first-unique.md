---
id: first-unique
title: First unique character
topic: Strings
difficulty: easy
---

## Prompt
Write `first_unique(s)` that returns the **index** of the first character that appears exactly once in `s`, or `-1` if there isn't one.

`first_unique("leetcode")` is `0` (the `l`), `first_unique("loveleetcode")` is `2` (the `v`).

## Starter
```python
def first_unique(s):
    pass
```

## Examples
```python
assert first_unique("leetcode") == 0
assert first_unique("loveleetcode") == 2
```

## Tests
```python
assert first_unique("aabb") == -1
assert first_unique("") == -1
assert first_unique("z") == 0
assert first_unique("aabbc") == 4
assert first_unique("abcabd") == 2
```

## Hints
- Two passes: first count every character, then find the first one whose count is 1.
- A dict works for counting: `counts[ch] = counts.get(ch, 0) + 1`. Or use `collections.Counter(s)`.
- Use `enumerate(s)` in the second pass to get indexes.

## Solution
```python
from collections import Counter

def first_unique(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
```

## Explanation
Counting first makes this O(n). Calling `s.count(ch)` inside the loop would be O(n²), which interviewers will ask you to improve.
