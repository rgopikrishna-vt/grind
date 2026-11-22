---
id: stats-imports
title: Imports and the standard library
topic: Modules and imports
difficulty: easy
---

## Prompt
Practice the three import styles. At the top of your code:

- `import statistics`
- `from math import sqrt as square_root`
- `from collections import Counter`

Then write `describe(nums)` returning a tuple `(mean, median, mode)` using `statistics.mean`, `statistics.median` and `Counter(...).most_common(1)` for the mode (on ties, the value seen first).

Also write `hypotenuse(a, b)` using `square_root`.

## Starter
```python
# add your three imports here


def describe(nums):
    pass


def hypotenuse(a, b):
    pass
```

## Examples
```python
assert describe([1, 2, 2, 3, 10]) == (3.6, 2, 2)
assert hypotenuse(3, 4) == 5.0
```

## Tests
```python
import math
assert square_root is math.sqrt, "import sqrt as square_root"
assert "statistics" in globals(), "use import statistics"
assert describe([5]) == (5, 5, 5)
assert describe([1, 1, 2, 2]) == (1.5, 1.5, 1)
assert describe([4, 1, 3]) == (8 / 3, 3, 4)
assert hypotenuse(5, 12) == 13.0
```

## Hints
- `import statistics` binds the module; call `statistics.mean(nums)`.
- `from math import sqrt as square_root` binds only that function, under a new name.
- `Counter(nums).most_common(1)` returns `[(value, count)]`, so the mode is `[0][0]`.

## Solution
```python
import statistics
from math import sqrt as square_root
from collections import Counter


def describe(nums):
    mode = Counter(nums).most_common(1)[0][0]
    return statistics.mean(nums), statistics.median(nums), mode


def hypotenuse(a, b):
    return square_root(a * a + b * b)
```

## Explanation
`import x` keeps names namespaced (`statistics.mean`), which is clearer in big files. `from x import y` is shorter for names you use often, and `as` renames to avoid clashes. Avoid `from x import *`: it hides where names come from. A module's code runs once, on first import; later imports reuse it from `sys.modules`.
