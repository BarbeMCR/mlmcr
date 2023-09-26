## Subroutines

Subroutines are pieces of code which can be called at will, just like functions.
The difference is that they do not take arguments, cannot return values and do not create new scopes at call time.

### Defining subroutines

To define a subroutine, you can use the `SUBR` opcode in a similar way to the `FUNC` opcode:
```
SUBR s  (s:->{SUBR})
RTS  ()

SUBR ->$0
    ...
RTS
```
As you can see, the `RTS` opcode works similarly to the `END` opcode for functions: it ends the current subroutine definition.
However, it does not return anything on call, like you would instead expect for a function.

### Calling subroutines

To call a subroutine, you can use the already mentioned `JUMP` opcode:
```
JUMP s  (s:SUBR|FUNC|PROC)

JUMP $0
```
