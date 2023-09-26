## Functions

Functions are essential in any mlmcr program, so the time has come to cover them.
Functions are pretty much pieces of code, which can be called whenever you want, can have arguments passed to them and create a new scope every time they are called.

### Defining functions

Function definitions in mlmcr are pretty straightforward, and resemble those of other programming languages (just in an uglier way).
To define a function, you must call the `FUNC` opcode:
```
FUNC fn, argdefs...  (fn:->{FUNC}, argdefs...:>)

FUNC ->$0, >@0, >@1, ?@F
    ...  ;; Function body
```

As we briefly saw when talking about types, function parameters are defined with the `>` syntax.
Since parameters are assigned at runtime inside the function scope, their names must follow the rules set by its scope (which means using the `@` prefix on a stock interpreter).

Functions also accept catch-all parameters, which bind to a pack of all the extra arguments that remain after binding the others to regular parameters, with the `?` syntax.
An example of how a catch-all parameter works is the following: `CALL $0, #1, #2, #3, #4, ->$FF` (ignore the opcode and last argument for now).
The function we defined before only accepted two regular arguments, but, thanks to the catch-all parameter, also accepts any other argument passed: this way `@0` becomes `1`, `@1` becomes `2` and `@F` becomes `(3, 4)`.

Function definitions are closed when an `END` opcode is hit in the function body:
```
END  ()

FUNC ->$0, >@0, >@1, ?@F
   ...  ;; Function body
END
```
`END` also implicitely returns `None`, if the function hasn't returned before.

### Calling functions

Functions can be called with the `CALL` opcode:
```
CALL fn, args..., return  (fn:FUNC|PROC, args...:*, return:->{*})

CALL $0, #1, #2, #3, #4, ->$FF  ;;$FF: None
```
`CALL` works by calling the first argument, and storing its return value in the last. Every argument between those is passed to the call, and will bind to the corresponding parameters.

In some very specific circumstances, the `JUMP` opcode can also be used, which simplifies things:
```
JUMP s  (s:SUBR|FUNC|PROC)

JUMP $1
```
`JUMP` is applicable to functions if the following conditions are met:
- the function accepts no argument
- (or) it only has a catch-all argument and we don't need to pass anything to it with this call
- the return value of the function isn't needed

### Getting things into functions

To import namespaces from the scope outside the function (which is called the "parent scope"), the `TAKE` opcode must be used:
```
TAKE space, spaces...  (space:>>, spaces...:>>)

TAKE >>TEST, >>STUFF
```
The syntax of this opcode definition might be a bit confusing. To avoid any ambiguity, it means that it accepts at least one special name.
Every argument passed to it gets translated to an actual namespace, which gets imported as a subspace of the function scope (i.e. become a sub-namespace of it, not linked with the original one and visible only inside the function).

It is worth noting that `THIS` doesn't have any special meaning here (not that there is a need to anyways).

It is also worth noting that the `_DEFAULT` namespace gets automatically imported whenever a call to the function is made.
This import is special, however, since the namespace gets taken directly from `namespaces` (which is where all top-level namespaces are stored) instead of getting it from the parent scope.

Also, functions have a builtin empty namespace called `EXT`, which can be used to simplify the passage of values from outer to inner functions.
You can, for example, place some variables you need in an inner function in the `EXT` namespace of the outer function, and call `TAKE >>EXT` in the inner function to retrieve them.

### Getting things out of functions

The standard way for getting stuff out of functions is to return them, with the `GIVE` and `HAND` opcodes.

To return a value like in any other programming language, the `GIVE` opcode gets used:
```
GIVE values...  (values...:*)

GIVE #1, @0
```
You can pass how many values you want to the `GIVE` opcode, but be wary that passing no value causes the function to immediately return `None`, and passing multiple ones causes them to be put into a pack.

As stated before, calling `GIVE` (or `HAND`) causes the function to immediatly return, which means that the rest of the body won't be executed.

A peculiarity of mlmcr is the `HAND` opcode, which lets you return a function at any stack level, which means that parent, grand-parent, grand-grand-parent, ... functions can be returned from any child function:
```
HAND depth, values...  (depth:INT, values...:*)

HAND #1  ;; This returns None from the function the current function was called from
HAND #2, &test  ;; This returns 'test' from the function the function that called the current function was called from
```
A positive value for `depth` causes the `depth`-shallow function in the stack (i.e. the function `depth` levels nearer to the beginning of the stack) to return
A zero or negative value for `depth` causes the current function to return instead.

There is also a way to get entire namespaces out of functions: the `SYNC` opcode.
Here is its definition:
```
SYNC space, spaces...  (space:>>, spaces...:>>)

SYNC >>TEST, >>STUFF
```
`SYNC` works exactly like `TAKE` but in reverse, exporting namespaces from the function scope.
It is to note that `SYNC` overwrites existing namespaces.
You can also update the `_DEFAULT` and `EXT` namespaces with `SYNC`, so try to make use of that feature.
