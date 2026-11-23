---
id: primes-sieve
title: Primes with math.isqrt
topic: The math module
difficulty: medium
lesson: 27
---

## Prompt
Two prime functions:

- `is_prime(n)` checks divisors only up to `math.isqrt(n)`, the integer square root.
- `primes_up_to(n)` returns every prime `<= n` using the **Sieve of Eratosthenes**.

`primes_up_to(20)` is `[2, 3, 5, 7, 11, 13, 17, 19]`. Numbers below 2 are not prime.

## Starter
```python
import math

def is_prime(n):
    pass


def primes_up_to(n):
    pass
```

## Examples
```python
assert is_prime(97) == True
assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
```

## Tests
```python
assert [n for n in range(-3, 12) if is_prime(n)] == [2, 3, 5, 7, 11]
assert is_prime(1) == False
assert is_prime(7919) == True
assert is_prime(7917) == False
assert is_prime(1_000_000_007) == True
assert primes_up_to(1) == []
assert primes_up_to(2) == [2]
assert len(primes_up_to(100_000)) == 9592
```

## Hints
- If `n` has a divisor bigger than its square root, it also has one smaller than it, so checking `range(2, math.isqrt(n) + 1)` is enough.
- Sieve: `is_p = [True] * (n + 1)`, mark 0 and 1 false, and for each `i` up to `isqrt(n)` that's still prime, mark `i*i, i*i+i, ...` false.
- Slice assignment marks multiples fast: `is_p[i*i::i] = [False] * len(range(i*i, n + 1, i))`.

## Solution
```python
import math

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


def primes_up_to(n):
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_p[i]:
            is_p[i * i::i] = [False] * len(range(i * i, n + 1, i))
    return [i for i, p in enumerate(is_p) if p]
```

## Explanation
`math.isqrt` returns an exact integer square root, avoiding float rounding issues with `int(math.sqrt(n))` on big numbers. The sieve runs in O(n log log n), far faster than testing each number. Start crossing off at `i*i` because smaller multiples were already crossed off by smaller primes.
