# Changelog

All notable changes to the "mlmcr" extension will be documented in this file.

## [3.0.0]

Initial release. The versioning of this extension starts with version 3.0.0 to indicate support for mlmcr Revision 3 syntax.

### Added

- Autocompletion and autoindentation of func-end, subr-rts and cls-ecls blocks
- Autocompletion of pyblock-pyend blocks
- Autocompletion of (), [], {} and "" pairs
- Autocompletion of /,/ and /;;/ escape sequences
- Basic Python syntax highlighting in pyblocks
- Differentiated syntax highlighting of most mlmcr features:
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
  - language variables (this, self and super)
  - the * idiom to catch all errors (as used in 'when *, ...')
  - registers (starting with <>)
