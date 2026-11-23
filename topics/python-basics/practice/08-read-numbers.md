---
id: read-numbers
title: Read numbers from input()
topic: Input and f-strings
difficulty: easy
lesson: 5
---

## Prompt
Many coding platforms feed input through `input()`. Write `summarize()` that **reads** from `input()` and **prints**:

- the first line is a count `n`
- the next `n` lines each hold one number (they may be floats)
- print `Total: X` and then `Average: Y`, both with 2 decimal places

With input `3`, `4`, `5`, `6` it prints:

```
Total: 15.00
Average: 5.00
```

If `n` is 0, print `Total: 0.00` and `Average: 0.00`. In the Try it cell you can't type into `input()`, so test it with the Scratchpad's stdin box or press Submit.

## Starter
```python
def summarize():
    n = int(input())
    # read n more lines, then print the two results
```

## Examples
```python
import io, sys, contextlib

def captured(fn, *args, stdin=""):
    """Run fn(*args) and return everything it printed."""
    old = sys.stdin
    sys.stdin = io.StringIO(stdin)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn(*args)
    finally:
        sys.stdin = old
    return buf.getvalue()

assert captured(summarize, stdin="3\n4\n5\n6\n") == "Total: 15.00\nAverage: 5.00\n"
```

## Tests
```python
assert captured(summarize, stdin="0\n") == "Total: 0.00\nAverage: 0.00\n"
assert captured(summarize, stdin="1\n2.5\n") == "Total: 2.50\nAverage: 2.50\n"
assert captured(summarize, stdin="2\n 10 \n-4\n") == "Total: 6.00\nAverage: 3.00\n"
assert captured(summarize, stdin="3\n1\n1\n2\n") == "Total: 4.00\nAverage: 1.33\n"
```

## Hints
- `input()` returns a string without the newline. Convert with `float(input())`; `float` ignores surrounding spaces.
- `total = sum(float(input()) for _ in range(n))` reads exactly `n` lines.
- Guard the average: `total / n if n else 0`. Format with `f"{total:.2f}"`.

## Solution
```python
def summarize():
    n = int(input())
    total = sum(float(input()) for _ in range(n))
    average = total / n if n else 0
    print(f"Total: {total:.2f}")
    print(f"Average: {average:.2f}")
```

## Explanation
`input()` always returns a `str`, so convert explicitly. When reading lots of input in timed contests, `sys.stdin.readline` or `sys.stdin.read().split()` is much faster than repeated `input()` calls.
