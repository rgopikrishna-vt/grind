---
id: lcm-list
title: LCM of a list
topic: The math module
difficulty: easy
---

## Prompt
Write `lcm_all(nums)` that returns the **least common multiple** of a non-empty list of positive integers: the smallest number every element divides evenly.

`lcm_all([4, 6])` is `12`. `lcm_all([2, 3, 4, 5])` is `60`.

Use `math.gcd` and the identity `lcm(a, b) = a * b // gcd(a, b)`. (Python 3.9+ also has `math.lcm`, but write it with `gcd` for practice.)

## Starter
```python
import math

def lcm_all(nums):
    pass
```

## Examples
```python
assert lcm_all([4, 6]) == 12
assert lcm_all([2, 3, 4, 5]) == 60
```

## Tests
```python
assert lcm_all([7]) == 7
assert lcm_all([1, 1, 1]) == 1
assert lcm_all([6, 10, 15]) == 30
assert lcm_all(list(range(1, 11))) == 2520
assert lcm_all([2 ** 20, 3 ** 10]) == 2 ** 20 * 3 ** 10
```

## Hints
- `math.gcd(12, 18)` is `6`.
- Fold the list: start with `result = nums[0]` and combine with each next number.
- `result = result * x // math.gcd(result, x)`. Use `//` so it stays an int.

## Solution
```python
import math

def lcm_all(nums):
    result = nums[0]
    for x in nums[1:]:
        result = result * x // math.gcd(result, x)
    return result
```

## Explanation
Folding a list with a two-argument function is what `functools.reduce` does: `reduce(lambda a, b: a * b // math.gcd(a, b), nums)`. Python ints have arbitrary precision, so there's no overflow to worry about.
