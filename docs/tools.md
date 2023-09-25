## Core tools

### Additional tools for arrays

There are four additional opcodes for working with arrays:
- `MIN`, for getting the minimum value in an array
- `MAX`, for getting the maximum value in an array
- `ANY`, which returns `True` when at least a value in an array is truthy, or `False` otherwise
- `ALL`, which returns `True` when all the values in an array is truthy, or `False` otherwise

```
MIN val_or_iter, vals..., store  (val_or_iter:*|SEQ|PSEQ|PACK|MAP|LOOP, vals...:*, store:->{*})
MAX val_or_iter, vals..., store  (val_or_iter:*|SEQ|PSEQ|PACK|MAP|LOOP, vals...:*, store:->{*})
ANY iter, store  (iter:SEQ|PSEQ|PACK|MAP|LOOP, store:->{BOOL})
ALL iter, store  (iter:SEQ|PSEQ|PACK|MAP|LOOP, store:->{BOOL})
```

### Standard operators

mlmcr supports several standard operators:
- `EQ` for checking equality: `a == b`
- `NE` for checking inequality: `a != b`
- `GT` for checking if a value is greater than another: `a > b`
- `LT` for checking if a value is smaller than another: `a < b`
- `GE` for checking if a value is greater than or equal to another: `a >= b`
- `LE` for checking if a value is smaller than or equal to another: `a <= b`
- `AND`, which returns `True` when two values are both truthy, or `False` otherwise: `a and b`
- `OR`, which returns `True` when at least one value is truthy, or `False` otherwise: `a or b`
- `NOT`, which returns the boolean opposite of a value: `not a`
- `IS` for checking identity: `a is b`
- `IN` for checking whether a value is inside another: `a in b`
- `ISNT` for checking lack of identity: `a is not b`
- `INNT` for checking whether a value isn't inside another: `a not in b`

```
EQ a, b, store  (a:*, b:*, store:->{BOOL})
NE a, b, store  (a:*, b:*, store:->{BOOL})
GT a, b, store  (a:*, b:*, store:->{BOOL})
LT a, b, store  (a:*, b:*, store:->{BOOL})
GE a, b, store  (a:*, b:*, store:->{BOOL})
LE a, b, store  (a:*, b:*, store:->{BOOL})
AND a, b, store  (a:*, b:*, store:->{BOOL})
OR a, b, store  (a:*, b:*, store:->{BOOL})
NOT what, store  (what:*, store:->{BOOL})
IS a, b, store  (a:*, b:*, store:->{BOOL})
IN a, b, store  (a:*, b:*, store:->{BOOL})
ISNT a, b, store  (a:*, b:*, store:->{BOOL})
INNT a, b, store  (a:*, b:*, store:->{BOOL})
```
mlmcr doesn't have any bitwise operator for now, though I might include them eventually as part of a standard library.

The operators are pretty straightforward: the only unintuitive thing is probably the `IS` (and `ISNT`) opcode.
It works by returning the value of Python's `id(a) == id(b)` (or `id(a) != id(b)`).
In practice, you'll probably only need it for comparing stuff to literal nulls and booleans (e.g. `IS $0, <>N, ->$1`).

### Console IO

There are two opcodes dedicated to console IO (i.e. user interaction through the terminal window mlmcr runs in):
- `PUSH`, which prints things to the screen (by writing to `stdout`)
- `PULL`, which gets input from the user (by reading from `stdin`)

```
PUSH stuff...  (stuff...:*)
PULL into, [prompt]  (into:->{STR}, prompt:STR)

PUSH &stuff, #2  ;; prints "stuff2"
PULL ->$0, &Input:   ;; prints "Input: " and stores the input in $0
PULL ->$0  ;; stores the input in $0 without printing anything
```
