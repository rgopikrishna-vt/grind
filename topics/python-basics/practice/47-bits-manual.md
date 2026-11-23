---
id: bits-manual
title: Count bits and binary strings
topic: Binary and bit operators
difficulty: easy
lesson: 26
---

## Prompt
Without using `bin()`, `format()` or `int.bit_count()`:

- `count_ones(n)` returns how many `1` bits the non-negative integer `n` has. `count_ones(13)` is 3, since 13 is `1101`.
- `to_binary(n)` returns the binary digits as a string. `to_binary(13)` is `"1101"`, and `to_binary(0)` is `"0"`.

Use `&`, `>>` and `%`/`//`.

## Starter
```python
def count_ones(n):
    pass


def to_binary(n):
    pass
```

## Examples
```python
assert count_ones(13) == 3
assert to_binary(13) == "1101"
```

## Tests
```python
assert count_ones(0) == 0
assert count_ones(1) == 1
assert count_ones(255) == 8
assert count_ones(2 ** 50) == 1
assert to_binary(0) == "0"
assert to_binary(1) == "1"
assert to_binary(8) == "1000"
assert to_binary(1023) == "1" * 10
assert all(to_binary(i) == bin(i)[2:] for i in range(300))
```

## Hints
- `n & 1` is the lowest bit; `n >>= 1` shifts the number right, dropping that bit.
- Repeat while `n` is non-zero, adding up the lowest bits.
- For the string, collect `str(n & 1)` each time, then reverse at the end. Handle `0` separately.

## Solution
```python
def count_ones(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def to_binary(n):
    if n == 0:
        return "0"
    digits = []
    while n:
        digits.append(str(n & 1))
        n >>= 1
    return "".join(reversed(digits))
```

## Explanation
Brian Kernighan's trick is faster for sparse numbers: `n &= n - 1` clears the lowest set bit, so the loop runs once per `1` bit. In normal code just use `n.bit_count()` and `bin(n)` or `f"{n:b}"`.
