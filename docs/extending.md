## Extending mlmcr

mlmcr is an extensible language, which means that its functionality can be expanded by using its implementation language, Python.

We can run Python code natively inside mlmcr scripts, by typing `PYBLOCK` (to start a Python block) and `PYEND` (to end it).
`PYBLOCK` and `PYEND` are the only opcodes which are truly hardcoded, since are needed to do everything in Python.

When we type `PYBLOCK`, the mlmcr interpreter will start saving everything that comes afterwards, until it hits a `PYEND`.
Then, the entire block is immediately executed as Python code from inside `mlmcr.run`.

We can use pyblocks to, for instance, define functions. This way we can implement new opcodes by wrapping them around Python code, with the help of `mlmcr.bind`.

As an example of a Python extension, take the code for the `USE` opcode:
```python
def use_mlmch(args):
    def _use_mlmch(args):
        if check(args[0], str):
            import_mlmch(args[0])
        else:
            typeErr(0)
    when(_use_mlmch, args, 1)

[...]

bind(use_mlmch, 'USE')
```
In this context, `check`, `import_mlmch`, `typeErr`, `when` and `bind` are all part of the mlmcr API.

You can do pretty much whatever you want inside pyblocks, so get creative if you want to build a native library!
