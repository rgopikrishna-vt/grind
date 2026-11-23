---
id: employee-records
title: namedtuple and defaultdict
topic: The collections module
difficulty: medium
lesson: 23
---

## Prompt
You get rows of `(name, department, salary)`.

1. Define `Employee` as a `namedtuple` with fields `name`, `dept`, `salary`.
2. `by_department(rows)` returns a dict mapping each department to the **sorted** list of names in it. Build it with `defaultdict(list)`, and return a plain `dict`.
3. `top_earner(rows)` returns the `Employee` with the highest salary (first one on ties), or `None` for no rows.

## Starter
```python
from collections import namedtuple, defaultdict

Employee = None  # replace with a namedtuple


def by_department(rows):
    pass


def top_earner(rows):
    pass
```

## Examples
```python
rows = [("Ana", "eng", 120), ("Bo", "ops", 90), ("Cy", "eng", 100)]
assert by_department(rows) == {"eng": ["Ana", "Cy"], "ops": ["Bo"]}
assert top_earner(rows) == Employee("Ana", "eng", 120)
```

## Tests
```python
assert Employee._fields == ("name", "dept", "salary")
e = top_earner([("Zed", "x", 5), ("Amy", "y", 5)])
assert e.name == "Zed" and e.salary == 5
assert isinstance(e, tuple)
assert top_earner([]) is None
assert by_department([]) == {}
assert type(by_department([("a", "d", 1)])) is dict
assert by_department([("b", "d", 1), ("a", "d", 2)]) == {"d": ["a", "b"]}
```

## Hints
- `Employee = namedtuple("Employee", ["name", "dept", "salary"])`.
- `groups = defaultdict(list)` then `groups[dept].append(name)`: no `KeyError` on new keys.
- `max(employees, key=lambda e: e.salary)` returns the first maximum on ties; `Employee(*row)` builds one from a tuple.

## Solution
```python
from collections import namedtuple, defaultdict

Employee = namedtuple("Employee", ["name", "dept", "salary"])


def by_department(rows):
    groups = defaultdict(list)
    for name, dept, _ in rows:
        groups[dept].append(name)
    return {dept: sorted(names) for dept, names in groups.items()}


def top_earner(rows):
    if not rows:
        return None
    return max((Employee(*r) for r in rows), key=lambda e: e.salary)
```

## Explanation
A `namedtuple` is a tuple with field names: immutable, lightweight, and readable (`e.salary` instead of `e[2]`). `defaultdict(list)` calls `list()` to create a value the first time a key is used. For mutable records with defaults, `@dataclass` is the modern alternative.
