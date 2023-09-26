## Namespaces

In mlmcr, variables and opcodes are grouped in namespaces, which are a core part of coding in this language.
A namespace is created every time you import a library or run a function (or lambda).

### Managing namespaces

Apart from the means I already mentioned, it is also possible to create a namespace at will, thanks to the `MAKE` opcode:
```
MAKE ns, [rule]  (ns:>>, rule:>>)

MAKE >>TEST, >>_
```
In this opcode definition, the `ns` argument is what you'd expect: it's the name of the namespace to be created.
To understand `rule`, however, we have to talk a bit deeper about namespaces.

You see, in order to specify different prefixes for variables in different scopes, mlmcr uses a system of rules.
For example, in most namespaces, the `mlmcr.Namespace._pref` attribute (which determines the rule for that namespace) is set to `$`.
Also as an example, in function namespaces, that attribute is set to `@`.
This causes standard variables to have names such as `$0` or `@0` depending on they type of namespace they're in.

In our example, the `TEST` namespace would have its rule set to `_`, and variables would be built like this: `_0`.

Obviously, we can also delete namespaces. This is done through the `DUMP` opcode:
```
DUMP ns  (ns:>>)

DUMP >>TEST
```

Additionally, we can rename and copy them, with the `REN` and `CLONE` opcodes, respectively:
```
REN from, to  (from:>>, to:>>)
CLONE ns, to  (ns:>>, to:>>)

REN >>TEST, >>STUFF  ;; TEST becomes STUFF
CLONE >>TEST, >>STUFF  ;; TEST is cloned into STUFF
```

### Adding opcodes

Now that we have talked a bit about namespaces, I have a question for you: where do you think all the opcodes we have mentioned until here came from?

If you answered the `_DEFAULT` namespace, you are right! We have encountered it before, when talking about variables.
But this namespace is also the source of opcodes too. If you aren't specifying a namespace, `_DEFAULT` will in fact be inspected for the opcode you requested.

But how do we add opcodes to namespaces?

There are actually two answers:
- with the `BIND` opcode, when we have a function and we want to make it work as an opcode
- with the `WRAP` opcode, when we already have an opcode and we want to copy it

Here are the opcode definitions:
```
BIND func, opcode  (func:FUNC, opcode:>>)
WRAP opcode, into  (opcode:F>>, into:F>>)

BIND $1000, >>THIS.THINGS  ;; Here opcode THINGS in the current namespace was created from whatever is at $1000
WRAP >>PUSH, >>TEST.MYPUSH  ;; Here opcode MYPUSH in namespace TEST was copied from _DEFAULT.PUSH
```

One important thing to note is that any function can become an opcode, simply by planning it ahead and handling eventual errors (and using `BIND`).
