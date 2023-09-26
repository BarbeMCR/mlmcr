## Lambdas

Lambdas are essentially one-instruction functions. Let's see them now.

### Defining and calling lambdas

To define a lambda, you have to use the `DO` opcode:
```
DO proc, argdefs..., :body  (proc:->{PROC}, argdefs...:>, :body>>>)

DO ->$0, >@0, :PUSH @0  ;; This works like the following:
;; FUNC ->$0, >@0
;;     PUSH @0
;; END
```
Note that lambdas must be defined with the colon notation.

To call a lambda, you have three ways:
- you can use the `CALL` opcode
- you can use the `JUMP` opcode
- you can use the splat notation to applicate a lambda in-line

The `CALL` and `JUMP` opcodes have already been described [here](functions.md), while the splat notation was explained [here](types.md).

You should know that lambdas import all top-level namespaces on call.

### Returning from lambdas

Lambdas automatically return `None` when their instruction gets executed.
However, it is often useful to make lambdas actually return one or more of their variables.

You can do that by calling the `SNAG` opcode:
```
SNAG proc, values...  (proc:<->{PROC}, values...:&*)

SNAG ->$0, >@0
```
`SNAG` must be called after defining the target lambda, but before calling it in order to be effective (since it doesn't update retroactively).

`SNAG` works exactly like `GIVE`. In fact, it works by injecting a `GIVE` instruction in the target lambda's body.

### Updating specific variables

The `COOK` opcode can be used to assign to a variable in a specified namespace in a lambda:
```
COOK proc, value, fullvar  (proc:<->{PROC}, value:&*, fullvar:F>>{*value})

COOK ->$0, &test, >>TEST.$0  ;;TEST.$0: 'test'
```
`COOK` works exactly like `BAKE`. In fact, it works by injecting a `BAKE` instruction in the target lambda's body.
