# mlmcr
The unnecessary Assembly-like programming language, made with love (or hate, decide by yourself) by BarbeMCR.

### Hello world example
Before jumping into the manual, let's try analyzing the Hello World program written in mlmcr.
The program is as follows:
```
PUT &Hello world!, $0
PUSH $0
```
The output will be:
```
Hello world!
```
Here, the `PUT` instruction stores the string `Hello world!` (we put a `&` sign before a string to signal the interpreter that we are in fact writing a string, and not anything else, such as an integer) in the variable `$0` (yes, variables can only be hexadecimal characters and are preceeded by a `$` sign).

Afterwards, the `PUSH` instructions prints the contents of the variable `$0` to screen, and we get our `Hello world!` string back.

If you need a more complex example, try opening the `map_demo.mlmcr` file. However, this demo doesn't include all features of mlmcr.
The `mlmcr2_manual.txt` file contains reference for all instructions in mlmcr.

Try out a few instructions in the interpreter until you get the desired output!
Then you can start writing scripts in your favorite text editor. Just make sure to save your scripts with the `.mlmcr` extension or the interpreter will not recognize them. Happy programming!

### Manual

**What is mlmcr?**

Well, it's easy enough: mlmcr is a Python-derived programming language that feels like you are writing machine code into an old-style code monitor that does not like variable names and wants you to write all the variables as memory addresses (e.g. $0DC7). If you wonder, yes, it's as useless as hell (and as evil too).

**What if I make some mistake in the code?**

Good luck. You are gonna need it. While it is shown what the culprit instruction is, you will not generally receive any hint regarding the nature of the error. Moreover, if you make a mistake in a subroutine or function, the error will appear only when you call it. This might lead you to believe the mistake lies in the JUMP/CALL instruction shown by the interpreter. Always double-check the subroutine(s) or function(s) referenced by JUMP/CALL instructions.

**How do I comment the code?**

Lines that start with ; will be treated as comments. In-line comments aren't allowed.

**How do I run mlmcr?**

__If you have a *COMPILED* version of mlmcr:__
- Launch a terminal session (if you want).
- Navigate into the directiory where `mlmcr.exe` is (or open it directly in a file browser).
- To launch the mlmcr interpreter, write (without quotes): `mlmcr.exe`
- To execute a `.mlmcr` file, write: `mlmcr.exe <file_path>`

__If you have a *SOURCE* version of mlmcr:__
- Launch a terminal session.
- Navigate into the directory where the `mlmcr.py` script is.
- To launch the mlmcr interpreter, write (without quotes): `python mlmcr.py`
- To execute a `.mlmcr` file, write: `python mlmcr.py <file_path>.mlmcr`

*__Make sure to read variable naming conventions in the manual!__*

*__SHORT INSTRUCTION GUIDE__*

Currently, mlmcr has 89 instructions to work with.

*__VARIABLES__*

**PUT** - assign a value to a variable

**DEL** - delete a variable

**NEW** - create a new instance of a variable's type

**SWAP** - swap two variables

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

**ABS** - calculate the absolute value of a variable or number

**SQRT** - calculate the square root of a variable or number

**CBRT** - calculate the cube root of a variable or number

**INC** - increment a variable

**DEC** - decrement a variable

**PUSH** - print things to screen

**PULL** - get a variable from user input

**INT** - convert a floating-point number or a string to an integer number

**FLPT** - convert an integer number or a string to a floating-point number

**STR** - convert an integer number or a floating-point number to a string

**BOOL** - convert a variable to a boolean

**NULL** - put NULL/None in a variable

**TYPE** - check the type of a value

**LINK** - join two strings together

**FSTR** - split a string into a sequence

**TSTR** - join a sequence into a string

**MIN** - get the minimum value

**MAX** - get the maximum value

*__ARRAYS__*

**SEQ** - build a sequence

**PSEQ** - build a permanent sequence

**PACK** - pack variables

**MAP** - build a map

**JOIN** - add items to an array

**NEST** - add an array to an array

**POP** - remove an item from an array based on its index

**REM** - remove an item from an array based on its value

**GETI** - get the index of a value in an array

**GET** - get a value in an array based on its index

**REST** - get part of an array

**SET** - insert a value in array before a given index

**REPL** - replace a value in an array based on its index

**MSET** - set an item in a map

**MGET** - get a value from a key in a map

**MPOP** - remove an item from a map based on its key

**MPLI** - remove and store the last item from a map

**GRAB** - get all key-value pairs from a map

**KEYS** - get all keys from a map

**VALS** - get all values from a map

**LEN** - get the lenght of an array

**WIPE** - clear an array of its items

**COPY** - create a shallow copy of an array

*__OPERATORS__*

**EQ** - check if two values are equal

**NE** - check if two values are not equal

**GT** - check if a value is greater than another

**LT** - check if a value is less than another

**GE** - check if a value is greater than or equal to another

**LE** - check if a value is less than or equal to another

**AND** - check if two values are both true

**OR** - check if at least a value is true

**NOT** - reverse a value

**IS** - check if two values are the same

**IN** - check if a value is in an array

*__CONTROL FLOW__*

**IF** - the if equivalent in mlmcr

**ELIF** - the else if equivalent in mlmcr

**ELSE** - the else equivalent in mlmcr

**FOR** - the for equivalent in mlmcr

**FORI** - the indexed for equivalent in mlmcr

**ALA** - the while equivalent in mlmcr

**DALA** - the do-while equivalent in mlmcr

**LOOP** - create a sequence of integers respecting a specificed set of rules

*__SUBROUTINES & FUNCTIONS__*

**SUBR** - create a subroutine
- **RTS** - end a subroutine

**JUMP** - call a subroutine

**FUNC** - create a function
- **TAKE** - copy a global variable into a local variable in a function
- **SYNC** - copy a local variable into a global variable in a function
- **GIVE** - return a value from a function
- **END** - end a function

**CALL** - call a function

*__OTHER INSTRUCTIONS__*

**RAND** - get a random integer

**HALT** - delay code execution

**EXIT** - quit the current script or interpreter

**PYEVAL** - evaluate a Python expression

**PYEXEC** - execute Python code
