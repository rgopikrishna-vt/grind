---
id: make-tag
title: Build an HTML tag
topic: Functions
difficulty: medium
lesson: 13
---

## Prompt
Practice `*args`, `**kwargs` and default arguments. Write `make_tag(name, *children, **attrs)` that returns an HTML string:

- `children` are strings placed inside the tag, joined with nothing between them
- each keyword argument becomes an attribute `key="value"`, in the order given
- a trailing underscore is removed from a key, so `class_="x"` becomes `class="x"` (because `class` is a reserved word)

```python
make_tag("p", "Hi")                      # '<p>Hi</p>'
make_tag("a", "Docs", href="/d", class_="nav")
# '<a href="/d" class="nav">Docs</a>'
```

## Starter
```python
def make_tag(name, *children, **attrs):
    pass
```

## Examples
```python
assert make_tag("p", "Hi") == "<p>Hi</p>"
assert make_tag("a", "Docs", href="/d", class_="nav") == '<a href="/d" class="nav">Docs</a>'
```

## Tests
```python
assert make_tag("br") == "<br></br>"
assert make_tag("ul", "<li>1</li>", "<li>2</li>") == "<ul><li>1</li><li>2</li></ul>"
assert make_tag("input", type="text", id="q") == '<input type="text" id="q"></input>'
assert make_tag("div", make_tag("span", "x"), id_="main") == '<div id="main"><span>x</span></div>'
args = ["a", "b"]
opts = {"title": "t"}
assert make_tag("i", *args, **opts) == '<i title="t">ab</i>'
```

## Hints
- Inside the function, `children` is a tuple and `attrs` is a dict.
- Build the attribute text with `"".join(f' {k.rstrip("_")}="{v}"' for k, v in attrs.items())`.
- Then `return f"<{name}{attr_text}>{''.join(children)}</{name}>"`.

## Solution
```python
def make_tag(name, *children, **attrs):
    attr_text = "".join(f' {key.rstrip("_")}="{value}"' for key, value in attrs.items())
    return f"<{name}{attr_text}>{''.join(children)}</{name}>"
```

## Explanation
`*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dict, which keeps the order they were passed. At a call site the same symbols *unpack*: `f(*my_list, **my_dict)`.
