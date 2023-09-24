## Types and prefixes

mlmcr has 5 builtin types and many more prefixes. We'll explore them in this document.

Before starting, however, it's worth specifying how an opcode definition can be represented.
The representation of an opcode definition looks like this:
```
TRY call, [args..., return]  (call:SUBR|FUNC|PROC, args...:*, return:->{*})
```
There are two parts to this representation:
- the actual opcode definition: `TRY call, [args..., return]`
- the type declarations: `(call:SUBR|FUNC|PROC, args...:*, return:->{*})`

In the opcode definition, there is the opcode followed by an arbitrary amount of arguments: here the opcode is `TRY`.
The arguments are a bit less straightforward:

- `TRY call, args, return` would mean that `TRY` accepts three arguments: `call`, `args` and `return`;
- `TRY call, args..., return` instead means that `TRY` accepts at least two arguments. We put `...` in front of an argument name to indicate that it will expand into any number of arguments on call;
- `TRY call, args..., [return]` means that `TRY` accepts at least one argument. Putting brackets around an argument name makes it optional;
- `TRY call, [args..., return]` means the same thing as above, but specifies that `args...` and `return` are linked in some way. However, it isn't strictly necessary to do so.

Let's now specify how things work in the type declarations (it's worth noting that those are wrapped in round brackets, and separated from the opcode definition by **two spaces**):

- each argument is declared with the structure `name:types` (e.g. `call:FUNC`), where `name` is the argument name specified earlier, and `types` is one or more valid types (either builtin or custom) in **uppercase only**;
- to specify multiple types, you can separate them with a pipeline: `call:SUBR|FUNC|PROC`;
- arguments of the form `name...` need to be kept as `name...`, like in `args...:*`;
- optional arguments (of the form `[name]`) must omit the square brackets around them;
- if the type can be anything, `*` is used instead of a list of types, like in `args...:*`;
- if the user needs to pass a variable declaration, the corresponding argument must be declared as `->{types}`, where `types` has the same rules cited before;
- if the type a variable will assume after declaration is the same as another argument's (with infinite possible types), we declare the former as `->{*name}`, where `name` is the name of the latter argument;
- if appropriate, a variable declaration can have the form `<-{types}` or `<->{types}` (see below for details);
- if an argument must be a special name, `>>` is used as `types`, which must be substituted by `F>>` when the special name must be of the form `namespace.name`;
- `>>` and `F>>` can also be used in the same way as `->`, though this behavior is not recommended and only used by `BAKE` and `COOK` opcodes;
- if an argument needs to be a parameter, `>` is used as `types`;
- to indicate that an argument of any type can also be a lookback, we use `^*` instead of `*`;
- to indicate that an argument of any type must be preceded by a `&` prefix in addition to all other prefixes (useful when we need a mlmcr-prefixed string, such as when injecting instructions), we use `&*` instead of `*`;
- to indicate that a `:` prefix is expected, the form `name>>>` is used, as it indicates the argument consumes everything until the end of the instruction

### Integers

Integers in mlmcr are equivalent to `int` types in Python. They are prefixed with `#` (e.g. `#1` becomes `1`), which we call the "pound notation".

To convert a float, a string or a boolean to an integer, we can use the `INT` opcode, which stores the result of Python's `int(from)` into `to`:
```
INT from, to  (from:FLPT|STR|BOOL, to:->{INT})

INT &41, ->$0  ;;$0: 41
```

### Floats

Floats in mlmcr are equivalent to `float` types in Python. They are prefixed with `##` (e.g. `##3.14` becomes `3.14`), which we call the "double pound notation".

To convert an integer, a string or a boolean to a float, we can use the `FLPT` opcode (which name stands for floating-point), which stores the result of Python's `float(from)` into `to`:
```
FLPT from, to  (from:INT|STR|BOOL, to:->{FLPT})

FLPT #4, ->$0  ;;$0: 4.0
```

### Strings

Strings in mlmcr are equivalent to `str` types in Python. They are prefixed with `&` (e.g. `&test` becomes `"test"`), which we call the "amperstand notation".

To convert an integer, a float or a boolean to a string, we can use the `STR` opcode, which stores the result of Python's `str(from)` into `to`:
```
STR from, to  (from:INT|FLPT|BOOL, to:->{STR})

STR ##3.14, ->$0  ;;$0: '3.14'
```

