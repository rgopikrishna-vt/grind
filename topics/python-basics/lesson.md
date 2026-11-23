# Python Basics for Beginners — From Zero to the Concepts Refresher

This is the on-ramp. It assumes **no prior Python knowledge** — if you've never written a line of code, start here. Each section builds only on what came before it, in order. Don't skip ahead; nearly every later section leans on something from an earlier one.

**How this fits together — your three-stop journey:**
1. **This file** — learn Python itself, from scratch, in order.
2. **[Python Concepts Refresher.md](Python%20Concepts%20Refresher.md)** — the same concepts you'll meet here, but shown inside real interview solutions, with frequency counts from the actual problem set.
3. **[NeetCode 250 Solutions.md](NeetCode%20250%20Solutions.md)** — the 250 problems themselves, your actual goal.

Every major topic in this file ends with a note pointing to where it reappears in the Concepts Refresher, so you always know how what you just learned will get used.

**How to use it:** type every example yourself in a real Python interpreter — don't just read it. Install Python (python.org) or use an online one (replit.com, or just run `python3` in a terminal if you're on Mac/Linux) and follow along live. Predict the output before you run each snippet; being wrong and finding out why is how this actually sticks.

---

## Table of Contents

1. [What Is Python, and How Do You Run It](#1-what-is-python-and-how-do-you-run-it)
2. [Your First Program: `print()` and Comments](#2-your-first-program-print-and-comments)
3. [Variables and Basic Types](#3-variables-and-basic-types)
4. [Operators](#4-operators)
5. [Getting Input, and f-strings](#5-getting-input-and-f-strings)
6. [Strings, Part 1: The Basics](#6-strings-part-1-the-basics)
7. [Lists](#7-lists)
8. [Tuples](#8-tuples)
9. [Dictionaries](#9-dictionaries)
10. [Sets](#10-sets)
11. [Conditionals: `if` / `elif` / `else`](#11-conditionals-if--elif--else)
12. [Loops: `while` and `for`](#12-loops-while-and-for)
13. [Functions](#13-functions)
14. [Strings, Part 2: Slicing and More Methods](#14-strings-part-2-slicing-and-more-methods)
15. [`enumerate`, `zip`, and `sorted`](#15-enumerate-zip-and-sorted)
16. [Ternary Expressions and `lambda`](#16-ternary-expressions-and-lambda)
17. [Comprehensions and Generator Expressions](#17-comprehensions-and-generator-expressions)
18. [Scope, Closures, and `nonlocal`](#18-scope-closures-and-nonlocal)
19. [Recursion](#19-recursion)
20. [Classes and Objects](#20-classes-and-objects)
21. [Type Hints](#21-type-hints)
22. [Modules and Imports](#22-modules-and-imports)
23. [The `collections` Module](#23-the-collections-module)
24. [The `heapq` Module](#24-the-heapq-module)
25. [The `bisect` Module](#25-the-bisect-module)
26. [Numbers in Binary and Bit Operators](#26-numbers-in-binary-and-bit-operators)
27. [The `math` Module](#27-the-math-module)
28. [NumPy Basics](#28-numpy-basics)
29. [Time and Space Complexity Cheat Sheet](#29-time-and-space-complexity-cheat-sheet)
30. [Gotchas Every Python Beginner Hits](#30-gotchas-every-python-beginner-hits)
31. [Where To Go From Here](#31-where-to-go-from-here)

---

## 1. What Is Python, and How Do You Run It

A program is just a list of instructions a computer follows, in order, one at a time. Python is a **language** for writing those instructions in a form that's readable by humans and translatable by a computer.

Python code lives in plain text files ending in `.py`. You run one of two ways:

- **A script**: save code in `hello.py`, then run `python3 hello.py` in a terminal. The whole file runs top to bottom.
- **The interactive interpreter (REPL)**: type `python3` in a terminal with no filename, and you get a prompt (`>>>`) where you type one line at a time and see the result immediately. Great for experimenting.

Python doesn't need a separate "compile" step like Java or C++ — you write it, you run it, and Python translates it to something the machine understands as it goes.

---

## 2. Your First Program: `print()` and Comments

`print()` is a **function** — a reusable chunk of behavior with a name, that you "call" by writing its name followed by parentheses. `print()` displays whatever you put inside its parentheses.

```python
print("Hello, world!")
# Hello, world!
```

Anything after a `#` on a line is a **comment** — Python ignores it completely. Comments are notes to humans, not instructions to the computer.

```python
# This whole line is ignored by Python.
print("This line actually runs.")  # so is this part, after the #
```

You can print multiple things at once, separated by commas — `print` automatically puts a space between them:

```python
print("The answer is", 42)
# The answer is 42
```

---

## 3. Variables and Basic Types

A **variable** is a name that points at a value. You create one with `=` (assignment — this is not mathematical equality, it's "store this value under this name"):

```python
age = 27
name = "Gopi"
is_hired = False
```

Python figures out the **type** of a value automatically — you never declare it up front (this is called "dynamic typing"). The core built-in types you'll use constantly:

```python
age = 27            # int — a whole number
price = 19.99        # float — a number with a decimal point
name = "Gopi"         # str — text, always in quotes (single or double, doesn't matter which)
is_hired = False       # bool — exactly True or False (capitalized, no quotes)
nothing = None          # None — Python's "no value / nothing here" marker
```

Check any value's type with the `type()` function:
```python
print(type(age))       # <class 'int'>
print(type(name))      # <class 'str'>
```

Variable names: start with a letter or underscore, contain letters/digits/underscores, no spaces, and by convention use `snake_case` (lowercase words joined by underscores) — `total_score`, not `TotalScore` or `totalScore`. Names are case-sensitive: `age` and `Age` are two different variables.

You can reassign a variable to a completely different type at any time — Python doesn't stop you:
```python
x = 5
x = "now I'm a string"   # perfectly legal, just confusing if overused
```

### Truthiness

Every value in Python is "truthy" or "falsy" when used where a `True`/`False` is expected (you'll see this matter a lot once we hit `if` statements). The falsy values worth memorizing: `False`, `None`, `0`, `0.0`, `""` (empty string), `[]` (empty list), `{}` (empty dict), `set()` (empty set). Everything else is truthy — including, notably, the string `"False"` (a non-empty string is always truthy, regardless of what it says).

> **Where this goes next:** the `type()` function is step one toward [type hints](#21-type-hints), where you'll start writing down a value's expected type up front instead of checking it after the fact.

---

## 4. Operators

**Arithmetic:**
```python
7 + 3    # 10  addition
7 - 3    # 4   subtraction
7 * 3    # 21  multiplication
7 / 3    # 2.333...  division — ALWAYS returns a float, even if it divides evenly
7 // 3   # 2   floor division — rounds DOWN to the nearest whole number, returns an int
7 % 3    # 1   modulo — the remainder after division
7 ** 3   # 343 exponent — 7 to the power of 3
```

**Comparison** (always produce a `bool`):
```python
5 == 5    # True   — equality (note: TWO equals signs; one = is assignment, not comparison)
5 != 3    # True   — not equal
5 > 3     # True
5 < 3     # False
5 >= 5    # True
```

**Logical** (combine `bool` values):
```python
True and False   # False — both sides must be True
True or False    # True  — at least one side must be True
not True         # False — flips it
```

**Assignment shortcuts** (augmented assignment) — these modify a variable using its own current value:
```python
x = 5
x += 1   # same as x = x + 1  -> x is now 6
x -= 2   # x is now 4
x *= 3   # x is now 12
```

> **Where this goes next:** floor division (`//`) behaves surprisingly with negative numbers — covered properly in [Gotchas](#30-gotchas-every-python-beginner-hits) once you've seen enough Python to appreciate why it matters. The comparison and logical operators here are exactly what drives every `if` statement in [section 11](#11-conditionals-if--elif--else).

---

## 5. Getting Input, and f-strings

`input()` pauses your program, waits for the user to type something and press Enter, and returns what they typed — **always as a string**, even if they typed a number:

```python
name = input("What's your name? ")
print("Hello, " + name)
```

To combine text and variables cleanly, use an **f-string** — put `f` right before the opening quote, and anything inside `{}` gets evaluated and inserted:

```python
name = "Gopi"
age = 27
print(f"{name} is {age} years old")
# Gopi is 27 years old
print(f"Next year: {age + 1}")   # you can put any expression inside {}, not just a variable
# Next year: 28
```

This is almost always nicer than gluing strings together with `+`, which only works between strings and requires you to manually convert numbers with `str(...)` first.

---

## 6. Strings, Part 1: The Basics

A string is a sequence of characters, written in quotes. Strings are **immutable** — once created, a string can never be changed in place; every operation that looks like it modifies a string actually builds a brand-new one. (This becomes important later — see [Gotchas](#30-gotchas-every-python-beginner-hits).)

```python
s = "hello"
len(s)          # 5 — the number of characters
s[0]            # 'h' — indexing: square brackets + a position, starting at 0
s[4]            # 'o' — the last character of a 5-character string is index 4, not 5
s[-1]           # 'o' — negative indices count from the end: -1 is the last character
s.upper()       # 'HELLO'
s.lower()       # 'hello'
s + " world"    # 'hello world' — concatenation
```

**Indices start at 0, not 1** — this trips up every beginner at least once. `s[0]` is the first character.

Trying to access an index that doesn't exist raises an error:
```python
s[10]   # IndexError: string index out of range
```

> **Where this goes next:** real `[a:b]` slicing (grabbing a *range* of characters at once) needs indexing as a foundation — that's [section 14](#14-strings-part-2-slicing-and-more-methods). This section's basics are also exactly what shows up as "String Idioms" in the Concepts Refresher.

---

## 7. Lists

A list holds an ordered, **mutable** (changeable) collection of values, in square brackets:

```python
nums = [3, 1, 4, 1, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "two", 3.0, True]   # a list can hold different types at once
empty = []
```

Indexing and `len()` work exactly like strings:
```python
fruits[0]     # 'apple'
fruits[-1]    # 'cherry'
len(fruits)   # 3
```

Unlike strings, lists are mutable — you can change an element in place:
```python
fruits[0] = "avocado"
print(fruits)   # ['avocado', 'banana', 'cherry']
```

Common operations:
```python
fruits.append("date")       # adds to the end: ['avocado', 'banana', 'cherry', 'date']
fruits.pop()                 # removes and returns the LAST element: 'date'
fruits.pop(0)                  # removes and returns the element AT index 0: 'avocado'
fruits.insert(1, "fig")          # inserts "fig" at index 1
fruits.remove("banana")           # removes the first "banana" it finds, by VALUE not index
3 in [1, 2, 3]                      # True — membership test, works on any index 0..len-1
sorted([3, 1, 2])                     # [1, 2, 3] — returns a NEW sorted list
[1, 2] + [3, 4]                         # [1, 2, 3, 4] — concatenation, like strings
[0] * 5                                   # [0, 0, 0, 0, 0] — repetition
```

`list.sort()` vs `sorted(list)`: `.sort()` sorts the list **in place** and returns `None`; `sorted(...)` returns a brand-new sorted list and leaves the original untouched. This distinction matters — more on it in [section 15](#15-enumerate-zip-and-sorted).

> **Where this goes next:** lists are the backbone of nearly every algorithm you'll write. List comprehensions ([section 17](#17-comprehensions-and-generator-expressions)) are a faster way to *build* a list from a loop.

---

## 8. Tuples

A tuple looks like a list but uses parentheses, and is **immutable** — once created, you can't change, add, or remove elements:

```python
point = (3, 4)
point[0]        # 3 — indexing works just like a list
point[0] = 99   # TypeError: 'tuple' object does not support item assignment
```

Why have both? Because immutability buys you something specific: **tuples can be used as dictionary keys or stored in a set, and lists cannot** (you'll see exactly why once dictionaries are introduced in the next section — it's because dict keys must be "hashable," and only immutable things are). Tuples are also the natural fit for "a fixed-size group of values that belong together," like a coordinate pair.

A one-element tuple needs a trailing comma, or Python just treats it as a regular value in parentheses:
```python
not_a_tuple = (5)     # this is just the int 5
a_tuple = (5,)          # this IS a tuple with one element — the comma is what matters, not the parens
```

**Multiple assignment / unpacking** works with both tuples and lists, and is used constantly:
```python
x, y = 3, 4            # x is 3, y is 4 — this is actually unpacking an implicit tuple (3, 4)
a, b = b, a              # the classic swap — the right side builds a tuple BEFORE any assignment happens
```

### How a tuple itself gets hashed

Indexing into a tuple (`t[0]`) is plain positional lookup — same O(1) contiguous-memory trick as a list, nothing to do with hashing. Separately, though, a tuple **as a whole** is hashable (assuming everything inside it is) — `hash(my_tuple)` combines the hashes of all its elements into one single number, which is what lets a tuple be *used as* a dict key or set element:

```python
hash((1, 2))             # one combined int, derived from hash(1) and hash(2) together
d = {(1, 2): "point A"}    # the tuple (1, 2) is being hashed HERE, to act as a dict key
```

This is exactly why tuples are hashable and lists aren't: a list's contents can change after the fact, which would silently change its hash and break a dict/set's ability to ever find it again. A tuple's contents are frozen, so its hash is guaranteed stable for its whole lifetime — the one hard requirement for anything used as a dict key or set element.

**Catch:** a tuple is only hashable if every element inside it is hashable too. `(1, 2)` hashes fine; `(1, [2, 3])` raises `TypeError: unhashable type: 'list'`, because Python can't compute a stable combined hash when one of the ingredients (a list) could silently change underneath it.

---

## 9. Dictionaries

A dictionary (`dict`) stores **key → value** pairs — think of it as a lookup table. Keys must be unique and must be an immutable type (string, number, or tuple); values can be anything.

```python
ages = {"Gopi": 27, "Alex": 30}
ages["Gopi"]           # 27 — look up by key, not by position
ages["Sam"] = 22         # adds a new key, or overwrites it if "Sam" already existed
"Gopi" in ages            # True — checks if a KEY exists (not a value)
del ages["Alex"]            # removes a key (and its value)
ages.get("Nope")              # None — looking up a missing key with [] raises KeyError, but .get() returns None instead
ages.get("Nope", 0)             # 0 — .get() lets you supply a fallback default as the second argument
```

Looping over a dict:
```python
for key in ages:                    # loops over KEYS by default
    print(key, ages[key])
for key, value in ages.items():       # .items() gives you (key, value) pairs directly — almost always nicer
    print(key, value)
```

Since Python 3.7, dictionaries remember the order keys were inserted — but you should still treat a dict as "a lookup table," not "an ordered list," in how you *use* it.

> **Where this goes next:** `.get()` with a default is the manual version of what `collections.defaultdict` automates for you — see [section 23](#23-the-collections-module). Dict comprehensions (`{k: v for ...}`) are covered in [section 17](#17-comprehensions-and-generator-expressions).

---

## 10. Sets

A set holds **unique, unordered** values — no duplicates allowed, and there's no indexing (no concept of "the first element"):

```python
seen = {1, 2, 3}
seen.add(4)           # {1, 2, 3, 4}
seen.add(2)            # no effect — 2 is already there, sets silently ignore duplicate adds
3 in seen                # True — membership checks on a set are extremely fast
seen.remove(1)             # {2, 3, 4}
```

The empty-set gotcha: `{}` is an empty **dict**, not an empty set — Python reserves `{}` for dicts because dicts came first historically. An empty set needs the constructor: `set()`.

```python
empty_dict = {}
empty_set = set()
```

Sets also support math-style set operations:
```python
{1, 2, 3} | {3, 4, 5}   # {1, 2, 3, 4, 5} — union
{1, 2, 3} & {3, 4, 5}   # {3} — intersection
{1, 2, 3} - {3, 4, 5}   # {1, 2} — difference
```

The most common real use of a set in algorithm code: tracking "have I seen this before?" with O(1) membership checks, instead of scanning a whole list every time.

**How hashing works for a set:** a set is essentially a dict with no values — `hash(element)` decides which internal slot each element lands in, exactly the same mechanism as dict keys (collisions resolved the same way too). Conceptually, `{1, 2, 3}` behaves like `{1: None, 2: None, 3: None}`: the "keys" are just the elements themselves. See [section 8](#8-tuples) for how a tuple gets hashed if you want one as a set element, and the complexity cheat sheet's [dict/set entry](#29-time-and-space-complexity-cheat-sheet) for the full O(1)-average / O(n)-worst-case story.

**Mixed types in one set are fine** — a set doesn't require all elements to be the same type, only that every element is **hashable** (roughly: immutable — numbers, strings, tuples, booleans, `None`):
```python
mixed = {1, "two", 3.0, (4, 5)}   # totally legal
```
Gotcha: `True == 1` and `hash(True) == hash(1)` in Python, so mixing `1` and `True` in the same set collapses them into one element (same for `0`/`False`). And mutable types — lists, dicts, other sets — can't go in a set at all: `{1, [2, 3]}` raises `TypeError: unhashable type: 'list'`.

---

## 11. Conditionals: `if` / `elif` / `else`

```python
age = 20
if age < 13:
    print("child")
elif age < 20:
    print("teenager")
else:
    print("adult")
```

Notes that matter:
- The colon `:` at the end of each line is required.
- **Indentation is not a style choice in Python — it's the syntax.** The indented lines below `if` are the block that runs when the condition is true. Mixing tabs and spaces, or inconsistent indentation, causes an `IndentationError`.
- `elif` is Python's "else if" — you can chain as many as you want. `else` (no condition) catches everything else and is optional.
- Conditions use the comparison/logical operators from [section 4](#4-operators), and rely on truthiness from [section 3](#3-variables-and-basic-types) — `if my_list:` is a common, idiomatic way to check "is this list non-empty," instead of `if len(my_list) > 0:`.

---

## 12. Loops: `while` and `for`

**`while`** repeats as long as a condition stays true:
```python
count = 0
while count < 3:
    print(count)
    count += 1
# prints 0, 1, 2
```
If you forget to update the condition's variable, you get an **infinite loop** — the single most common beginner bug with `while`.

**`for`** iterates over a sequence — a string, list, tuple, dict, or anything else "iterable":
```python
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)

for char in "abc":
    print(char)
```

`range()` generates a sequence of numbers, most often used to loop a fixed number of times or to loop by index:
```python
for i in range(5):          # 0, 1, 2, 3, 4 — stop is EXCLUSIVE
    print(i)
for i in range(2, 5):         # 2, 3, 4 — start, stop
    print(i)
for i in range(10, 0, -2):      # 10, 8, 6, 4, 2 — start, stop, step (counting down)
    print(i)
```

`break` exits a loop immediately; `continue` skips straight to the next iteration:
```python
for n in range(10):
    if n == 5:
        break        # stop the loop entirely once n hits 5
    if n % 2 == 0:
        continue       # skip printing even numbers, but keep looping
    print(n)
```

> **Where this goes next:** `for ... in ...` is the exact syntax reused inside comprehensions ([section 17](#17-comprehensions-and-generator-expressions)) — a comprehension is really just a compact `for` loop that builds a collection.

---

## 13. Functions

A function packages up reusable behavior under a name, with optional **parameters** (inputs) and a **return value** (output):

```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Gopi")   # calling the function — "Gopi" is the ARGUMENT, bound to the PARAMETER `name`
print(result)              # Hello, Gopi!
```

- `def` starts a function definition; the colon and indentation work exactly like `if`/`for`.
- `return` sends a value back to the caller and immediately exits the function. A function with no `return` statement implicitly returns `None`.
- Parameters can have **default values**, making them optional when calling:
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Gopi")               # "Hello, Gopi!"
greet("Gopi", "Hi")            # "Hi, Gopi!"
greet("Gopi", greeting="Hey")     # "Hey, Gopi!" — naming the argument explicitly, order doesn't matter then
```

**Scope**: a variable created *inside* a function only exists inside that function (it's "local") — it disappears once the function returns, and code outside the function can't see it:
```python
def f():
    x = 5   # local to f
    return x

f()
print(x)   # NameError: x is not defined — x only existed inside f
```

> **Where this goes next:** this simple view of scope gets one wrinkle once functions are nested inside other functions — [section 18](#18-scope-closures-and-nonlocal). Functions calling themselves is [section 19](#19-recursion). `lambda` ([section 16](#16-ternary-expressions-and-lambda)) is a shorthand way to write a tiny one-expression function without `def`.

---

## 14. Strings, Part 2: Slicing and More Methods

Now that you know indexing (section 6) and ranges (section 12), **slicing** extends indexing to grab a whole chunk at once: `s[start:stop:step]`. All three are optional, and `stop` is always exclusive (not included).

```python
s = "hello world"
s[0:5]      # 'hello'  — characters at index 0,1,2,3,4
s[6:]        # 'world'  — from index 6 to the end
s[:5]         # 'hello'  — from the start up to (not including) index 5
s[::-1]        # 'dlrow olleh' — step -1 walks backward: the classic "reverse a string" trick
s[::2]          # 'hlowrd'  — every other character
```
Slicing never errors on an out-of-range index (unlike plain `s[10]`) — `s[100:200]` on a short string just returns `""`.

More string methods you'll use constantly:
```python
"  hi  ".strip()        # 'hi' — removes leading/trailing whitespace
"a,b,c".split(",")        # ['a', 'b', 'c'] — string -> list, on a delimiter
"-".join(["a", "b", "c"])    # 'a-b-c' — list -> string, the REVERSE of split, and the right way to build strings in a loop
"hello".replace("l", "L")      # 'heLLo'
"5".isdigit()                    # True — is this string entirely digits?
"abc123".isalnum()                 # True — is this string entirely letters/digits?
ord("a")                             # 97 — character -> its numeric code
chr(97)                                # 'a' — numeric code -> character, the reverse of ord()
```

**Why `"".join(pieces)` beats building a string with `+=` in a loop:** both approaches end up creating a new string — immutability (section 6) is never violated either way. The difference is *how much copying happens along the way* before you get there.

```python
# Slow (quadratic):
result = ""
for word in words:
    result += word
# Fast (linear):
result = "".join(words)
```

With `+=`, every single iteration builds a brand-new string: it copies *everything accumulated so far*, plus the new piece, into a fresh string, then throws the old one away. So word 1 gets copied once, but it gets **re-copied** on every iteration after that — by the time you're done, the first few words have been copied over and over. Summed across `n` iterations, that's roughly `1 + 2 + ... + n` units of copying — `O(n²)`, quadratically slower as the list grows.

`"".join(words)` instead: scans all the pieces once to compute the total final length, allocates **one** buffer of exactly that size, then copies each word into it exactly once. Every character gets copied a single time, total — `O(n)`. One new string comes out either way; `.join()` just reaches it without any repeated re-copying.

---

## 15. `enumerate`, `zip`, and `sorted`

**`enumerate`** gives you both the index and the value while looping — avoids the clunky `for i in range(len(x)): x[i]`:
```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(i, fruit)
# 0 apple
# 1 banana
# 2 cherry
```

**`zip`** walks two (or more) sequences in parallel, pairing them up — stops as soon as the shortest one runs out:
```python
names = ["Gopi", "Alex"]
ages = [27, 30]
for name, age in zip(names, ages):
    print(name, age)
# Gopi 27
# Alex 30
```

**`sorted`** returns a new sorted list, leaving the original untouched (unlike `.sort()`, which sorts a list in place):
```python
nums = [3, 1, 2]
sorted(nums)          # [1, 2, 3] — nums itself is unchanged
nums.sort()             # nums is NOW [1, 2, 3] — modified in place, returns None

sorted(nums, reverse=True)   # [3, 2, 1]
```

The real power is the `key=` argument — a function that's applied to each element *before* comparing, letting you sort by anything:
```python
words = ["banana", "kiwi", "fig"]
sorted(words, key=len)             # ['fig', 'kiwi', 'banana'] — sorted by LENGTH, not alphabetically
```
You'll almost always pair `key=` with a `lambda` — that's next.

---

## 16. Ternary Expressions and `lambda`

A **ternary expression** is a compact `if`/`else` that produces a *value* instead of running a block of statements:
```python
age = 15
status = "adult" if age >= 18 else "minor"
# equivalent to:
if age >= 18:
    status = "adult"
else:
    status = "minor"
```
Use it for a simple "pick one of two values" — if the logic gets more complex than that, write a real `if`/`else` block instead.

A **`lambda`** is a tiny, unnamed function limited to a single expression — no `def`, no multiple lines, no statements like assignment or loops inside it:
```python
square = lambda x: x * x
square(5)   # 25

# equivalent full function:
def square(x):
    return x * x
```
Lambdas exist mainly to be handed to something else as an argument on the spot — most commonly, as the `key=` for `sorted()`:
```python
people = [("Alex", 30), ("Gopi", 27)]
sorted(people, key=lambda person: person[1])   # sort by age (the 2nd element of each tuple)
# [('Gopi', 27), ('Alex', 30)]
```

---

## 17. Comprehensions and Generator Expressions

A **list comprehension** is a compact way to build a new list from a loop, combining a `for` loop and (optionally) an `if` filter into one expression:
```python
squares = [x * x for x in range(5)]
# equivalent to:
squares = []
for x in range(5):
    squares.append(x * x)
# [0, 1, 4, 9, 16]

evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8] — the `if` filters which elements make it in
```

The same pattern works for dicts and sets:
```python
squares_dict = {x: x * x for x in range(5)}    # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
unique_remainders = {x % 3 for x in range(10)}   # {0, 1, 2}
```

A **generator expression** looks almost identical but uses `()` instead of `[]`, and — critically — doesn't build the whole list in memory. It produces values one at a time, lazily, as something asks for the next one:
```python
total = sum(x * x for x in range(1000000))   # no 1,000,000-element list is ever built in memory
```
Rule of thumb: if you're handing the result straight to something like `sum()`, `max()`, `any()`, or `all()` that only needs to look at each value once, use a generator expression (no brackets). If you need the actual list to use repeatedly afterward, use a list comprehension.

---

## 18. Scope, Closures, and `nonlocal`

Section 13 showed that variables inside a function are local to it. Here's the wrinkle: a function can be defined **inside** another function, and the inner function can "see" the outer function's variables — this is called a **closure**.

```python
def make_counter():
    count = 0
    def increment():
        return count + 1   # reading `count` from the OUTER function — this just works
    return increment

counter = make_counter()
print(counter())   # 1
```

Reading an outer variable from inside a nested function works automatically. But **reassigning** one needs the `nonlocal` keyword — without it, Python assumes you're creating a brand-new *local* variable with the same name, not touching the outer one:
```python
def make_counter():
    count = 0
    def increment():
        nonlocal count     # without this line, `count += 1` below would raise an error
        count += 1          # this is REASSIGNMENT, not just reading
        return count
    return increment

counter = make_counter()
print(counter())   # 1
print(counter())   # 2 — count persisted between calls, remembered by the closure
```

Why this matters for algorithms: it's extremely common to write an outer function (the one with the signature you're required to implement) that defines an inner helper function to do the actual recursive work, while the outer function's variable tracks some running answer the helper updates as it goes.

---

## 19. Recursion

A recursive function calls **itself**. Every recursive function needs two parts:
1. A **base case** — a condition where it stops and returns directly, without recursing.
2. A **recursive case** — where it calls itself with an input that's closer to the base case.

```python
def factorial(n):
    if n <= 1:          # base case: factorial(0) and factorial(1) are both 1
        return 1
    return n * factorial(n - 1)   # recursive case: n! = n * (n-1)!

factorial(5)   # 5 * 4 * 3 * 2 * 1 = 120
```

Trace it by hand once to see how it unwinds:
```
factorial(5)
= 5 * factorial(4)
= 5 * (4 * factorial(3))
= 5 * (4 * (3 * factorial(2)))
= 5 * (4 * (3 * (2 * factorial(1))))
= 5 * (4 * (3 * (2 * 1)))
= 120
```

Miss the base case (or never actually reach it) and you get infinite recursion, which Python stops with a `RecursionError` once you hit its default limit of 1000 nested calls.

A classic second example — Fibonacci — also shows why recursion alone can be slow: each call branches into two more calls, so the same sub-problems get recomputed over and over.
```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```
(The fix for that repeated work — caching results you've already computed — is "memoization," which you'll meet properly in the Concepts Refresher's dynamic-programming examples.)

---

## 20. Classes and Objects

A **class** is a blueprint for creating objects that bundle data and behavior together. An **object** (or "instance") is one concrete thing built from that blueprint.

```python
class Dog:
    def __init__(self, name, age):   # __init__ runs automatically when you create a new Dog
        self.name = name                # stores `name` onto THIS instance
        self.age = age

    def bark(self):
        return f"{self.name} says woof!"

my_dog = Dog("Rex", 3)   # creates a new Dog object; __init__ runs with name="Rex", age=3
print(my_dog.name)          # Rex
print(my_dog.bark())           # Rex says woof!
```

Breaking that down:
- `__init__` is the **constructor** — a special method Python calls automatically when you create a new object with `ClassName(...)`. Methods surrounded by double underscores like this are called "dunder" (double-underscore) methods; `__init__` is by far the most common one.
- `self` refers to "this particular instance" — it's always the first parameter of a method, and Python passes it automatically. `my_dog.bark()` is really shorthand for `Dog.bark(my_dog)`.
- `self.name = name` stores the value as an **attribute** on the instance, so it's still there later when you access `my_dog.name`.

A second class can create instances of the first and link them together — this is exactly how linked lists and trees are built:
```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

first = Node(1)
second = Node(2)
first.next = second       # now `first` points to `second`
print(first.next.value)     # 2
```

---

## 21. Type Hints

A type hint is an annotation that documents what type a variable, parameter, or return value is *expected* to be. Python **never enforces** these at runtime — they're purely for humans and tools to read.

```python
def add(a: int, b: int) -> int:
    return a + b
```
Reading this: `a` and `b` are expected to be `int`s, and the function is expected to return an `int`. Nothing stops you from calling `add("x", "y")` — Python will happily try and either succeed or raise its own error, type hints or not.

Collections need a type *inside* square brackets to say what they contain:
```python
def total(nums: list[int]) -> int:
    return sum(nums)
```
`list[int]` (lowercase `list`) works with no import needed, on Python 3.9+. An older, equivalent style uses a capitalized version from the `typing` module, which **does** need an explicit import:
```python
from typing import List

def total(nums: List[int]) -> int:
    return sum(nums)
```
Using `List[int]` without that import raises `NameError: name 'List' is not defined` — a real, easy-to-make mistake, and exactly the one found and fixed in your Solutions.md file.

---

## 22. Modules and Imports

A module is just a `.py` file full of reusable code someone else (or you) wrote. Python ships with a large standard library of built-in modules you can use without installing anything — you just `import` them:

```python
import math
math.sqrt(16)      # 4.0 — using something from the math module via module.name

from math import sqrt
sqrt(16)             # 4.0 — importing ONE specific name directly, so you can skip the "math." prefix

from math import sqrt as square_root   # import with a different local name, if you want
square_root(16)      # 4.0
```

The next several sections cover specific standard-library modules that come up constantly in algorithm code.

---

## 23. The `collections` Module

Three tools from `collections` solve "I need a specialized list/dict" problems that come up constantly.

**`deque`** — a double-ended queue: adding/removing from *either* end is fast (O(1)), unlike a plain list where removing from the front is slow (O(n)):
```python
from collections import deque
dq = deque([1, 2, 3])
dq.append(4)        # [1, 2, 3, 4] — add to the right
dq.appendleft(0)      # [0, 1, 2, 3, 4] — add to the left
dq.pop()               # removes & returns 4, from the right
dq.popleft()             # removes & returns 0, from the left
```
This makes `deque` the standard choice for a queue (first-in-first-out), which is exactly what breadth-first search needs.

**`defaultdict`** — a dict that auto-creates a value for any missing key, instead of raising `KeyError`:
```python
from collections import defaultdict
counts = defaultdict(int)       # missing key -> starts at int(), which is 0
counts["a"] += 1                  # works even though "a" was never set before
counts["a"] += 1
print(counts)                       # {'a': 2}

groups = defaultdict(list)            # missing key -> starts at list(), which is []
groups["fruit"].append("apple")         # works immediately, no need to check "does this key exist yet"
```

**`Counter`** — built specifically for counting things, in one line:
```python
from collections import Counter
count = Counter(["a", "b", "a", "c", "a"])
print(count)                 # Counter({'a': 3, 'b': 1, 'c': 1})
count.most_common(1)            # [('a', 3)] — the most frequent item(s)
```

---

## 24. The `heapq` Module

A **heap** is a data structure that keeps track of the smallest (or largest) item efficiently, even as you keep adding and removing things. Python's `heapq` module turns a regular list into a **min-heap** — the smallest item is always accessible at index `0`.

```python
import heapq
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
heapq.heappop(heap)       # 1 — always removes and returns the current smallest
heapq.heappop(heap)         # 3
```

There's no built-in max-heap. The standard trick: push the **negative** of each value, so the smallest negative number corresponds to the largest real number — negate again when you pop it back out:
```python
nums = [5, 1, 3]
max_heap = [-n for n in nums]
heapq.heapify(max_heap)    # turns an existing list into a valid heap, in place
biggest = -heapq.heappop(max_heap)   # 5
```

Why bother with a heap instead of just calling `max()`/`min()` on a list every time? Because `max()`/`min()` scan the whole list every single call (slow if you do it repeatedly), while a heap keeps the smallest item instantly accessible and only does a small amount of work to maintain that as things change.

---

## 25. The `bisect` Module

If a list is already sorted, `bisect` finds where a value belongs (or would belong) using binary search — much faster than scanning the whole list.

```python
import bisect
nums = [1, 3, 3, 5, 7]
bisect.bisect_left(nums, 3)     # 1 — the LEFTMOST position where 3 could go
bisect.bisect_right(nums, 3)      # 3 — the RIGHTMOST position where 3 could go (past the existing 3s)
bisect.insort(nums, 4)              # inserts 4 into nums, keeping it sorted: [1, 3, 3, 4, 5, 7]
```
Use this whenever you have a sorted sequence and need to find "where does X fit" without writing your own binary-search loop.

---

## 26. Numbers in Binary and Bit Operators

Every integer is stored, under the hood, as a sequence of bits (1s and 0s). `5` in binary is `101`. Bit operators work directly on those bits:

```python
5 & 3    # AND: 101 & 011 = 001 = 1  — a bit is 1 only if BOTH inputs have a 1 there
5 | 3    # OR:  101 | 011 = 111 = 7  — a bit is 1 if EITHER input has a 1 there
5 ^ 3    # XOR: 101 ^ 011 = 110 = 6  — a bit is 1 if the inputs DIFFER there
~5       # NOT: flips every bit — equals -6 in Python (see note below)
5 << 1   # left shift: 101 -> 1010 = 10 — shifting left multiplies by 2 per shift
5 >> 1   # right shift: 101 -> 10 = 2   — shifting right divides by 2 (rounding down) per shift
```

A useful property of XOR: `x ^ x == 0` (anything XOR'd with itself cancels to zero), and `x ^ 0 == x` (XOR with zero changes nothing). This is the whole trick behind the classic "find the one number that appears once while everything else appears twice" problem — XOR every number together, and every pair cancels out, leaving only the lone number.

```python
nums = [4, 1, 2, 1, 2]
result = 0
for n in nums:
    result ^= n
print(result)   # 4
```

**Note on `~`:** in most other languages, integers have a fixed size (commonly 32 bits), so `~` wraps around in a specific, bounded way. Python integers have no fixed size at all — they grow as large as needed — so `~x` in Python always equals `-x - 1`. If you're solving a problem that explicitly simulates 32-bit integer behavior, you'll see solutions apply a mask like `& 0xFFFFFFFF` to force that wraparound manually, because Python itself won't do it for you.

---

## 27. The `math` Module

A few functions you'll reach for constantly:
```python
import math
math.sqrt(16)       # 4.0
math.ceil(4.3)         # 5 — round UP
math.floor(4.7)          # 4 — round DOWN
math.gcd(12, 18)           # 6 — greatest common divisor
```

And one pattern that isn't from `math` at all but is used just as often — `float('inf')` and `float('-inf')` represent infinity, and are the standard "starting point" when you want to track a running minimum or maximum:
```python
best = float('-inf')
for n in [3, 7, 2, 9, 4]:
    if n > best:
        best = n
print(best)   # 9 — starting at -infinity guarantees the very first real comparison wins
```

---

## 28. NumPy Basics

`numpy` is not part of the standard library — it's a third-party package, but it's installed by default on essentially every coding-interview platform (LeetCode, HackerRank, CoderPad, etc.) alongside the standard `math` module, because numeric/array-heavy interview questions lean on it so often. Import convention — everyone writes it this exact way:

```python
import numpy as np
```

### Why NumPy exists: the problem with Python lists for numeric work

A Python `list` can hold anything, and that flexibility costs memory and speed: each element is a separate Python object (with its own type info, reference count, etc.) sitting behind a pointer, so operating on a list means looping in Python, object by object. A NumPy `array` stores elements of **one single type** packed directly in memory, side by side — like a C array — so NumPy can run operations in fast, compiled C loops instead of the Python interpreter looping element-by-element. This is the whole reason NumPy is fast: less flexibility, in exchange for far less overhead per element.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr)            # [1 2 3 4 5]
print(type(arr))       # <class 'numpy.ndarray'> — "n-dimensional array"
print(arr.dtype)         # int64 (or similar) — EVERY element shares this one type
print(arr.shape)          # (5,) — a tuple describing the array's dimensions
```

### Creating arrays

```python
np.array([1, 2, 3])            # from a list
np.array([[1, 2], [3, 4]])       # a 2D array (a "matrix"), from a list of lists
np.zeros(5)                        # array([0., 0., 0., 0., 0.]) — 5 zeros (floats by default)
np.ones((2, 3))                      # a 2x3 array of all 1.0
np.arange(5)                           # array([0, 1, 2, 3, 4]) — like range(), but gives an array
np.arange(2, 10, 2)                      # array([2, 4, 6, 8]) — start, stop (exclusive), step
np.full(5, 7)                              # array([7, 7, 7, 7, 7])
```

### Indexing and slicing — looks like a list, but more powerful

Basic indexing/slicing works exactly like a list (section 7):
```python
arr = np.array([10, 20, 30, 40, 50])
arr[0]        # 10
arr[-1]        # 50
arr[1:3]        # array([20, 30])
```

2D indexing uses one set of brackets with a comma, instead of `list[i][j]`:
```python
grid = np.array([[1, 2, 3], [4, 5, 6]])
grid[0, 1]       # 2 — row 0, column 1
grid[1]            # array([4, 5, 6]) — the whole second row
grid[:, 0]           # array([1, 4]) — every row, column 0 only (the first "column")
```

**Boolean masking** — indexing with a condition instead of a position, extremely common in interview solutions:
```python
arr = np.array([1, 2, 3, 4, 5, 6])
mask = arr > 3            # array([False, False, False, True, True, True])
arr[mask]                   # array([4, 5, 6]) — only the elements where the mask is True
arr[arr % 2 == 0]             # array([2, 4, 6]) — can skip the intermediate variable entirely
```

### Vectorized operations — the actual point of NumPy

A "vectorized" operation applies to every element at once, with no explicit Python loop:
```python
arr = np.array([1, 2, 3, 4])
arr + 10            # array([11, 12, 13, 14]) — adds 10 to every element
arr * 2               # array([2, 4, 6, 8])
arr ** 2                # array([1, 4, 9, 16])

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
a + b                      # array([11, 22, 33]) — element-wise addition, NOT concatenation like a list's `+`
```
Compare that last line to plain lists: `[1, 2, 3] + [10, 20, 30]` gives `[1, 2, 3, 10, 20, 30]` (concatenation — section 7). NumPy's `+` on arrays means something completely different — element-wise math — which is the single most common point of confusion moving from lists to NumPy.

**Vectorized math is a NumPy-only feature — lists, tuples, and sets don't have it.** Those built-in types never redefine `+`/`*`/etc. to mean "element-wise" — they keep their ordinary meanings (concatenation for list/tuple, repetition for `*`, and for `set`, `+` isn't even defined at all):
```python
[1, 2, 3] + [10, 20, 30]      # [1, 2, 3, 10, 20, 30]  -- concatenation, NOT element-wise add
(1, 2, 3) + (10, 20, 30)        # same story, concatenation
{1, 2, 3} + {10, 20, 30}          # TypeError -- '+' isn't defined for set at all
```
To get real element-wise math on data that starts as a list, you have to convert it to a NumPy array first — `np.array(my_list) + np.array(other_list)`. There's no shortcut that works directly on a plain list/tuple/set.

### Aggregate functions

```python
arr = np.array([3, 1, 4, 1, 5, 9])
arr.sum()        # 23
arr.mean()        # 3.833...
arr.max()          # 9
arr.min()           # 1
arr.std()            # standard deviation
np.sort(arr)           # array([1, 1, 3, 4, 5, 9]) — like sorted(), returns a new array
arr.argmax()             # 5 — the INDEX of the max value, not the value itself
```

On a 2D array, pass `axis=` to aggregate along rows or columns instead of the whole thing:
```python
grid = np.array([[1, 2, 3], [4, 5, 6]])
grid.sum()            # 21 — everything
grid.sum(axis=0)        # array([5, 7, 9]) — sum DOWN each column (collapsing rows)
grid.sum(axis=1)          # array([6, 15]) — sum ACROSS each row (collapsing columns)
```
The `axis=` rule that trips everyone up at first: `axis=0` collapses rows (giving you one result per column), `axis=1` collapses columns (giving you one result per row) — it names the axis being *eliminated*, not the one being kept.

### Reshaping

```python
arr = np.arange(6)          # array([0, 1, 2, 3, 4, 5])
arr.reshape(2, 3)              # array([[0, 1, 2], [3, 4, 5]]) — same 6 elements, viewed as 2 rows x 3 cols
arr.reshape(3, 2)                # array([[0, 1], [2, 3], [4, 5]])
grid.flatten()                     # back to a flat 1D array from any shape
```
`reshape` requires the total element count to match (2x3 = 6 = the original length) — `arr.reshape(2, 4)` on a 6-element array raises an error.

### Converting back to a plain Python list

```python
arr = np.array([1, 2, 3])
arr.tolist()     # [1, 2, 3] — a real Python list, not a NumPy array
```
Interview functions are usually required to `return` a plain `list` (or `int`/`float`), not an `ndarray` — forgetting `.tolist()` at the end is a common, easy mistake when you've done the actual computation in NumPy.

> **When to actually reach for NumPy in an interview:** almost all NeetCode-style problems (arrays, strings, trees, graphs) are solved with plain Python lists/dicts/sets — NumPy rarely helps there, and some interview platforms disable it specifically to force you to demonstrate manual algorithm skills (writing your own loop, your own binary search) rather than delegating to a library. NumPy earns its place when a problem is **explicitly numeric/matrix-shaped** — image/grid processing, matrix multiplication, statistics over a dataset, vectorized math across large arrays — where looping in plain Python would be both slower and more verbose. If a prompt doesn't clearly call for array math, default to the plain-Python structures from sections 7–10; reach for `numpy` when the problem itself is fundamentally about numerical arrays.

---

## 29. Time and Space Complexity Cheat Sheet

"Time complexity" = roughly how the number of operations grows as the input (`n` items) grows. "Space complexity" = roughly how much extra memory an operation or structure needs beyond the input itself. Both are usually expressed in **Big-O notation** — `O(1)` (constant, doesn't grow with `n`), `O(log n)` (grows very slowly), `O(n)` (grows linearly), `O(n log n)`, `O(n²)` (grows quadratically — gets painful fast). This section collects the complexity of everything covered so far in one place, and explains *why* each one is what it is — the "why" is what actually transfers to new problems, not the number itself.

### Strings (section 6, 14)

| Operation | Time | Why |
|---|---|---|
| `s[i]` (index) | O(1) | strings are stored as one contiguous block in memory; an index is just "jump to this offset" |
| `len(s)` | O(1) | Python stores the length as a field on the string object — it doesn't recount characters |
| `s[a:b]` (slice) | O(k), k = slice length | has to copy k characters into a new string |
| `s + other` | O(n), n = combined length | must allocate a new string and copy both into it (strings are immutable — section 6) |
| `x in s` | O(n) | no shortcut — may have to scan the whole string to rule out a match |
| `s.upper()`, `.lower()`, `.strip()`, `.replace()` | O(n) | each builds and returns a whole new string |
| `"sep".join(pieces)` | O(n), n = total characters across all pieces | one pass to size the buffer, one pass to copy — see [section 14](#14-strings-part-2-slicing-and-more-methods) for the full breakdown vs. `+=` |
| `s1 += s2` in a loop, n times | O(n²) total | each `+=` re-copies everything accumulated so far — this is the trap `.join()` avoids |

**Space:** O(n) to store a string of n characters; every "modifying" operation above allocates a brand-new O(n)-ish block rather than reusing the old one.

### Lists (section 7)

| Operation | Time | Why |
|---|---|---|
| `lst[i]` (index/assign) | O(1) | same reason as strings — contiguous memory, direct offset jump |
| `lst.append(x)` | O(1) amortized | Python over-allocates extra capacity so most appends just drop into already-reserved space; occasionally it has to grow the underlying array and copy everything (O(n)), but spread across many appends that averages out to O(1) each — "amortized" means "on average, over many calls" |
| `lst.pop()` (from the end) | O(1) | nothing has to shift |
| `lst.pop(0)` / `lst.insert(0, x)` | O(n) | removing/inserting at the front means every remaining element has to shift one slot over, to keep the list contiguous |
| `lst.remove(value)` | O(n) | has to scan to *find* the value first (O(n)), then shift everything after it (O(n)) |
| `x in lst` | O(n) | linear scan, no shortcuts — this is the single biggest reason to reach for a `set` instead when you'll do this a lot |
| `lst.sort()` / `sorted(lst)` | O(n log n) | Python's sort (Timsort) is comparison-based; no comparison-based sort can beat O(n log n) in the worst case |
| `lst[a:b]` (slice) | O(k) | copies k elements into a new list |
| `len(lst)` | O(1) | stored as a field, like strings |

**Space:** O(n), plus some slack from over-allocation (that's what makes `.append()` amortized O(1)).

### Tuples (section 8)

Same O(1) indexing and O(n) concatenation/slicing as lists — the *access* patterns are identical, since both are contiguous sequences under the hood. The difference is entirely about what you *can't* do:

| Operation | Time | Why |
|---|---|---|
| `t[i]` | O(1) | same as list |
| `t1 + t2` | O(n) | same as list — immutable, so it must build a new tuple |
| `.append()` / `.remove()` / item assignment | — doesn't exist | immutability means there's no in-place mutation API at all |

**Space:** O(n), and slightly *less* overhead per element than a list, because a tuple never over-allocates spare capacity (it can't grow, so there's nothing to reserve room for).

### Dictionaries (section 9) and Sets (section 10)

Both are **hash tables** under the hood — this is the single most important fact for both structures' performance:

| Operation | Time (average) | Time (worst case) | Why |
|---|---|---|---|
| `d[key]` get/set, `d.get()` | O(1) | O(n) | the key's hash value is used to jump almost directly to its storage slot, instead of searching; worst case only happens with pathological hash collisions, which is rare enough to ignore in practice |
| `key in d`, `x in a_set` | O(1) | O(n) | same mechanism — this is *the* reason to use a dict/set instead of a list for "have I seen this?" checks |
| `del d[key]`, `s.remove(x)` | O(1) | O(n) | same |
| `set1 \| set2` (union), `&` (intersection), `-` (difference) | O(len(set1) + len(set2)) | — | has to visit every element of both sets once |
| iterating (`for k in d`, `for x in s`) | O(n) | — | no way to visit n items in less than O(n) |

**Space:** O(n), but with noticeably more per-element overhead than a list — a hash table needs extra empty slots (to keep collisions rare) and stores the hash alongside each entry.

**A key's hash is a property of the key itself, not of the dict/set it's in.** `hash("apple")` returns the exact same number every time, in any dict, any set, or no container at all — hashing is a method on the key object (`__hash__`), and a dict/set merely *calls* it; it never defines or influences the hash itself. So the same key used in two completely different dicts always hashes identically.

What *can* differ between two dicts, even for the same key, is which physical slot it ends up in — because slot = `hash(key) % table_size`, and `table_size` is internal to each dict (it grows as a dict fills up past ~2/3 full). If two dicts happen to have the same current table size, a shared key computes to the same target slot in both — pure arithmetic, same inputs. But whether it actually *settles* there depends on collision history too: if some other key already landed on that slot first, open addressing probes to a different nearby slot instead. Two dicts built from different keys, even with the same final entry count, usually have different collision patterns (and sometimes different table sizes, since resizing tracks peak fill, not just the current count) — so "same key, same hash" doesn't guarantee "same key, same slot" across two different dicts.

### `collections.deque` (section 23)

| Operation | Time | Why |
|---|---|---|
| `append()` / `appendleft()` | O(1) | implemented as a doubly-linked list of fixed-size blocks — both ends are always immediately reachable, nothing shifts |
| `pop()` / `popleft()` | O(1) | same reason — this is the whole point of `deque` over a plain list |
| `dq[i]` (index into the middle) | O(n) | has to walk the chain of blocks to get there — unlike a list, a deque has no single contiguous array to jump into |

**Space:** O(n), with somewhat more per-element overhead than a list (the linked-block structure).

### `defaultdict`, `Counter` (section 23)

Both are dict subclasses — same O(1) average get/set/`in`/delete as a plain dict. `Counter.most_common(k)` is O(n log n) (it sorts), or O(n log k) when k is small, since Python uses a heap internally for that case.

### `heapq` (section 24)

| Operation | Time | Why |
|---|---|---|
| `heappush()` | O(log n) | after inserting, the new element may have to "bubble up" to restore heap order, and a heap's height is log n |
| `heappop()` | O(log n) | removing the root leaves a gap that must be refilled and "bubbled down" — same log n height argument |
| `heap[0]` (peek the smallest) | O(1) | the smallest element is *always* at index 0 by the heap's own invariant — no search needed |
| `heapq.heapify(lst)` | O(n) | surprisingly not O(n log n) — turning an *already-built* list into valid heap order is cheaper than inserting n elements one at a time, because most of the work happens near the bottom of the tree where there's less to bubble |

**Space:** O(n) — a heap is just a regular list underneath; no extra structure.

### `bisect` (section 25)

| Operation | Time | Why |
|---|---|---|
| `bisect_left()` / `bisect_right()` | O(log n) | binary search — halves the search space each step |
| `bisect.insort()` | O(n) | **the search is O(log n), but the actual insertion into a list is O(n)** — same reason as `list.insert()` above: everything after the insertion point has to shift over. Finding the spot fast doesn't make inserting into it fast. |

### Why one structure beats another — the comparisons that actually come up

**List vs. Tuple** — use a tuple when the data shouldn't change (a coordinate pair, a fixed record) or needs to be a dict key / set element (section 8 — only immutable things are hashable). Use a list when you need to grow, shrink, or reassign elements. Performance-wise they're nearly identical for reading; the real difference is the mutability API, not speed.

**List vs. Set, for membership testing** — this is the one that shows up in nearly every interview problem. `x in list` is O(n) (scan everything); `x in set` is O(1) (hash lookup). Any solution that does `if x in collection` inside a loop should almost always use a set (or dict) for `collection`, not a list — that single swap is often the difference between an O(n²) brute-force solution and an O(n) one. The trade-off: a set has no order and no duplicates, so you lose those properties if you need them.

**List vs. `deque`, for queue-like use** — `lst.pop(0)` is O(n) (shifts everything left); `dq.popleft()` is O(1). Any time you're using a list as a queue (adding at one end, removing from the other — the exact shape of breadth-first search), switch to `deque`. The trade-off: a list gives O(1) random indexing (`lst[500]`); a deque's O(n) random indexing means it's a poor choice if you need to jump into the middle often.

**Dict vs. list-of-tuples/list-of-pairs, for lookup** — scanning a `[(key, value), ...]` list for a matching key is O(n) per lookup; a dict is O(1). If you ever write a loop that searches a list of pairs for a matching first element, that's almost always a sign the data should be a dict instead.

**Heap vs. sorted list, for "repeatedly grab the smallest"** — a heap does O(log n) per insert *and* O(log n) per extract-min, so n insertions + n extractions costs O(n log n) total. Keeping a list fully sorted at all times costs O(n) per insert (via `bisect.insort` — the shifting problem above), so the same n insertions + n extractions costs O(n²) total. The heap wins specifically because it only maintains a *partial* order (parent ≤ children) instead of a *total* order (everything fully sorted) — it does less work per operation by promising less about the overall structure. The sorted list only wins if you need the full sorted order itself for something else, not just repeated access to the extremes.

**`+=` loop vs. `.join()`, for building a string from pieces** — covered in full in [section 14](#14-strings-part-2-slicing-and-more-methods): O(n²) vs. O(n), because immutable strings force every `+=` to re-copy everything accumulated so far, while `.join()` sizes and fills one buffer exactly once.

> **The one-sentence version to internalize:** nearly every "why is X faster than Y" answer in this whole table traces back to one of two causes — *contiguous array with shifting* (lists/strings/tuples: O(1) to read, O(n) to insert/delete anywhere but the end) vs. *hashing* (dicts/sets: O(1) almost everywhere, at the cost of order and extra memory). Recognizing which category a data structure falls into tells you its performance profile without memorizing a table.

---

## 30. Gotchas Every Python Beginner Hits

Four specific bugs, each one caused by a real Python behavior rather than bad luck:

**1. `[[0] * 3] * 2` doesn't do what it looks like.** `[x] * n` repeats the same *reference* n times, not n independent copies. For a plain number that's harmless, but `[0] * 3` is itself a list — so you end up with the same inner list referenced twice:
```python
grid = [[0] * 3] * 2
grid[0][0] = 9
print(grid)   # [[9, 0, 0], [9, 0, 0]]  <- changed BOTH rows! They were the same list all along.

# Correct way — build a fresh list on every iteration of the loop:
grid = [[0] * 3 for _ in range(2)]
grid[0][0] = 9
print(grid)   # [[9, 0, 0], [0, 0, 0]]  <- only row 0 changed, as intended
```

**2. Mutable default arguments are a trap.** A default value is created **once**, when the function is defined — not fresh on every call:
```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print(add_item("apple"))    # ['apple']
print(add_item("banana"))     # ['apple', 'banana']  <- surprise! Same list as before, not a fresh one.

# Fix: default to None, build the real default INSIDE the function body
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

**3. Floor division rounds toward negative infinity, not toward zero.** `7 // 2` is `3` (no surprise), but `-7 // 2` is `-4`, not `-3`. If you want "truncate toward zero" instead (`-3`), you need `int(-7 / 2)`, not `//`.

**4. Assigning a list doesn't copy it.** `b = a` makes `b` point at the *same* list as `a` — they're two names for one object. Modifying one modifies the other, because there's only one list.
```python
a = [1, 2, 3]
b = a           # b is NOT a copy — it's the same list, with a second name
b.append(4)
print(a)         # [1, 2, 3, 4]  <- a changed too!

# To actually copy:
b = a.copy()       # or b = a[:], or b = list(a)
```
This is exactly why recursive/backtracking code that builds up one shared list and appends *copies* of it to a results list (`results.append(current.copy())`) needs that `.copy()` — without it, every entry in `results` would secretly point at the same, constantly-changing list.

---

## 31. Where To Go From Here

If every section above made sense, you have the full prerequisite toolkit for the Concepts Refresher. Go to **[Python Concepts Refresher.md](Python%20Concepts%20Refresher.md)** next — every concept there (sorting with `key=`, closures inside tree recursion, `defaultdict` for graphs, `heapq` for top-k problems, bit tricks, the exact same gotchas revisited) will now be recognizable instead of overwhelming, because you've already met each piece here in isolation, with no algorithm complexity layered on top.

From there, the real target is **[NeetCode 250 Solutions.md](NeetCode%20250%20Solutions.md)** — try writing a solution yourself before reading the given one. Start with the Easy problems in "Arrays & Hashing": that section leans almost entirely on what you just learned in sections 3, 7, 9, 10, and 17 of this file.
