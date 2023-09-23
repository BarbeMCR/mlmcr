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

What about a slightly more complex example?
```
push #1, & + , #2, & = , #3
```
This will print "1 + 2 = 3".

Here `push` is the same as before, but we have more than one argument this time. In fact, we have 5: `#1`, `& + `, `#2`, `& = ` and `#3`.
We use commas to separate the arguments.

You need to be very careful when passing arguments, since their amount, their order and their prefixes all count.

If you want to save any program for later usage, you can put the instructions in a text editor and tell it to save the file with a `.mlmcr` extension.
