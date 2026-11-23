---
id: typed-inventory
title: Add type hints
topic: Type hints
difficulty: easy
lesson: 21
---

## Prompt
Write `restock(inventory, deliveries)` **with type hints**:

- `inventory` is a `dict[str, int]` of item → quantity
- `deliveries` is a `list[tuple[str, int]]` of `(item, amount)` pairs
- it returns a **new** `dict[str, int]` with the deliveries added (new items appear too), leaving `inventory` unchanged

The tests check the annotations, so write them exactly as: `inventory: dict[str, int]`, `deliveries: list[tuple[str, int]]`, and `-> dict[str, int]`.

Remember: Python does not enforce hints at runtime. They are for readers and tools like mypy.

## Starter
```python
def restock(inventory, deliveries):
    pass
```

## Examples
```python
assert restock({"apple": 2}, [("apple", 3), ("pear", 1)]) == {"apple": 5, "pear": 1}
```

## Tests
```python
hints = restock.__annotations__
assert hints.get("inventory") == dict[str, int], "annotate inventory: dict[str, int]"
assert hints.get("deliveries") == list[tuple[str, int]], "annotate deliveries: list[tuple[str, int]]"
assert hints.get("return") == dict[str, int], "annotate the return type: -> dict[str, int]"
stock = {"a": 1}
assert restock(stock, []) == {"a": 1}
assert restock(stock, [("a", 2), ("a", 3)]) == {"a": 6}
assert stock == {"a": 1}
assert restock({}, [("x", 0)]) == {"x": 0}
```

## Hints
- Hints go after parameter names with a colon, and the return type after `->`: `def f(x: int) -> str:`.
- Since Python 3.9 you can write `dict[str, int]` and `list[tuple[str, int]]` without importing anything from `typing`.
- Copy first with `result = dict(inventory)`, then add with `result[item] = result.get(item, 0) + amount`.

## Solution
```python
def restock(inventory: dict[str, int], deliveries: list[tuple[str, int]]) -> dict[str, int]:
    result = dict(inventory)
    for item, amount in deliveries:
        result[item] = result.get(item, 0) + amount
    return result
```

## Explanation
Hints are stored in `__annotations__` and otherwise ignored at runtime: `restock("oops", 5)` would still run until it hits an error. Older code uses `Dict[str, int]` and `List[...]` from `typing`; modern code uses the built-in generics. `Optional[int]` is written `int | None` in 3.10+.
