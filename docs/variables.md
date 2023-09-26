## Variables

Variables in mlmcr work just like in any other programming language, with a few quirks.

The main one is that variable names must be of the form `<namespace>.<prefix><hexstring>` (e.g. `TEST.$F0`).

Variables can be used in any instruction by simply citing their names.
For example, `PUSH $0` will print whatever happens to be in the `$0` variable at that time. If the variable does not exist, an error (a `Name error` called by `mlmcr.genericNameError`) will be thrown instead.

### Global variables

In mlmcr, global variables don't really exist (there are registers for that).
Instead, globals are limited to a namespace, are generally invisible to functions and lambdas, and simply happen to be in the "outer" scope.

Global variables are the basis upon which everything else works.
We form them with the prefix `$`, followed by an hexadecimal string (e.g. `$0`).

### Local variables

In mlmcr, local variables are the ones only defined in procedures which create a new scope (i.e. functions and lambdas).

We make them with the prefix `@`, followed by an hexadecimal string (e.g. `@FF`).

### Variables with namespaces

You can look up a variable in a specified namespace by preceding its name with the namespace name and a dot.
For example, to look up variable `$0` in namespace `CUSTOM`, you must specify it as `CUSTOM.$0`.

### The `THIS` keyword

When we are running the mlmcr interpreter in interactive mode or running a mlmcr script and we don't specify a namespace before variable names, they are actually searched in a hidden namespace called `_DEFAULT` (or in the root function scope if we are into a function or lambda).
We don't usually see this, as we also set new variables into the `_DEFAULT` namespace (or the root function scope).

However, when we are in a mlmcr header file, or any other context where the namespace we are using is not `_DEFAULT`, we need to look up variables in that namespace, since assigning to a variable through the usual means (i.e. not using `BAKE` and `COOK`) automatically assigns them in the current namespace.

To do that, the `THIS` keyword must be used before the variable name, as if it was the namespace of the variable.
`THIS` acts by substituting the target namespace with the current one.

`THIS` can always be used, even when the current namespace is `_DEFAULT`, since the `mlmcr.this` function it calls will resolve to it.

`THIS` must also be used when calling an opcode from a different namespace than `_DEFAULT` (we'll see this later).

### Managing variables

In mlmcr, there are three different opcodes to assign to a variable:
- `PUT`, to assign a value to a variable in the current namespace
- `BAKE`, to assign a value to a variable in any namespace
- `NEW`, to create a new instance of a value's type and assign it to a variable in the current namespace: `fromtype` is the value from which to take the type, `to` is the variable to store the new instance, and `args...` are any arguments to pass to the new instance's constructor method

```
PUT value, var  (value:*, var:->{*value})
BAKE value, fullvar  (value:*, fullvar:F>>{*value})
NEW fromtype, to, args...  (fromtype:*, to:->{*fromtype}, args...:*)

PUT #1, ->$0  ;;$0: 1
BAKE #1, >>NS.$0  ;;NS.$0: 1
NEW #1, ->$0, #15, #16  ;;$0: '0xf'
```

To delete a variable, you can use the `DEL` opcode:
```
DEL var  (var:<-{*})

DEL ->$0
```

To swap the contents of two variables, there is the convenience opcode `SWAP`:
```
SWAP a, b  (a:<->{*}, b:<->{*})

SWAP ->$0, ->$1  ;;$0: $1, $1: $0
```

### The kill list

mlmcr has a unique feature amongst programming languages: the ability to temporarily banish variables and retrieve them back later.
This feature was originally added as a solution to namespace pollution (i.e. the quick exhaustion of easy-to-remember variable names: mlmcr has only 16 single-digit variable names and 256 double-digits ones), and was kept for backwards compatibility.

In mlmcr revision 3, the kill list was given a revamp, making it work less like a sequence and more like a map, while keeping the convenience of the builtin opcodes to manage it.

In the current revision, each namespace has its own kill list (this includes procedures which create new scopes, such as functions and lambdas).

To "kill" a variable (i.e. put it in the kill list), you can use the `KILL` opcode:
```
KILL var, [ticket]  (var:<-{*}, ticket:->{INT})

KILL ->$0, ->$F0
```
When a variable is killed, it gets removed from the current scope, but its value gets saved in the scope's kill list. If `ticket` was given, the ticket (the killing identification number) gets stored in it.
`ticket` is optional, since you can get away with manually tracking tickets through careful interaction with the kill list.
Since, if `ticket` is provided, another variable is occupied, I tend to always provide `->$FF`, appending its value to an array. This way the namespace pollution gets contained.

To retrieve a variable from the kill list, you'll need to use the `WAKE` opcode, providing a valid ticket to it:
```
WAKE ticket, var  (ticket:INT, var:->{*})

WAKE #0, ->$0
```

By default, the kill list has a maximum length of `-1`, which equates to infinity.
However, you can set its maximum length with the `KSET` opcode, if you wish:
```
KSET lenght  (lenght:INT)

KSET #256
```

You can also get the current length of the kill list thanks to the `KGET` opcode:
```
KGET to  (to:->{INT})

KGET ->$0
```
