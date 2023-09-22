# mlmcr
mlmcr is a dynamically typed, multi-paradigm, general-purpose, interpreted semi-esoteric programming language written in Python.
Its code is made to look similar, at least to some extent, to Assembly code.

mlmcr makes wide use of prefixes to identify types, and limits variable names to hexadecimal-only names.

I don't recommend mlmcr for actual production code, due to the high likelyhood of encountering bugs (I am a solo developer, and it would help me a lot if you took the time to open a bug report in case you find any).

## Sample code

This code asks the user to input an arbitrary number of floats, then increases each by 1 and prints the resulting list:

```
seq ->$0
pull ->$10, &How many values to insert? 
int $10, ->$10
loop $10, ->$a0
subr ->$1000
    pull ->$a, &Insert value: 
    flpt $a, ->$a
    join <->$0, $a
rts
for ->$ff, $a0, $1000
func ->$1001, >@1, >@a
    do ->@10010, >@a, :inc ->@a
    snag <->@10010, >@a
    call @10010, @a, ->@a
    put $0, ->@0
    repl <->@0, @1, @a
end
fori ->$f1, ->$f0, $0, $1001, ^$f1, ^$f0, ->$ff
push $0
```

## Features

- Variables names must be hexadecimal, and are preceded by a prefix: usually *$* for globals and *@* for locals
- Most types are defined using specific prefixes
- Instructions are executed one at a time, without the possibility of nesting them together, and are composed of an opcode and a number of arguments
- Supports many standard Python types (int, float, str, bool, NoneType, list, tuple, dict, range)
- Allows variables to be "killed" (i.e. put in a special list, the kill list) and woken up again to limit namespace pollution
- Has an extra array type: the pseudosequence (which is a sort of read-only list)
- Supports if-elif-else statements, for, indexed for, while and do-while loops
- Supports error handling and throwing custom errors
- Has functions, subroutines and lambdas
- Supports registers, which act as "superglobal" variables (indicated to use as constants)
- Supports multiple namespaces, each with their own opcodes and variables
- Allows binding callables to opcodes
- Supports external libraries
- Can be extended using the mlmcr API in Python
- Has a Visual Studio Code extension for syntax highlighting (requires VS Code >=1.43.0)

## Language reference and documentation

You can find the documentation contents [here](docs/contents.md).

## Requirements

- Python (>=3.10)
- pyinstaller (>=4.7 for python 3.10, >=5.6.2 for python 3.11, >=5.13.2 for python 3.12+; requires additional libraries; only required to freeze the mlmcr interpreter)

To use a pre-frozen interpreter (does not include the entire Python standard library):
- Windows 10+ 64-bit
- a modern GNU/Linux distro (tested on Ubuntu 22.04)

To install and use mlmcr from a pre-frozen bundle (not recommended for "production" use), download and extract the relevant release for your platform, then type `mlmcr` (or `mlmcr <file>` to run a script).

To install and use mlmcr from source, download and extract the source code, then type `python mlmcr.py` or `python3 mlmcr.py` (or `python mlmcr.py <file>` or `python3 mlmcr.py <file>` to run a script) in a terminal window.

To freeze mlmcr, download and extract the source code (using only basic libraries), then type: `pyinstaller --console --hiddenimport math --hiddenimport random mlmcr.py`.
To package extra Python modules (standard or not), type `--hiddenimport <library>` before `mlmcr.py`.

## License

mlmcr is licensed under the MIT license.
