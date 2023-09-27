## Libraries

mlmcr can be extended natively through the use of libraries.
Libraries are `.mlmch` (mlmcr header) files which hold a series of instructions, and are run on demand (during import).
mlmcr headers can contain any kind of instruction, but are usually full of definitions and opcode bindings.

### Using libraries

If you just want to import a library, you can use the `USE` opcode:
```
USE path  (path:>>)

USE >>slice  ;; We put the path in lowercase to indicate that it is an actual file path and not a just a reference name
```
`USE` runs the file at `<path>.mlmch` in its own namespace, which gets automatically created before importing.
The name of the created namespace is `path`, unless the library used the `NAME` opcode (see below).

In our example, `slice` didn't do any `NAME` call, so we can call its contents with the `SLICE.` prefix.

`path` can also include directory paths (e.g. in `USE >>cores/arithmetics`).

### The `NAME` opcode

`NAME` is a very important opcode, as it allows any library to change its reference name from within itself, keeping all the previously defined content intact.
This is its opcode definition:
```
NAME name  (name:>>)

NAME >>TEST
```
In this example, the namespace created for the library `NAME` was called in would change its name to `TEST`.

`NAME` can also be used in a hacky way to make opcodes and variables core. This is done by calling `NAME >>_DEFAULT`.
This trick is used in all cores.

For example, the `ADD` opcode is actually defined in `./cores/arithmetics.mlmch`, which would cause it to be referenced only through `ARITHMETICS.ADD`.
However, since `arithmetics.mlmch` calls `NAME >>_DEFAULT`, we can use the opcode as simply `ADD`.

After calling `NAME`, the old namespace is removed.
