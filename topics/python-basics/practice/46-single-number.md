---
id: single-number
title: Single number
topic: Binary and bit operators
difficulty: easy
lesson: 26
---

## Prompt
Every value in `nums` appears **exactly twice** except for one, which appears once. Write `single_number(nums)` that returns that one.

Do it in O(n) time and O(1) extra space using XOR (`^`). Hint: `x ^ x == 0` and `x ^ 0 == x`.

Also write `is_power_of_two(n)` using a bit trick: it should be `True` for 1, 2, 4, 8, ... and `False` for 0 and negatives.

## Starter
```python
def single_number(nums):
    pass


def is_power_of_two(n):
    pass
```

## Examples
```python
assert single_number([4, 1, 2, 1, 2]) == 4
assert is_power_of_two(16) == True
```

## Tests
```python
assert single_number([1]) == 1
assert single_number([2, 2, 1]) == 1
assert single_number([-3, 7, 7]) == -3
assert single_number([0, 5, 5]) == 0
assert is_power_of_two(1) == True
assert is_power_of_two(0) == False
assert is_power_of_two(-8) == False
assert is_power_of_two(6) == False
assert is_power_of_two(2 ** 40) == True
assert is_power_of_two(2 ** 40 + 1) == False
```

## Hints
- XOR everything together; the pairs cancel out to 0, leaving the single value.
- Start with `result = 0` and do `result ^= x` for each `x`.
- A power of two has exactly one bit set, so `n & (n - 1)` clears it to 0. Remember to require `n > 0`.

## Solution
```python
def single_number(nums):
    result = 0
    for x in nums:
        result ^= x
    return result


def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0
```

## Explanation
XOR is commutative and associative, so the order doesn't matter. Other handy tricks: `n & 1` tests for odd, `n >> 1` halves, and `n.bit_count()` (Python 3.10+) or `bin(n).count("1")` counts set bits. Precedence note: in Python `&` binds tighter than `==`, so `n & (n - 1) == 0` means `(n & (n - 1)) == 0`. In C it's the other way round.
