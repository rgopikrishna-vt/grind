---
id: fizzbuzz
title: FizzBuzz
topic: Loops and conditionals
difficulty: easy
lesson: 11
---

## Prompt
The classic warm-up. Write `fizzbuzz(n)` that returns a **list of strings** for the numbers 1 to `n`:

- `"Fizz"` if the number is divisible by 3
- `"Buzz"` if it is divisible by 5
- `"FizzBuzz"` if it is divisible by both
- otherwise the number itself, as a string

Return the list. Don't print it.

## Starter
```python
def fizzbuzz(n):
    result = []
    # your code here
    return result
```

## Examples
```python
assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
assert fizzbuzz(15)[-1] == "FizzBuzz"
```

## Tests
```python
assert fizzbuzz(1) == ["1"]
assert fizzbuzz(0) == []
assert fizzbuzz(15) == ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
assert fizzbuzz(30)[29] == "FizzBuzz"
assert fizzbuzz(100).count("FizzBuzz") == 6
```

## Hints
- Loop with `for i in range(1, n + 1):`. The `+ 1` matters because `range` stops before its end.
- Check divisibility with `i % 3 == 0`.
- Test the *both* case (`i % 15 == 0`) first. Otherwise the `% 3` branch catches 15 before you get there.

## Solution
```python
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
```

## Explanation
Order matters in an `if`/`elif` chain: the first true branch wins, so the most specific case (divisible by 15) must come first. A neat alternative builds the word: `s = "Fizz" * (i % 3 == 0) + "Buzz" * (i % 5 == 0)`, then `s or str(i)`.
