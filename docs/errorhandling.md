## Error Handling

Many opcodes in mlmcr might cause errors to be raised. Normally, these cause the interpreter to exit when running scripts.
To help you control that, we have introduced error handling.

### Builtin errors

Before we can actually talk about error handling, it is better to make a list of all builtin errors:
- `Name error`, for when an inexistent variable is referenced;
- `Format error`, for when the creation of a variable whose name doesn't follow its scope rules is attemped;
- `Number error`, for when a non-numeric value is passed where an integer or float was expected *(deprecated)*;
- `Kill list full error`, for when the scope's kill list is full and another variable is attemped to be killed;
- `Ticket error`, for when an invalid ticket is used to resurrect a variable;
- `Opcode error`, for when an inexistent opcode gets called, or a value is passed instead of a variable declaration in an instruction, or there is a format error in the arguments or in the opcode definition;
- `Argument error`, for when a wrong number of arguments is passed in an instruction;
- `Type error`, for when an argument of the wrong type is passed in an instruction;
- `Context error`, for when an opcode is called outside of its allowed scopes (e.g. calling `END` outside a function definition);
- `Operation type error`, for when an unsupported type is passed for an operation;
- `Namespace error`, for when an inexistent namespace is referenced, or it has a format error;
- `Index error`, for when an out-of-bounds index for an array is passed;
- `Key error`, for when an inexistent key for a map is passed;
- `Definition error`, for when there is more than one catch-all parameter in a definition, it isn't the last one, or a definition is attempted in a forbidden place (e.g. a function definition is attempted inside a lambda body);
- `Argument count error`, for when a wrong number of arguments is passed to a mlmcr callable;
- `Mismatch error`, for when an opcode is called, but no matching opcode was called before (e.g. when an `ELIF` opcode is called before an `IF`);
- `Lambda error`, for when a lambda application error occurs (e.g. when a lambda with a catch-all parameter is attempted to be applied);
- `Invalid register name error`, for when a register whose name doesn't respect the rule is attempted to be created;
- `Invalid register error`, for when an inexistent register is referenced;
- `Control flow error`, for when advanced control flow is attempted outside a control flow statement (e.g. when `SKIP` is called outside a `FOR`);
- `Stack error`, for when a return to a level outside the stack length is attempted;
- `Inexistent header file`, for when no valid header file is found at the location specified by an import instruction;
- `Fatal lookup error`, for when a fatal error happens inside `mlmcr.this`;
- `Recursion error`, for when the recursion limit is exceeded, and `RecursionError` is raised;
- `Memory error`, for when the mlmcr interpreter exceeds its allocated memory, and `MemoryError` is raised

### Error handling

To start handling errors, you first have to make the mlmcr interpreter go into "try mode".
To do so, you must use the `TRY` opcode:
```
TRY call, [args..., return]  (call:SUBR|FUNC|PROC, args...:*, return:->{*})

TRY $0, #1, #2, ->$1
```
The `TRY` opcode works by calling `call`, just like calling the `CALL` opcode would.
However, there is a neat thing about `TRY`: whatever error `call` happens to throw will be recorded and ignored by the mlmcr interpreter.

After calling a `TRY`, you can then start seeing whether specific errors were raised with the `WHEN` opcode:
```
WHEN error, call, [args..., return]  (error:STR|'*', call:SUBR|FUNC|PROC, args...:*, return:->{*})

WHEN &Name error, $2, ->$FF
```
Here, `error` must be one of the names above, or that of a custom error (see below). Keep in mind that error names are **case-sensitive**.
A lone star (i.e. only a `*`) can also be used as a name. In that case, any error occured will be handled.
If an error of type `error` was thrown before, `call` will then be called.

After any `WHEN` opcode, you can optionally place an `ACE` opcode:
```
ACE call, [args..., return]  (call:SUBR|FUNC|PROC, args...:*, return:->{*})

ACE $3, ->$FF
```
`ACE` calls `call` only if no error at all occured in try mode.

After any `WHEN` (or `ACE`, if present), you can also place a `THEN` opcode:
```
THEN call, [args..., return]  (call:SUBR|FUNC|PROC, args...:*, return:->{*})

THEN $1000, #1, #2, #3, ->$10
```
`THEN` calls `call` regardless of any error that might have occured before.

Finally, to exit try mode, you must put a `STOP` opcode:
```
STOP  ()

STOP
```

### Custom errors

You can also throw your own errors with the `CAST` opcode:
```
CAST error, [message]  (error:STR, message:STR)

CAST &Custom error, &this is a custom error thrown with CAST
```
Builtin error names can also be used as the `error` argument.
Optionally, you can also put a `message` to be displayed in case the error doesn't get handled.
In order to catch a custom error, you must call `WHEN error, ...`, where `error` is the name of the error you just created.
