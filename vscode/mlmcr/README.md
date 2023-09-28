# mlmcr

mlmcr is a Visual Studio Code extension that adds syntax highlighting support for the mlmcr programming language.

## Features

The mlmcr extension provides distinct syntax highlighting to each of this following language features:
- comments (starting with ;;)
- numbers (starting with # and ##)
- booleans (starting with !)
- the null opcode
- function, subroutine and lambda definitions (respectively func, subr and do opcodes)
- class definitions (cls opcode)
- control flow opcodes (if, elif, else, for, fori, ala, dala, call, jump, give, take, sync and loop)
- error handling opcodes (try, when, ace and then)
- logical opcodes (eq, ne, gt, lt, ge, le, and, or, not, is and in)
- arithmetic opcodes (add, sub, mul, div, fdiv, mod, pow and abs)
- assignment opcodes (put, inc and dec)
- "special" push and pull opcodes
- all other namespace.opcode sequences (including those inside lambda definitions, of format :namespace.opcode)
- strings (starting with &)
- escape sequences (/,/ and /;;/ in strings)
- global and local variables (starting with $ and @)
- class instance attributes (starting with _$)
- declarations/parameters (starting with ->$, ->@ and ->_$)
- lambda-applicator instruction arguments (starting with *$, *@ and *_$)
- catch-all parameters (starting with ?$, ?@ and ?_$)
- look-back instruction arguments (starting with ^$, ^@ and ^_$)
- language variables (this, self and sup)
- the * idiom to catch all errors (as used in 'when *, ...')

It also allows autocompletes func-end, subr-rts, cls-ecls and pyblock-pyend blocks, (), [], {} and "" pairs and /,/ and /;;/ escape sequences.

Finally, it autoindents function, subroutine and class bodies.

## Release Notes

### 3.0.0

Initial release of the mlmcr extension. It supports the new mlmcr 3 syntax, and is not compatible with either mlmcr 1 or mlmcr 2.
