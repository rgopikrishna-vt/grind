---
id: closest-points
title: Closest points
topic: Tuples
difficulty: medium
---

## Prompt
Points are `(x, y)` tuples. Write `closest(points, k)` that returns the `k` points closest to the origin `(0, 0)`, nearest first. Break ties by `x`, then by `y` (so compare `(distance², x, y)`).

```python
closest([(3, 3), (1, 2), (-2, 1), (0, 5)], 2)   # [(-2, 1), (1, 2)]
```

Tuples compare element by element, which makes this a one-line sort key. Don't use `math.sqrt`: comparing squared distances gives the same order.

## Starter
```python
def closest(points, k):
    pass
```

## Examples
```python
assert closest([(3, 3), (1, 2), (-2, 1), (0, 5)], 2) == [(-2, 1), (1, 2)]
```

## Tests
```python
assert closest([], 3) == []
assert closest([(1, 1)], 5) == [(1, 1)]
assert closest([(0, 0), (5, 5)], 1) == [(0, 0)]
assert closest([(1, 0), (0, 1), (-1, 0), (0, -1)], 4) == [(-1, 0), (0, -1), (0, 1), (1, 0)]
assert closest([(2, 2), (-3, 0), (1, -1)], 0) == []
pts = [(1, 2)]
closest(pts, 1)
assert pts == [(1, 2)]
```

## Hints
- Unpack inside the key: `key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0], p[1])`.
- `sorted(...)` returns a new list and leaves `points` alone; slicing `[:k]` is safe even when `k` is larger than the list.

## Solution
```python
def closest(points, k):
    return sorted(points, key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0], p[1]))[:k]
```

## Explanation
Tuple comparison is lexicographic: `(1, 5) < (2, 0)` because the first elements decide. That's why returning a tuple from a sort key gives you multi-level ordering for free. For huge inputs with small `k`, `heapq.nsmallest(k, points, key=...)` is O(n log k).
