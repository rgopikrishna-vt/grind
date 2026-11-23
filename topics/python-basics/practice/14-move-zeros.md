---
id: move-zeros
title: Move zeros to the end
topic: Lists
difficulty: easy
lesson: 7
---

## Prompt
Write `move_zeros(nums)` that moves every `0` to the end of the list **in place**, keeping the order of the other elements. It should return `None`, like `list.sort()` does.

```python
nums = [0, 1, 0, 3, 12]
move_zeros(nums)
nums  # [1, 3, 12, 0, 0]
```

## Starter
```python
def move_zeros(nums):
    pass
```

## Examples
```python
nums = [0, 1, 0, 3, 12]
move_zeros(nums)
assert nums == [1, 3, 12, 0, 0]
```

## Tests
```python
a = [0]
assert move_zeros(a) is None
assert a == [0]
b = [1, 2, 3]
move_zeros(b)
assert b == [1, 2, 3]
c = [0, 0, 1]
move_zeros(c)
assert c == [1, 0, 0]
d = [4, 0, 5, 0, 0, 6, 7, 0]
d_id = id(d)
move_zeros(d)
assert d == [4, 5, 6, 7, 0, 0, 0, 0]
assert id(d) == d_id
e = []
move_zeros(e)
assert e == []
```

## Hints
- "In place" means change the list you were given; assigning `nums = ...` inside the function only rebinds the local name.
- Keep a write position `w`. Walk the list, and copy each non-zero to `nums[w]`, then `w += 1`.
- After the walk, fill `nums[w:]` with zeros. Or swap `nums[w], nums[i] = nums[i], nums[w]` as you go.

## Solution
```python
def move_zeros(nums):
    w = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[w], nums[i] = nums[i], nums[w]
            w += 1
```

## Explanation
The two-pointer swap is O(n) time and O(1) extra space. A shorter version that is still in place is slice assignment: `nums[:] = [x for x in nums if x] + [0] * nums.count(0)`. Writing `nums[:] =` replaces the contents of the same list object, whereas `nums =` would not affect the caller.
