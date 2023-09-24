## Arithmetics

mlmcr supports several arithmetic operations out-of-the-box. We'll explore them in this document.

### Standard arithmetics

mlmcr supports addition, subtraction, multiplication, division, floor division, modulo, power and absolute value computation through the `ADD`, `SUB`, `MUL`, `DIV`, `FDIV`, `MOD`, `POW` and `ABS` opcodes:
```
As you can see, wDD a, b, c..., result  (a+b+c...:INT|FLPT, result:->{INT|FLPT})`step` is not provided, it is assumed to be `1`.

When you need another type of in-place operation, you should refer to the `opcode var, term, ->var` syntax (which is essentially the same as, for example, `a = a // b` in Python).

### Signs

mlmcr provides two opcodes for changing the sign of values: `POS` and `NEG`.

`POS` (positive) stores the value of 
SUB a, b, c..., result  (a+b+c...:INT|FLPT, result:->{INT|FLPT})
MUL a, b, c..., result  (a+b+c...:INT|FLPT, result:->{INT|FLPT})
DIV a, b, c..., result  (a+b+c...:INT|FLPT, result:->{FLPT})
FDIV a, b, c..., result  (a+b+c...:INT|FLPT, result:->{INT})
MOD a, b, c..., result  (a+b+c...:INT|FLPT, result:->{INT})
POW a, b, c..., result  (a+b+c...:INT|FLPT, result:->{INT|FLPT})
ABS n, absn  (n:INT|FLPT, absn:->{INT|FLPT})

ADD #1, #2, ##3.4, ->$0  ;;$0: 6.4
SUB #5, ##2.2, #3, ->$0  ;;$0: -0.2
MUL #4, #3, #1.5, ->$0  ;;$0: 18
DIV #25, #10, ->$0  ;;$0: 2.5
FDIV #25, #10, ->$0  ;;$0: 2
MOD #25, #10, ->$0  ;;$0: 5
POW #2, #3, ->$0  ;;$0: 8
ABS #-3.14, ->$0  ;;$0: 3.14
```
Here `a+b+c...:INT|FLPT` is a compact way of saying `a:INT|FLPT, b:INT|FLPT, c...:INT|FLPT`. This is non-standard, however, so use it carefully when documenting.

### In-place arithmetics

mlmcr also supports some in-place operations (i.e. those that directly modify a variable): in-place addition, in-place subtraction, in-place multiplication and in-place division.

They are provided by the `INC` (increment), `DEC` (decrement), `IMUL` (in-place multiply) and `IDIV` (in-place divide) opcodes:
```
INC var, [step]  (var:<->{INT|FLPT}, step:INT|FLPT)
DEC var, [step]  (var:<->{INT|FLPT}, step:INT|FLPT)
IMUL var, [step]  (var:<->{INT|FLPT}, step:INT|FLPT)
IDIV var, [step]  (var:<->{FLPT}, step:INT|FLPT)

INC ->$0, #2  ;;ADD $0, #2, ->$0
DEC ->$0  ;;SUB $0, #1, ->$0
IMUL ->$0, ##3.14  ;;MUL $0, ##3.14, ->$0
IDIV ->$0, #5  ;;DIV $0, #5, ->$0
```
As you can see, when `step` is not provided, it is assumed to be `1`.

When you need another type of in-place operation, you should refer to the `opcode var, term, ->var` syntax (which is essentially the same as, for example, `a = a // b` in Python).

### Signs

mlmcr provides two opcodes for changing the sign of values: `POS` and `NEG`.

`POS` (positive) stores the value of `+var`, while `NEG` (negative) that of `-var`:
```
POS var, store  (var:INT|FLPT, store:->{INT|FLPT})
NEG var, store  (var:INT|FLPT, store:->{INT|FLPT})

POS #-1, ->$0  ;;$0: -1
NEG #-1, ->$0  ;;$0: 1
```

Keep in mind that `POS` and `NEG` do not make a value inherently positive or negative (as seen in the example).
To do that, you can use `ABS` to force positivity and `ABS` followed by `NEG` to force negativity.

### Other uses of arithmetic operators

Some arithmetic operators can be used to do other things as well, in particular:
- `ADD` can be used to concatenate strings
- `ADD` can be used to merge sequences and permasequences
- `MUL` can be used to repeat a string (e.g. in `MUL &t, #3, ->$0`, `$0` will be `'ttt'`)
- `MUL` can be used to repeat sequences and permasequences, in the same way as strings

`INC` and `IMUL` can also be used instead of `ADD` and `MUL` if the user wants to overwrite the original string, sequence or permasequence, and only one other term is needed.

Keep in mind that, when using `MUL` and `IMUL` to repeat strings, sequences and permasequences, only the first term must be one of those types.
