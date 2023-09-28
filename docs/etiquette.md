## The mlmcr Etiquette

While it's true that mlmcr is a semi-esoteric language, meaning it purposefully is hard to read, it is also nice to be able to actually understand code written with it.

In order to improve its readability, a list of recommended ways to structure code has been compiled, and is presented here.

Keep in mind that everything presented in this style guide is optional, though its use should still be favored by mlmcr programmers.

### Appearance

mlmcr code is case-insensitive. However, it is preferred to stick to either **all lowercase or all uppercase** characters. This recommendation doesn't apply to case-sensitive situations, like strings.

You can introduce empty lines if it helps readability, though you shouldn't abuse them.

### Types

Please only use `!0` and `!1` as `False` and `True` respectively.

### Variables

Variable names should follow these guidelines (which are prefix-agnostic, as they should be applied to, for example, `$0` as well as `@0`):

| Start of name block | End of name block | Intended purpose |
| ------------------- | ----------------- | ---------------- |
| `$0`                | `$9`              | Working variables (e.g. variables needed throughout the program, or frequently accessed, especially in functions, etc.) |
| `$A`                | `$F`              | Working variables, especially when it makes sense to group them separately from the others (e.g. `$0-$9` for variables related to arrays, and `$A-$F` for variables related to strings) |
| `$10`               | `$9F`             | Less-used variables |
| `$A0`               | `$AF`             | Loops |
| `$B0`               | `$BF`             | Flags and semi-constants (the latters are variables that get updated very rarely) |
| `$C0`               | `$CF`             | Constants |
| `$D0`               | `$DF`             | Arbitrarily allocated space for extra flags and constants (try to follow a `$D0-$D9` and `$DA-$DF` division between them if applicable) |
| `$E0`               | `$E9`             | Custom error names |
| `$EA`               | `$EF`             | Arbitrarily allocated space for extra error names (or data if only variables `$E0-$E5` are used), flags and constants (prioritize errors) |
| `$F0`               | `$FE`             | Temporary variables |
| `$FF`               | ---               | Universal throw-away variable (like Python's `_`) |
| `$100`              | `$10F`            | Custom error messages and data |
| `$110`              | `$FFF`            | Arbitrary variables (try dividing these logically if possible) |
| `$1000`             | `$9FFF`           | Functions, subroutines and lambdas |
| `$A000`             | `$FFFF`           | *unallocated* |
| `$10000`            | `$FFFFF`          | Sparsely allocated inner-level functions, subroutines and lambdas (see below for more guidelines) |
| `$100000`           | *infinity*        | Arbitrary data *__(use not recommended)__* |

Variable names should be somewhat progressive, but still resemble some kind of logical pattern if possible.

Names for inner-level functions, subroutines and lambdas should be formed as follows: `$<outermost name>0-F`.
For example, a subroutine defined inside function `$174F` might have `$174F0` as its name.
If there are even more inner-level procedures, no more digit should be added, but another name should be created with the same pattern as before (e.g. a lambda defined inside `$174F0` might have `$174F1` as its name).

### Indentation

Definitions should be indented 4 spaces in, and the termination opcode should be unindented.

### Register names

If you are a script user, it is recommended to only use the 3 or less characters version of register names (e.g. `<>AEX`).

Instead, if you are writing a library of some sort, it is more appropriate to use the 8.3 version (e.g. `<>MYLIB.XYZ`).
The name before the dot should be the namespace your library defines, or an abbreviation of it.

It is **absolutely** indicated to only modify the contents of registers made by your script or library (**especially** in the latter case, since the user will be the final user, not you!).

*__NEVER__*, never, never delete registers not created by you, **especially** in libraries.
