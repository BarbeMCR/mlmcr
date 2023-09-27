## Introduction

Welcome to the wonderful world of mlmcr! This is the documentation, where you'll (hopefully) learn how to code in this weird language.

To start off, as the tradition says, we'll make the classic "Hello, world!" program:
```
push &Hello/,/ world!  ;; Prints "Hello, world!"
```
Let's analyze this instruction token by token:
- `push` is the opcode, which it dictates which operation must be done: here `push` prints stuff to the console window
- `&Hello/,/ world!` is an argument, which is used to send data to the opcode: it has the `&` prefix, which is used to indicate a string. I'll explain later what the `/,/` part is.
- `;; Print "Hello, world!"` is a comment. When a `;;` is hit in an instruction, everything past it will get ignored.

Instructions are case-insensitive, meaning that `push &test`, `PUSH &test` and `pUsH &test` will all print `'test'`. However, strings are case-sensitive, so `PUSH &TEST` will print `'TEST'` instead.

What about a slightly more complex example?
```
push #1, & + , #2, & = , #3
```
This will print "1 + 2 = 3".

Here `push` is the same as before, but we have more than one argument this time. In fact, we have 5: `#1`, `& + `, `#2`, `& = ` and `#3`.
We use commas to separate the arguments.

You need to be very careful when passing arguments, since their amount, their order and their prefixes all count.

To end your mlmcr session, you can use the `EXIT` opcode:
```
EXIT [excode]  (excode:INT)

EXIT
EXIT #1
```
You can pass an integer to `EXIT` in order to set an exit code (the default is `0`).

If you want to save any program for later usage, you can put the instructions in a text editor and tell it to save the file with a `.mlmcr` extension.

Let's now do a little thing: we'll describe what each line in the sample program in the home page does:
```
seq ->$0  ;; Initialize the empty sequence [] at $0
pull ->$10, &How many values to insert?   ;; Print "How many values to insert? " and store the user input in $10
int $10, ->$10  ;; Convert $10 from string to integer
loop $10, ->$a0  ;; Create a loop that goes from 0 to $10 and store it in $a0
subr ->$1000  ;; Define a subroutine at $1000
    pull ->$a, &Insert value:   ;; Print "Insert value: " and store the user input in $a
    flpt $a, ->$a  ;; Convert $a from string to float
    join <->$0, $a  ;; Append $a to $0
rts  ;; Return from subroutine $1000
for ->$ff, $a0, $1000  ;; Call $1000 for every item $ff in $a0
func ->$1001, >@1, >@a  ;; Define a function $1001: it takes @1 and @a as parameters
    do ->@10010, >@a, :inc ->@a  ;; Define a lambda which increases its parameter @a at @10010
    snag <->@10010, >@a  ;; Tell lambda @10010 to return its variable @a
    call @10010, @a, ->@a  ;; Call @10010 with argument @a and store the return value in @a
    put $0, ->@0  ;; copy $0 into @0
    repl <->@0, @1, @a  ;; Replace the item at index @1 with @a in @0
end  ;; Return from function $1001
fori ->$f1, ->$f0, $0, $1001, ^$f1, ^$f0, ->$ff  ;; Call $1001 for every index $f1 and item $f0 in $0 (storing the return value in $ff)
push $0  ;; Print $0
```
