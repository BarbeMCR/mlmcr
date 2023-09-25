## Arrays

In mlmcr, there are 5 builtin array types: sequences, permasequences, packs, maps and loops.

### Sequences

mlmcr sequences are the same as Python's `list`s.
You can create them with the `SEQ` opcode:
```
SEQ var, items...  (var:->{SEQ}, items...:*)

SEQ ->$0, #1, &test  ;;$0: [1, 'test']
```
During the initialization of a sequence, there can be one or more items to immediately append to it.

### Permasequences

Permasequences are not wrappers for a standard Python type. Instead, they wrap `mlmcr.PermaSequence` instances (which are built upon `list`, though).
We'll talk about its differences from sequences later.
You can create them with the `PSEQ` opcode:
```
PSEQ var, items...  (var:->{PSEQ}, items...:*)

PSEQ ->$0, #1, &test  ;;$0: P[1, 'test']
```

### Packs

mlmcr packs are the same as Python's `tuple`s.
You can create them with the `PACK` opcode:
```
PACK var, items...  (var:->{PACK}, items...:*)

PACK ->$0, #1, &test  ;;$0: (1, 'test')
```
Packs can't be changed after they are created, so you should include some items in its definition.

### Maps

mlmcr maps are the same as Python's `dict`s.
You can create them with the `MAP` opcode:
```
MAP var  (var:->{MAP})

MAP ->$0  ;;$0: {}
```
You can't add items to maps on initialization, but you can at any later time.

### Loops

mlmcr loops are the same as Python's `range`s.
You can create them with the `LOOP` opcode:
```
LOOP [start], stop, [step], var  (start:INT, stop:INT, step:INT, var:->{LOOP})

LOOP #5, ->$0  ;;$0 -> {0, 1, 2, 3, 4}
LOOP #2, #5, ->$0  ;;$0 -> {2, 3, 4}
LOOP #1, #5, #2, ->$0  ;;$0 -> {1, 3}
LOOP #10, #7, #-1, ->$0  ;;$0 -> {10, 9, 8}
```
You need to specify a `start` parameter to use the `step` parameter.
All parameters can be `0` or negative. Negative steps make the range work backwards.

### Comparison of arrays

|     | Sequences | Permasequences | Packs | Maps | Loops |
| --- | --------- | -------------- | ----- | ---- | ----- |
| Can iterate through it    | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Can get items from it     | ✔️ | ✔️ | ✔️ | ✔️ | :x: |
| Can append items to it    | ✔️ | ✔️ | :x: | ✔️ | :x: |
| Can modify or delete existing items | ✔️ | :x: | :x: | ✔️ | :x: |

It is also worth noting that sequences, permasequences and packs share the same opcodes for managing their items, since they all use indexes, while maps have their own opcodes, since they use keys.

### Tools for sequences, permasequences and packs

There are several opcodes aimed to sequence, permasequence and pack management. All use the same format: `<opcode> <array>, <arguments>` (e.g. `JOIN ->$0, #1`).
Here is a list of all builtin ones:
- `JOIN` to append items to arrays *(not supported by packs)*
- `NEST` to extend arrays with other iterables' items *(not supported by packs)*
- `POP` to pop items from arrays, based on their indexes, returning them *(not supported by permasequences and packs)*
- `REM` to remove items from arrays, based on their values *(not supported by permasequences and packs)*
- `GETI` to get the index of a value in an array
- `GET` to get a value in an array based on its index
- `REST` to get part of an array
- `SET` to insert an item in an array before an index *(not supported by permasequences and packs)*
- `REPL` to replace an item with another *(not supported by permasequences and packs)*
- `COUNT` to count the number of times a value is present in an array
- `RVRS` to reverse an array in-place *(not supported by permasequences and packs)*
- `SORT` to sort an array in-place *(not supported by permasequences and packs)*
- `RSORT` to sort an array in-place, in reverse order *(not supported by permasequences and packs)*
- `LEN` to get the length of an array **_(also works on maps, loops and strings)_**
- `WIPE` to clear an array of its items *(__also works on maps__, but isn't supported by packs)*
- `COPY` to make a copy of an array, without creating a pointer to the original array *(__also works on maps__, but isn't supported by packs)*

```
JOIN to, items...  (to:<->{SEQ|PSEQ}, items...:*)
NEST to, iters...  (to:<->{SEQ|PSEQ}, iters...:SEQ|PSEQ|PACK|MAP|LOOP|STR)
POP from, index, [store]  (from:<->{SEQ}, index:INT, store:->{*})
REM from, item  (from:<->{SEQ}, item:*)
GETI from, item, store  (from:SEQ|PSEQ|PACK, item:*, store:->{*item})
GET from, index, store  (from:SEQ|PSEQ|PACK, index:INT, store:->{*})
REST from, start, [stop], [step], store  (from:SEQ|PSEQ|PACK, start:INT, stop:INT, step:INT, store:->{*from})
SET to, index, item  (to:<->{SEQ}, index:INT, item:{*})
REPL to, index, item  (to:<->{SEQ}, index:INT, item:{*})
COUNT from, item, store  (from:SEQ|PSEQ|PACK, item:*, store:->{INT})
RVRS what  (what:<->{SEQ})
SORT what  (what:<->{SEQ})
RSORT what  (what:<->{SEQ})
LEN what, store  (what:SEQ|PSEQ|PACK|MAP|LOOP|STR, store:->{INT})
WIPE what  (what:<->{SEQ|PSEQ|MAP})
COPY what, to  (what:SEQ|PSEQ|MAP, to:->{*what})
```
I won't include any example here because I feel those opcodes should be pretty intuitive. You can experiment with them in the mlmcr interpreter if you want anyways.
Also, the meaning of the arguments is included in the *core opcodes table*.

### Tools for maps

There are also several opcodes aimed at map management. Here they are:
- `MSET` for setting a key to a value
- `MGET` for getting a key's value
- `MPOP` to remove a key-value pair
- `MPLI` to pop the last key-value pair added and return it
- `GRAB` to get a pack of all key-value packs
- `KEYS` to get a pack of all keys
- `VALS` to get a pack of all values

```
MSET map, key, value  (map:<->{MAP}, key:*, value:*)
MGET map, key, store  (map:MAP, key:*, store:->{*})
MPOP map, key, [store]  (map:<->{MAP}, key:*, store:->{*})
MPLI map, pair  (map:<->{MAP}, pair:->{PACK})
GRAB map, pairs  (map:MAP, pairs:->{PACK})
KEYS map, keys  (map:MAP, keys:->{PACK})
VALS map, values  (map:MAP, values:->{PACK})
```
