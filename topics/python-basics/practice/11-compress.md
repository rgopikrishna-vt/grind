---
id: compress
title: String compression
topic: Strings
difficulty: medium
lesson: 14
---

## Prompt
Write `compress(s)` that run-length encodes a string: each run of the same character becomes the character followed by the run's length.

`compress("aaabccdddd")` returns `"a3b1c2d4"`.

If the compressed string would **not be shorter** than the original, return the original unchanged. So `compress("abc")` returns `"abc"`.

## Starter
```python
def compress(s):
    pass
```

## Examples
```python
assert compress("aaabccdddd") == "a3b1c2d4"
assert compress("abc") == "abc"
```

## Tests
```python
assert compress("") == ""
assert compress("a") == "a"
assert compress("aa") == "aa"
assert compress("aaa") == "a3"
assert compress("aabbcc") == "aabbcc"
assert compress("zzzzzzzzzzzz") == "z12"
assert compress("aaAAaa") == "aaAAaa"
assert compress("aaaAAAaaa") == "a3A3a3"
```

## Hints
- Walk the string keeping the current character and a count. When the character changes, write out the previous run.
- Don't forget to write out the final run after the loop ends.
- Collect pieces in a list and `"".join()` them; repeated `+=` on strings is slower. Then compare lengths.

## Solution
```python
def compress(s):
    if not s:
        return s
    parts = []
    current, count = s[0], 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            parts.append(f"{current}{count}")
            current, count = ch, 1
    parts.append(f"{current}{count}")
    result = "".join(parts)
    return result if len(result) < len(s) else s
```

## Explanation
The forgotten last run is the classic bug here. `itertools.groupby` does the grouping for you: `"".join(f"{k}{len(list(g))}" for k, g in groupby(s))`.
