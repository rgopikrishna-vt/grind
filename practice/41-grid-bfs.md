---
id: grid-bfs
title: Shortest path in a grid (BFS)
topic: The collections module
difficulty: hard
---

## Prompt
A grid is a list of strings: `.` is open, `#` is a wall. Starting at the top-left and moving up, down, left or right, return the **fewest steps** to reach the bottom-right, or `-1` if it can't be reached (also `-1` if the start or end is a wall).

```python
shortest_path(["..#",
               "#..",
               "..."])   # 4
```

Use breadth-first search with `collections.deque` as the queue. BFS explores in order of distance, so the first time you reach the goal is the shortest route.

## Starter
```python
from collections import deque

def shortest_path(grid):
    pass
```

## Examples
```python
assert shortest_path(["..#", "#..", "..."]) == 4
assert shortest_path([".#", "#."]) == -1
```

## Tests
```python
assert shortest_path(["."]) == 0
assert shortest_path(["#"]) == -1
assert shortest_path(["..", ".#"]) == -1
assert shortest_path(["....", "###.", "....", ".###", "...."]) == 13
assert shortest_path([".....", ".###.", ".#...", ".#.#.", "...#."]) == 8
big = ["." * 60] * 60
assert shortest_path(big) == 118
```

## Hints
- Queue items are `(row, col, steps)`. Start with `deque([(0, 0, 0)])` and a `seen` set containing `(0, 0)`.
- Pop from the left with `popleft()` (O(1); `list.pop(0)` is O(n)). For each of the 4 neighbours inside the grid, open and not seen, add it to `seen` and append it.
- Mark cells as seen when you *enqueue* them, not when you pop them, or the same cell gets queued many times.

## Solution
```python
from collections import deque

def shortest_path(grid):
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == "#" or grid[-1][-1] == "#":
        return -1
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        r, c, steps = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return steps
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc, steps + 1))
    return -1
```

## Explanation
BFS with a deque is the go-to for shortest paths on unweighted graphs (grids, word ladders, knight moves). With weighted edges you'd switch to Dijkstra, which replaces the deque with a `heapq` priority queue. Python's chained comparison `0 <= nr < rows` keeps the bounds check readable.
