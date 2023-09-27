## Registers

Another way of storing values, apart from variables, is through the use of registers.
Registers are "superglobals", in the sense that they are shared among all namespaces, and can be created, modified and deleted from anywhere.

You can reference registers with the `<>` syntax (called the "spread notation"), such as in `PUSH <>MLMCR.AUTHOR`.

### Builtin registers

These registers are created at the start of every interpreter session:
- `<>N`, which holds `None` (a null)
- `<>T`, which holds `True`
- `<>F`, which holds `False`
- `<>MLMCR.VER`, which holds version information in a pack with format `(major, minor)` (e.g. `(3, 0)` for mlmcr Revision 3)
- `<>MLMCR.HUMANVER`, which holds human-readable version information (e.g. `3.0` for mlmcr Revision 3)
- `<>MLMCR.AUTHOR`, which holds a string describing mlmcr's author
- `<>MLMCR.COPYRIGHT`, which holds copyright information for the current mlmcr version
- `<>MLMCR.PYVER`, which holds the underlying Python version string (e.g. `3.11.5`)

It is to note that builtin registers are not subject to name limitations.

### Using registers

Apart from referencing them in instructions, registers have four opcodes especially designed to work with them:
- `SIGN` to create registers
- `POKE` to update registers
- `PEEK` to explicitely read registers
- `REVOKE` to delete registers

Here are their opcode definitions:
```
SIGN reg  (reg:>>)
POKE reg, val  (reg:>>, val:*)
PEEK reg, store  (reg:>>, store:->{*})
REVOKE reg  (reg:>>)

SIGN >>AEX
POKE >>AEX, #1  ;;<>AEX: 1
PEEK >>AEX, ->$0  ;;$0: 1
REVOKE >>AEX
```

Registers created through `SIGN` have some name limitations:
- they can be only up to 3 characters long  (e.g. `AEX`)
- (unless) they are preceded by a dot, in which case they can have up to an additional 8 characters before the dot (e.g. `SOMETEST.AEX`)

Technically, `PEEK` isn't needed to copy the contents of a register into a variable (we could use `PUT` for that), but it is recommended to use it to improve readability (unless you can't, such in the case of `MAKE` assignments).