mlmcr strings have two special escape sequences: `/,/` and `/;;/`, which appear as `,` and `;;` in strings, respectively.
Escaping commas and double semicolons is necessary, since the formers are used as argument separators, and the latters to start comments.

### Booleans

Booleans in mlmcr are equivalent to `bool` types in Python. They are prefixed with `!`, which we call the "shout notation".
mlmcr booleans are evaluated to `False` when they are `!0`, or `True` if they are anything else.

To convert something to a boolean, we can use the `BOOL` opcode, which stores the result of Pyhon's `bool(from)` into `to`:
```
BOOL from, to  (from:*, to:->{BOOL})

BOOL &whatever, ->$0  ;;$0: True
```

To quickly use booleans, you have a couple of choices:
- using `!0` for `False` and `!1` for `True` (which is also the recommended method, according to the *mlmcr etiquette*)
- using the `<>F` and `<>T` registers (which evaluate to `False` and `True` respectively)

When setting a variable to a boolean value, we can also use the `FLAG` and `UNFLAG` opcodes (for `True` and `False` respectively):
```
FLAG var  (var:->{BOOL})
UNFLAG var  (var:->{BOOL})

FLAG ->$0  ;;$0: True
UNFLAG ->$0  ;;$0: False
```

To flip a variable (i.e. set it to `True` if it is falsy, and to `False` if it is truthy), we can use the `FLIP` opcode:
```
FLIP var  (var:<->{BOOL})

FLIP <->$0
```

### Null

Null types are the mlmcr representation of Python's `None`.

You can set variables to a null value with the `NULL` opcode:
```
NULL var  (var:->{NULL})

NULL ->$0  ;;$0: None
```

The `<>N` register also holds `None`.

### Binary, octal and hexadecimal numbers

In mlmcr, just like in Python, binaries, octals and hexadecimals are stored as prefixed strings, with the `0b` prefix for binaries, `0o` for octals and `0x` for hexadecimals.

You can convert integers to them by using the `BIN`, `OCT` and `HEX` opcodes, which use the standard Python `bin`, `oct` and `hex` functions:
```
BIN from, to  (from:INT, to:->{STR})
OCT from, to  (from:INT, to:->{STR})
HEX from, to  (from:INT, to:->{STR})

BIN #15, ->$0  ;;$0: '0b1111'
OCT #15, ->$0  ;;$0: '0o17'
HEX #15, ->$0  ;;$0: '0xf'
```

### Getting types

In order to get the type of a variable, you can use the `TYPE` opcode.
`TYPE` uses a custom mlmcr function, `mlmcr.gettype`, to gather the type.

