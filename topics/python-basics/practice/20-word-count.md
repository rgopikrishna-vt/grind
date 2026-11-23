---
id: word-count
title: Word frequency
topic: Dictionaries
difficulty: easy
lesson: 9
---

## Prompt
Write `word_count(text)` that returns a dict mapping each word to how many times it appears. Words are compared **case-insensitively** and should be stored lowercase. Strip these punctuation characters from the ends of each word: `.,!?;:"'`

`word_count("The cat. The hat!")` returns `{"the": 2, "cat": 1, "hat": 1}`.

## Starter
```python
def word_count(text):
    counts = {}
    # your code here
    return counts
```

## Examples
```python
assert word_count("The cat. The hat!") == {"the": 2, "cat": 1, "hat": 1}
```

## Tests
```python
assert word_count("") == {}
assert word_count("a A a") == {"a": 3}
assert word_count("Hello, hello? HELLO!") == {"hello": 3}
assert word_count("one two  three\ntwo") == {"one": 1, "two": 2, "three": 1}
assert word_count("\"Quoted\" words; and: more.") == {"quoted": 1, "words": 1, "and": 1, "more": 1}
assert word_count("don't stop") == {"don't": 1, "stop": 1}
```

## Hints
- `text.lower().split()` gives you lowercase words.
- `word.strip(".,!?;:\"'")` removes those characters from both ends only.
- `counts[w] = counts.get(w, 0) + 1`, and skip words that become empty after stripping.

## Solution
```python
def word_count(text):
    counts = {}
    for word in text.lower().split():
        word = word.strip(".,!?;:\"'")
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts
```

## Explanation
`dict.get(key, default)` avoids a `KeyError` for new keys. `collections.defaultdict(int)` and `collections.Counter` are the idiomatic shortcuts; `Counter(words).most_common(3)` gives the top three.
