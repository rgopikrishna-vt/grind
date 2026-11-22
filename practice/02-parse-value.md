---
id: parse-value
title: Parse a value
topic: Variables and types
difficulty: easy
---

## Prompt
Write `parse_value(text)` that turns a string into the most specific Python value:

- `"42"` and `"-7"` become `int`
- `"3.14"` and `"1e3"` become `float`
- `"True"` / `"False"` become `bool`
- `"None"` becomes `None`
- anything else is returned as a string, with surrounding spaces stripped

Also write `count_falsy(values)` that returns how many values in a list are **falsy** (`0`, `0.0`, `""`, `[]`, `{}`, `None`, `False`, ...).

## Starter
```python
def parse_value(text):
    pass


def count_falsy(values):
    pass
```

## Examples
```python
assert parse_value("42") == 42
assert count_falsy([0, 1, "", "a", None]) == 3
```

## Tests
```python
assert type(parse_value("42")) is int
assert parse_value(" -7 ") == -7
assert type(parse_value("3.14")) is float and parse_value("3.14") == 3.14
assert parse_value("1e3") == 1000.0 and type(parse_value("1e3")) is float
assert parse_value("True") is True
assert parse_value("False") is False
assert parse_value("None") is None
assert parse_value("  hello ") == "hello"
assert parse_value("12abc") == "12abc"
assert count_falsy([]) == 0
assert count_falsy([0.0, [], {}, set(), False, "0", [0]]) == 5
```

## Hints
- Strip first: `text = text.strip()`.
- Check the special words (`True`, `False`, `None`) before trying numbers.
- Try `int(text)` inside `try:` / `except ValueError:`, then `float(text)`, then fall back to the string. `bool(x)` tells you whether a value is truthy.

## Solution
```python
def parse_value(text):
    text = text.strip()
    specials = {"True": True, "False": False, "None": None}
    if text in specials:
        return specials[text]
    for convert in (int, float):
        try:
            return convert(text)
        except ValueError:
            pass
    return text


def count_falsy(values):
    return sum(1 for v in values if not v)
```

## Explanation
`bool("False")` is `True`: any non-empty string is truthy, which is why you can't convert with `bool()` here. Note `"0"` and `[0]` are truthy too: only *empty* containers and zero numbers are falsy. Trying a conversion and catching `ValueError` is the idiomatic "easier to ask forgiveness than permission" style.