Here is the opcode definition:
```
TYPE var, store (var:*, store:->{STR})

TYPE #1, ->$0  ;;$0: 'INT'
```
It is worth noting that `store` can only be a handful of values in practice:
- `BOOL` for booleans
- `INT` for integers
- `FLPT` for floats
- `STR` for strings
- `NULL` for nulls
- `LOOKBACK` for lookbacks (the type translation of which you'll very rarely encounter in practice)
- `SEQ` for sequences
- `PSEQ` for permasequences
- `PACK` for packs
- `MAP` for maps
- `LOOP` for ranges
- `SUBR` for subroutines
- `FUNC` for functions
- `PROC` for lambdas
- the proper name for other python objects

### The `->`, `<-` and `<->` prefixes

In mlmcr, `->`, `<-` and `<->` all mean one thing: a variable declaration. Sorta.

You see, what the "arrow notation" (this is the name of all those prefixes) actually does is telling the interpreter to not look up the content of whatever variable name follows them, instead transforming it into a string and passing it as an argument.
In fact, you could substitute the arrow notation with the amperstand notation, and everything would still work as expected (though it isn't recommended, since it heavily impacts code clarity), with the exception of escape sequences, which wouldn't be applied and would work as normal (likely causing unexpected errors).

Why are there three prefixes to indicate the same thing, tho?
Well, it's because sometimes it makes sense to use different prefixes, as explained in the *mlmcr etiquette*.

To avoid getting errors because you forgot the arrow notation, it might be helpful to remember a few things:
- you should use the arrow notation every time you want to store stuff to a variable
- you should use the arrow notation every time the variable needs to be read and rewritten afterwards (e.g. when dealing with arrays)
- in general, the arrow notation should be used every time the opcode needs the actual name of the variable, instead of its contents

*Note: if you want to distinguish between the three different prefixes, you can call `->` the "arrow notation", `<-` the "inverted arrow notation", and `<->` the "bidirectional arrow notation".*

### The `>>` prefix

In mlmcr, the `>>` prefix (called the "double arrow notation") is used to indicate special names (i.e. things like namespaces and opcodes), when a string representation is needed.
As with the arrow notation, you can substitute it with the amperstand notation, and nothing bad will happen (apart from a decrease in code readability, and the malfunctioning of escapes).

Generally, when a special name is expected, it is specified directly in the opcode definition, as explained earlier.

### The `>` prefix

The `>` prefix is used in mlmcr to indicate parameter names, and works in the same way as the arrow notation does.
It is recommended to only use this (which is called the "parameter notation") in definition contexts (as specified in the *mlmcr etiquette*).

### The `?` prefix

The `?` prefix (called the "catch-all idiom") is used to indicate a parameter as a catch-all one in functions and lambdas.
There can only be a catch-all parameter in a definition, and it must be the last parameter.
It works by collecting all arguments not bound to parameter names, and binding them to the parameter name that follows the `?` prefix.

To work, it does not get converted to a string. Instead, during argument conversion, a `mlmcr.CatchAll` instance is created and passed as an argument to be handled by relevant opcodes.

### The `:` syntax

In order to handle nested instructions in lambdas, the `:` syntax (called the "colon notation") must be used.
When a colon outside a string is hit, everything following it will be merged into one giant argument and passed to the current opcode.
For example, the instruction `DO ->$0, :PUSH &This is a test!, #1`, will have two arguments: `'$0'` and `"PUSH &This is a test!, #1"`.

### The literal `*`

When a lone `*` is used as an argument (e.g. in `WHEN *, $0`), it gets treated as if it were the string `&*`.

This is called the "any-error idiom", and is used as a shortcut to indicate that any error will trigger the `WHEN` call.
It can also be used, though it's not recommended, as a shortcut when typing strings.

### The `*` prefix

`*` can also be a prefix. This is called the "splat notation", or the "lambda applicator idiom".
When it is used as an argument, such as in `*$1000`, it calls the variable following it, if it evaluates to a lambda, passing as many subsequent arguments as required by the lambda definition (lambdas with catch-alls can't be applied), and substituting it with its return value.

For example, calling:
```
DO ->$1000, >@0, >@1, :ADD @0, @1, ->@2  ;; A lambda that requires two arguments
SNAG <->$1000, >@2  ;; Set @2 (the result of the addition between @0 and @1, the two lambda arguments) as the return value for $1000
PUSH *$1000, #1, #2, &!  ;; Should print "3!"
```
results in `*$1000` being called with the arguments `#1` and `#2`, and all three being substituted for a single argument: the return value of `$1000`.
We can see that arguments before the splat notation and after the required number of lambda arguments are kept intact and will follow the other rules listed here.

### The `^` prefix

The last prefix I'm gonna talk about here is the `^` prefix, which is called the "pointer notation", or "lookback idiom".
This is used to initialize a lookback, which I'll now explain.

Lookbacks are used to postpone variable lookup until the relevant opcode function call.
When an argument like `^$0` is getting converted, it becomes an instance of `mlmcr.LookBack`, which contains the variable name that follows `^` as its `backref` attribute.
Then, during the opcode function call, if the opcode supports lookbacks, the variable gets looked up at the right time, depending on the specific opcode needs.

Currently, by default, only `FOR` and `FORI` opcodes support lookbacks, but there is nothing stopping you from using them in your libraries, if appropriate.

*Note: due to the way lookbacks are handled in `FOR` and `FORI` opcodes, they can only backreference variables in the current scope.
However, there is nothing stopping you from adding support for lookbacks backreferencing variables in any namespace in your libraries (or even in core and builtin libraries, if you change their code).*

### Variable and register prefixes

Those will be covered in later documents: [this](variables.md) for variables and [this](registers.md) for registers. Just keep in mind that there are also those ones.
