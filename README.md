# mlmcr
The unnecessary Assembly-like programming language, made with love (or hate, decide by yourself) by BarbeMCR.

### Manual

- What is mlmcr?
Well, it's easy enough: mlmcr is a Python-derived programming language that feels like you are writing machine code into an old-style code monitor that does not like variable names and wants you to write all the variables as memory addresses (e.g. $0DC7). If you wonder, yes, it's as useless as hell (and as evil too).

- What if I make some mistake in the code?
Good luck. You are gonna need it. When something like a syntax error is found, the file that is being parsed will display an error message. Based on when the error appeared, you may be hinted towards a specific section of the file. Other than that, there isn't much else aiding you. But, if you are programming on the interpreter, the culprit line will be immediately identifiable, as the code throws an error after entering the instruction.

- How do I comment the code?
Lines that start with ; will be treated as comments. In-line comments aren't allowed.

- How do I run mlmcr?
If you have a *COMPILED* version of mlmcr:
Launch a terminal session (if you want).
Navigate into the directiory where mlmcr.exe is (or open it directly in a file browser).
To launch the mlmcr interpreter, write (without quotes):
`mlmcr.exe`
To execute a `.mlmcr` file, write:
`mlmcr.exe <file_path>`

If you have a *SOURCE* version of mlmcr:
Launch a terminal session.
Navigate into the directory where the mlmcr.py script is.
To launch the mlmcr interpreter, write (without quotes):
`python mlmcr.py`
To execute a '.mlmcr' file, write:
`python mlmcr.py <file_path>.mlmcr`

*__SHORT INSTRUCTION GUIDE__*

Currently, mlmcr has 42 instructions to work with.

Note: operations with floating-point numbers will always store results as floating-point numbers, regardless of the amount of integer arguments.
Note: boolean values are generally omitted from this manual as rarely used, but can be used in a variety of instructions.

**VARIABLES**

**PUT** - assign a value to a variable

**DEL** - delete a variable

**KILL** - put a variable in the kill list

**WAKE** - retrieve a variable from the kill list

**KSET** - set the maximum lenght of the kill list

**KGET** - retrieve the highest index of the kill list

**ADD** - sum variables and/or numbers and store the result in a variable

**SUB** - subtract variables and/or numbers and store the result in a variable

**MUL** - multiply variables and/or numbers and store the result in a variable

**DIV** - divide variables and/or numbers and store the result in a variable

**FDIV** - floor divide variables and/or numbers and store the result in a variable

**MOD** - calculate the remainder of variables and/or numbers and store the result in a variable

**POW** - calculate the power of variables and/or numbers and store the result in a variable

**INC** - increment a variable

**DEC** - decrement a variable

**PUSH** - print variables to screen

**PULL** - get a variable from user input

**INT** - convert a floating-point number or a string to an integer number

**FLPT** - convert an integer number or a string to a floating-point number

**STR** - convert an integer number or a floating-point number to a string

**BOOL** - convert a variable to a boolean

**LINK** - join two strings together

**FSTR** - split a string into a sequence

**TSTR** - join a sequence into a string

**ARRAYS**

**SEQ** - build a sequence

**PSEQ** - build a permanent sequence

**PACK** - pack variables

**JOIN** - add items to an array

**NEST** - add an array to an array

**POP** - remove an item from an array based on its index

**REM** - remove an item from an array based on its value

**GETI** - get the index of a value in an array

**GET** - get a value in an array based on its index

**SET** - insert a value in array before a given index

**REPL** - replace a value in an array based on its index

**LEN** - get the lenght of an array

**IN** - check if a value is in an array

**WIPE** - clear an array of its items

**OTHER INSTRUCTIONS**

**HALT** - delay code execution

**EXIT** - quit the current script or interpreter

**PYEVAL** - evaluate a Python expression

**PYEXEC** - execute Python code
