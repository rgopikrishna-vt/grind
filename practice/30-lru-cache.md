---
id: lru-cache
title: LRU cache
topic: The collections module
difficulty: hard
---

## Prompt
Build an `LRUCache(capacity)` class, a very common interview question:

- `get(key)` returns the value, or `-1` if the key is missing. A successful `get` marks the key as **most recently used**.
- `put(key, value)` inserts or updates the key and marks it most recently used. If that pushes the size over `capacity`, evict the **least recently used** key.

Both operations should be O(1). `collections.OrderedDict` has the two methods you need: `move_to_end(key)` and `popitem(last=False)`.

## Starter
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        pass

    def get(self, key):
        pass

    def put(self, key, value):
        pass
```

## Examples
```python
cache = LRUCache(2)
cache.put(1, "one")
cache.put(2, "two")
assert cache.get(1) == "one"
cache.put(3, "three")     # evicts key 2, the least recently used
assert cache.get(2) == -1
```

## Tests
```python
c = LRUCache(2)
c.put("a", 1)
c.put("b", 2)
c.put("a", 10)            # update makes "a" most recent
c.put("c", 3)             # so "b" is evicted
assert c.get("b") == -1
assert c.get("a") == 10
assert c.get("c") == 3
one = LRUCache(1)
one.put(1, 1)
one.put(2, 2)
assert one.get(1) == -1
assert one.get(2) == 2
big = LRUCache(3)
for i in range(5):
    big.put(i, i * i)
assert [big.get(i) for i in range(5)] == [-1, -1, 4, 9, 16]
z = LRUCache(2)
z.put(0, 0)
assert z.get(0) == 0, "a stored 0 is a real value, not a miss"
```

## Hints
- Store `self.capacity` and `self.data = OrderedDict()` in `__init__`. The order of the dict is the usage order: oldest first.
- In `get`: if the key is present, `self.data.move_to_end(key)` and return its value.
- In `put`: set the value, `move_to_end`, then if `len(self.data) > self.capacity`, `self.data.popitem(last=False)` removes the oldest.

## Solution
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)
```

## Explanation
An `OrderedDict` is a hash map plus a doubly linked list, which is the structure interviewers expect you to describe if asked to build it from scratch. For caching function results in real code, use the `@functools.lru_cache(maxsize=...)` decorator.
