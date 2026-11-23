---
id: rank-players
title: Rank players
topic: enumerate, zip and sorted
difficulty: medium
lesson: 15
---

## Prompt
You get two parallel lists: `names` and `scores`. Write `rank(names, scores)` that returns a list of strings like `"1. Ana (95)"`:

- highest score first
- ties broken by name, alphabetically
- numbered from 1

```python
rank(["Bo", "Ana", "Cy"], [80, 95, 80])
# ['1. Ana (95)', '2. Bo (80)', '3. Cy (80)']
```

Use `zip`, `sorted` with a `key=lambda ...`, and `enumerate(..., start=1)`.

## Starter
```python
def rank(names, scores):
    pass
```

## Examples
```python
assert rank(["Bo", "Ana", "Cy"], [80, 95, 80]) == ["1. Ana (95)", "2. Bo (80)", "3. Cy (80)"]
```

## Tests
```python
assert rank([], []) == []
assert rank(["Solo"], [1]) == ["1. Solo (1)"]
assert rank(["d", "c", "b", "a"], [1, 1, 1, 1]) == ["1. a (1)", "2. b (1)", "3. c (1)", "4. d (1)"]
assert rank(["x", "y", "z"], [10, 30, 20]) == ["1. y (30)", "2. z (20)", "3. x (10)"]
assert rank(["Max", "Al"], [-5, 0]) == ["1. Al (0)", "2. Max (-5)"]
```

## Hints
- `zip(names, scores)` pairs them up as `(name, score)` tuples.
- Sort by a tuple key: `key=lambda p: (-p[1], p[0])`. Negating the score sorts it descending while the name stays ascending.
- `for i, (name, score) in enumerate(pairs, start=1):`

## Solution
```python
def rank(names, scores):
    pairs = sorted(zip(names, scores), key=lambda p: (-p[1], p[0]))
    return [f"{i}. {name} ({score})" for i, (name, score) in enumerate(pairs, start=1)]
```

## Explanation
Tuples compare element by element, which makes multi-key sorts easy. Negation works for numbers; for strings you'd sort twice instead, because Python's sort is stable: first by the secondary key, then by the primary key with `reverse=True`.
