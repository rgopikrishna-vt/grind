---
id: print-formatting
title: print() with sep and end
topic: print() and comments
difficulty: easy
---

## Prompt
`print()` has two keyword arguments people forget: `sep` (what goes **between** the values, default `" "`) and `end` (what goes **after** them, default `"\n"`).

Write two functions that **print** (not return):

- `countdown(n)` prints `n`, `n-1`, ... `1` and then `Go!`, all on **one line** separated by spaces. `countdown(3)` prints `3 2 1 Go!` followed by a newline.
- `print_csv(rows)` prints each row (a list of values) on its own line with the values separated by commas. `print_csv([[1, "a"], [2, "b"]])` prints `1,a` then `2,b`.

Use `sep` and `end` rather than building strings with `+`.

## Starter
```python
def countdown(n):
    # Hint: print(i, end=" ") keeps you on the same line
    pass


def print_csv(rows):
    pass
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

assert captured(countdown, 3) == "3 2 1 Go!\n"
assert captured(print_csv, [[1, "a"], [2, "b"]]) == "1,a\n2,b\n"
```

## Tests
```python
assert captured(countdown, 1) == "1 Go!\n"
assert captured(countdown, 0) == "Go!\n"
assert captured(countdown, 5) == "5 4 3 2 1 Go!\n"
assert captured(print_csv, []) == ""
assert captured(print_csv, [["x"]]) == "x\n"
assert captured(print_csv, [[1.5, None, True]]) == "1.5,None,True\n"
```

## Hints
- `print(i, end=" ")` prints `i` followed by a space instead of a newline.
- After the loop, a plain `print("Go!")` ends the line.
- `print(*row, sep=",")` unpacks the row into separate arguments and puts commas between them.

## Solution
```python
def countdown(n):
    for i in range(n, 0, -1):
        print(i, end=" ")
    print("Go!")


def print_csv(rows):
    for row in rows:
        print(*row, sep=",")
```

## Explanation
`print` converts each argument with `str()`, joins them with `sep`, then writes `end`. `print(*row, sep=",")` is shorter than `",".join(...)` and handles non-string values, because `join` needs strings. Comments start with `#`; there is no block comment, but an unassigned triple-quoted string is often used as one (and as a docstring right after a `def`).
