## Control Flow

### if, else if, else

mlmcr supports the 'if', 'else if' and 'else' constructs through the `IF`, `ELIF` and `ELSE` opcodes.
Those opcodes are based upon Python's `if`, `elif` and `else` statements, and behave pretty much in the same way.

The `IF` opcode works by calling `call` if `condition` is `True`:
```
IF condition, call, [args..., return]  (condition:BOOL, call:SUBR|FUNC|PROC, args...:*, return:->{*})
```
We'll cover procedure calls later.

The `ELIF` opcode works again by calling `call` if `condition` is `True`, but only if all previous `IF` and `ELIF` opcodes failed:
```
ELIF condition, call, [args..., return]  (condition:BOOL, call:SUBR|FUNC|PROC, args...:*, return:->{*})
```
The `ELIF` opcode requires at least an `IF` opcode to have been called before, and no `ELSE` opcode after that.

The `ELSE` opcode, instead, calls `call` only if all previous `IF` and `ELIF` opcodes failed:
```
ELSE call, [args..., return]  (call:SUBR|FUNC|PROC, args...:*, return:->{*})
```
The `ELSE` opcode requires at least an `IF` opcode to have been called before, and no `ELSE` opcode after that.

### for, indexed for

mlmcr supports the 'for' and "indexed for" constructs through the `FOR` and `FORI` opcodes.
Those opcodes are based on Python's `for ... in ...` and `for ... in enumerate(...)` statements.

The `FOR` opcode works by calling `call` as many times as the number of iterations through `iterable`.
For each iteration, the item (in the iterable) being handled during this iteration is stored in `item`.
It can be accessed during iteration for use as an argument with the pointer notation (`^item`).

Here is the opcode definition:
```
FOR item, iterable, call, [args..., return]  (item:->{*}, iterable:SEQ|PSEQ|PACK|MAP|LOOP, call:SUBR|FUNC|PROC, args...:^*, return:->{*})
```

The `FORI` opcode works in the same way as the `FOR` opcode, but adding another backreferenceable variable: `index`.

Here is its opcode definition:
```
FORI index, item, iterable, call, [args..., return]  (index:->{INT}, item:->{*}, iterable:SEQ|PSEQ|PACK|MAP|LOOP, call:SUBR|FUNC|PROC, args...:^*, return:->{*})
```

### while, do-while

mlmcr supports the 'while' and 'do-while' constructs through the `ALA` (as long as) and `DALA` (do as long as) opcodes.
The `ALA` opcode is based on Python's `while` statement.
Since in Python there is no 'do-while', the `DALA` opcode emulates one.

The `ALA` opcode works by calling `call` until `condition` is `False`:
```
ALA condition, call, [args..., return]  (condition:BOOL, call:SUBR|FUNC|PROC, args...:*, return:->{*})
```

Similarly, the `DALA` opcode works by calling `call` once, then continuing to call it until `condition` is `False`:
```
DALA condition, call, [args..., return]  (condition:BOOL, call:SUBR|FUNC|PROC, args...:*, return:->{*})
```

### Advanced control flow

Inside calls done from `FOR`, `FORI`, `ALA` and `DALA` opcodes, we can control the course of the innermost control flow operator.
This is done with two opcodes:
- `SKIP`, which breaks the loop, ending it prematurely
- `NEXT`, which skips to the next iteration

```
SKIP  ()
NEXT  ()
```

Technically speaking, advanced control flow is obtained by raising two custom exceptions, `mlmcr.Break` and `mlmcr.Continue`, which are caught by supported opcodes and converted to actual iteration modifiers in Python.
If `SKIP` and `NEXT` are used without any control flow opcode running, to prevent the custom exceptions from reaching the module level and causing the underlying Python interpreter to quit, the exceptions are caught in `mlmcr.run` (the function that executes mlmcr instructions) and converted to `Control flow error`s, thrown by `mlmcr.cantUseAdvancedControlFlow`.
