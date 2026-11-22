---
id: group-anagrams
title: Group anagrams
topic: Dictionaries
difficulty: medium
---

## Prompt
Write `group_anagrams(words)` that groups words that are anagrams of each other (same letters, different order).

Return a list of groups. Inside each group keep the words in their **original order**, and order the groups by where their **first word** appeared.

`group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])` returns `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`.

## Starter
```python
def group_anagrams(words):
    pass
```

## Examples
```python
assert group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

## Tests
```python
assert group_anagrams([]) == []
assert group_anagrams([""]) == [[""]]
assert group_anagrams(["a"]) == [["a"]]
assert group_anagrams(["abc", "bca", "cab", "xyz"]) == [["abc", "bca", "cab"], ["xyz"]]
assert group_anagrams(["ab", "ba", "abc"]) == [["ab", "ba"], ["abc"]]
assert group_anagrams(["listen", "silent", "enlist", "google", "gogole"]) == [["listen", "silent", "enlist"], ["google", "gogole"]]
```

## Hints
- Two words are anagrams exactly when their sorted letters match: `sorted("tea") == sorted("eat")`.
- Lists can't be dict keys, so use `"".join(sorted(word))` or `tuple(sorted(word))` as the key.
- Dicts keep insertion order (Python 3.7+), so `list(groups.values())` is already in first-appearance order.

## Solution
```python
def group_anagrams(words):
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
```

## Explanation
The sorted-letters key costs O(k log k) per word. For lowercase letters you can make it O(k) with a 26-length count tuple. Dict keys must be hashable, which is why a tuple works and a list doesn't.
