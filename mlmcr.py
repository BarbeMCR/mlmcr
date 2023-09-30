#!/usr/bin/env python3

# mlmcr, the unnecessary Assembly-like programming language
# Copyright (C) 2023  BarbeMCR

from typing import Any, Self, Iterable

import sys
import os
import re
import itertools

# Builtin classes
class MlmcrError(Exception):
    pass

class ThisLookupError(Exception):
    def __init__(self, ref: str) -> None:
        self.ref = ref

class PermaSequence:
    def __init__(self, *items: tuple) -> None:
        self.sequence = [*items]
    def __getitem__(self, index: slice | int) -> Self | Any:
        if isinstance(index, slice):
            return PermaSequence(*self.sequence.__getitem__(index))
        return self.sequence.__getitem__(index)
    def __reversed__(self):
        return reversed(self.sequence)
    def __contains__(self, value: Any) -> bool:
        return value in self.sequence
    def __len__(self) -> int:
        return len(self.sequence)
    def __iter__(self) -> Any:
        return iter(self.sequence)
    def __str__(self) -> str:
        return f'P{str(self.sequence)}'
    def __add__(self, value: Any) -> list:
        return self.sequence + value
    def __mul__(self, value: int) -> list:
        return self.sequence * value
    def __eq__(self, value: Any) -> bool:
        return self.sequence == value
    def __ne__(self, value: Any) -> bool:
        return self.sequence != value
    def __gt__(self, value: Any) -> bool:
        return self.sequence > value
    def __lt__(self, value: Any) -> bool:
        return self.sequence < value
    def __ge__(self, value: Any) -> bool:
        return self.sequence >= value
    def __le__(self, value: Any) -> bool:
        return self.sequence <= value
    def __reduce__(self) -> str | tuple[Any, ...]:
        return self.sequence.__reduce__()
    def append(self, item: Any) -> None:
        self.sequence.append(item)
    def extend(self, item: Iterable) -> None:
        self.sequence.extend(item)
    def count(self, value: Any) -> int:
        return self.sequence.count(value)
    def index(self, value: Any) -> int:
        return self.sequence.index(value)
    def clear(self) -> None:
        self.sequence.clear()
    def copy(self) -> Self:
        return PermaSequence(*self.sequence.copy())

class Namespace:
    def __init__(self, _name: str, _pref: str = '$') -> None:
        self._name = _name
        self._vars = {}
        self._pref = _pref  # This is used for error reporting
        _npref = ''.join(map(lambda c: f'\{c}' if c in {'\\', '|', '$', '/', '(', ')', '?', '^', '[', ']', '+', '*', '-', '.', ':', '<', '>', '=', '!'} else c, _pref))
        self._matcher = re.compile(rf'^{_npref}[\da-f]+$', re.IGNORECASE)
        self._ops = {}
        self.kill_list = KillList()
        self.subspaces = {}
        self.current_subspace = None

    def copy(self, other: Self) -> None:
        for k, v in other._vars.items(): self._vars[k] = v
        for k, v in other._ops.items(): self._ops[k] = v
        for k, v in other.subspaces.items(): self.subspaces[k] = v
        self.kill_list.copy(other.kill_list)

    def set_var(self, name: str, value: Any) -> None:
        if self._matcher.match(name):
            self._vars[name] = value
        else:
            nameFormatError(name, self._pref)

    def get_var(self, name: str) -> Any | None:
        if name in self._vars:
            return self._vars[name]
        else:
            genericNameError(name, self._name)

    def del_var(self, name: str) -> None:
        if name in self._vars:
            del self._vars[name]
        else:
            genericNameError(name, self._name)

    def new_op(self, op: str, ref: object) -> None:  # ref: function (python functions) | Function
        self._ops[op.upper()] = ref

    def call_op(self, op: str, args: list[str]) -> None:
        if op in self._ops:
            global current_op
            current_op = op
            try:
                # Redirects this calls in function opcodes to point to the <function> opcode
                if [f for f in stack if hasattr(f,'scope') and f.scope==this(get_parent=True)]:
                    s = get_subspace(get_parent=True)
                    pop_subspace()
                    if isinstance(self._ops[op], Callable):
                        _op = self._ops[op]
                        if (len(args)==len(_op.argdefs)) or (len(args)>=len(_op.argdefs) and _op.has_catchall()):
                            call(_op, args)
                        else:
                            append_subspace(s)
                            wrongCallableArguments(len(args), len(_op.argdefs), _op.has_catchall())
                    else:
                        self._ops[op](args)
                    append_subspace(s)
                else:
                    if isinstance(self._ops[op], Callable):
                        _op = self._ops[op]
                        if (len(args)==len(_op.argdefs)) or (len(args)>=len(_op.argdefs) and _op.has_catchall()):
                            call(_op, args)
                        else:
                            wrongCallableArguments(len(args), len(_op.argdefs), _op.has_catchall())
                    else:
                        self._ops[op](args)
                if not stack:
                    backup()
            except TypeError:
                opFormatError(self._name, op)
        else:
            invalidOpError(self._name, op)

    def kill_var(self, name: str) -> int | None:
        if name in self._vars:
            if self.kill_list.max_len > -1:
                if len(self.kill_list._kills) < self.kill_list.max_len:
                    del self._vars[name]
                    return self.kill_list.kill(self._vars[name])
                else:
                    killListFullError(self._name, self.kill_list.max_len, name)
            else:
                t = self.kill_list.kill(self._vars[name])
                del self._vars[name]
                return t
        else:
            genericNameError(name, self._name)

    def unkill_var(self, ticket: int, var: str) -> None:
        if ticket in self.kill_list._kills:
            self.set_var(var, self.kill_list.unkill(ticket))
        else:
            killTicketError(ticket, self._name)

    def add_subspace(self, subspace: Self) -> None:
        if hasattr(subspace, '_name'):
            self.subspaces[subspace._name] = Namespace(subspace._name, subspace._pref)
            self.subspaces[subspace._name].copy(subspace)
        else:
            namespaceFormatError(subspace.__name__)

class KillList:
    def __init__(self) -> None:
        self._kills = {}
        self.max_len = -1

    def copy(self, other: Self) -> None:
        for k, v in other._kills.items(): self._kills[k] = v

    def kill(self, var: Any) -> int:
        ticket = len(self._kills)
        self._kills[ticket] = var
        return ticket

    def unkill(self, ticket: int) -> Any:
        var = self._kills[ticket]
        del self._kills[ticket]
        return var

class CatchAll:
    def __init__(self, name: str) -> None:
        self.name = name

class LookBack:
    def __init__(self, backref: str) -> None:
        self.backref = backref

class Break(Exception):
    pass

class Continue(Exception):
    pass

class Return(Exception):
    def __init__(self, depth: int, value: Any = None) -> None:
        self.depth = depth
        self.value = value

class Definable:
    def __init__(self):
        self.defline = n
        self.body = []
    def add_instruction(self, instruction: str) -> None:
        self.body.append(instruction)

class Callable(Definable):
    def __init__(self, argdefs: list[str]) -> None:
        super().__init__()
        self.scope = Namespace('<fallback>', '@')
        self.argdefs = argdefs
        self.parent = Namespace('<fallback>')
    def __call__(self, args: list[Any], parent: Namespace) -> None:
        pass  # This is a fallback method to avoid getting an exception
    def has_catchall(self) -> bool:
        return sum(isinstance(a, CatchAll) for a in self.argdefs)

class Function(Callable):
    def __init__(self, argdefs: list[str]) -> None:
        super().__init__(argdefs)

    def __call__(self, args: list[Any], parent: Namespace) -> Any:
        global context_type
        # Scope preparation
        self.parent = parent
        self.scope = Namespace('<function>', '@')
        self.scope.add_subspace(namespaces['_DEFAULT']) if '_DEFAULT' in namespaces else invalidNamespaceError('_DEFAULT')
        self.scope.add_subspace(Namespace('EXT', '@'))
        # Argument binding
        for i, data in enumerate(zip(self.argdefs, args)):
            if isinstance(data[0], CatchAll):
                self.scope.set_var(data[0].name, args[i:])
            else:
                self.scope.set_var(data[0], data[1])
        _context = context_type
        context_type = 'function'  # This adjusts the context type for error reporting purposes
        # Body execution
        try:
            run(self.body)
        except Return as r:
            if current_subspace_needs_cleanup:
                pop_subspace()
                current_subspace_needs_cleanup.pop()
            if r.depth <= 0:
                context_type = _context
                return r.value
            else:
                stack_needs_pop.append(True)
                r.depth -= 1
                raise r

    def add_instruction(self, instruction: str) -> None:
        global deflen
        super().add_instruction(instruction)
        match instruction.lstrip().split(' ', maxsplit=1)[0].upper():
            case 'END':
                if deflen > 1: deflen -= 1
                else: end_define()
            case 'RTS' | 'ECLS':
                if deflen > 1: deflen -= 1
            case 'FUNC' | 'SUBR' | 'CLS':
                deflen += 1

class Subroutine(Definable):
    def __call__(self, args: list[Any], parent: Namespace) -> None:
        # Warning: args gets discarded!
        global context_type
        self.parent = parent  # parent is set up purely for intercompatibility purposes
        _context = context_type
        context_type = 'function'  # This adjusts the context type for error reporting purposes
        run(self.body)  # Body execution
        context_type = _context

    def add_instruction(self, instruction: str) -> None:
        global deflen
        super().add_instruction(instruction)
        match instruction.lstrip().split(' ', maxsplit=1)[0].upper():
            case 'RTS':
                if deflen > 1: deflen -= 1
                else: end_define()
            case 'END' | 'ECLS':
                if deflen > 1: deflen -= 1
            case 'FUNC' | 'SUBR' | 'CLS':
                deflen += 1

class Lambda(Callable):
    def __init__(self, argdefs: list[str]) -> None:
        super().__init__(argdefs)

    def __call__(self, args: list[Any], parent: Namespace) -> Any:
        global context_type
        # Scope preparation
        self.parent = parent
        self.scope = Namespace('<lambda>', '@')
        # Namespace imports
        if self.parent in namespaces.values():
            for k, v in namespaces.items():
                self.scope.subspaces[k] = v  # A pointer to v gets created here (not a copy!):
                                             # modifications to the lambda scope also get applied in the parent scope
        else:
            for k, v in self.parent.subspaces.items():
                self.scope.subspaces[k] = v
        # Argument binding
        for i, data in enumerate(zip(self.argdefs, args)):
            if isinstance(data[0], CatchAll):
                self.scope.set_var(data[0].name, args[i:])
            else:
                self.scope.set_var(data[0], data[1])
        _context = context_type
        context_type = 'lambda'  # This adjusts the context type for error reporting purposes
        # Body execution
        try:
            run(self.body)
        except Return as r:
            if current_subspace_needs_cleanup:
                pop_subspace()
                current_subspace_needs_cleanup.pop()
            if r.depth <= 0:
                context_type = _context
                return r.value
            else:
                stack_needs_pop.append(True)
                r.depth -= 1
                raise r

    def add_instruction(self, instruction: str) -> None:
        super().add_instruction(instruction)
        match instruction.lstrip().split(' ', maxsplit=1)[0].upper():
            case 'END' | 'RTS' | 'ECLS':
                cantUseOpHere()
            case 'FUNC':
                cantDefineHere("functions", "lambdas")
            case 'SUBR':
                cantDefineHere("subroutines", "lambdas")
            case 'CLS':
                cantDefineHere("classes", "lambdas")

class LambdaApplicator:
    def __init__(self, ref: Lambda):
        self.ref = ref

class Class:
    pass

# Core global variables
namespaces = {
    '_DEFAULT': Namespace('_DEFAULT')  # This is a hidden namespace where all core instructions reside
}
registers = {
    'N': None,
    'T': True,
    'F': False,
    'MLMCR.VER': (3, 0),
    'MLMCR.HUMANVER': '3.0',
    'MLMCR.AUTHOR': "Made with love (and hate) by BarbeMCR <3",
    'MLMCR.COPYRIGHT': "Copyright (C) 2023  BarbeMCR",
    'MLMCR.PYVER': f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
}
stack = []
current_namespace = '_DEFAULT'
if_stack = []
trying = False
aced_try = False
defining = None
deflen = 0
error = False
current_error = ('Unknown error', 'if you see this, please file a bug report')  # This should never be seen during normal use
caught_error = ('', '')  # Same here
context_type = 'main'
backups = {
    'namespaces': namespaces,
    'registers': registers,
    'stack': stack,
    'current_namespace': current_namespace,
    'if_stack': if_stack,
    'trying': trying,
    'aced_try': aced_try,
    'defining': defining,
    'deflen': deflen,
    'context_type': context_type
}

# Specialized global variables (some with placeholder values)
n = 0
s = '...'  # It's run's source, but renamed to avoid name clashing
in_pyblock = False
pyblock = []
current_op = None
stack_needs_pop = []
current_subspace_needs_cleanup = []

# Core imports
cores = (
    'packinghelpers',
    'vartools',
    'arithmetics',
    'consoleio',
    'typeconverters',
    'basicutilities',
    'arraydefs',
    'arrayops',
    'mapops',
    'operators',
    'procs',
    'stockif',
    'controlflow',
    'stocktry',
    'registers'
    #'classes'
)

def backup(var: str | None = None) -> None:
    if var is None:
        for v in backups:
            backups[v] = eval(v) if not isinstance(eval(v), (set, list, dict)) else eval(v).copy()
    else:
        backups[var] = eval(var) if not isinstance(eval(var), (set, list, dict)) else eval(var).copy()

def restore(var: str | None = None) -> None:
    if var is None:
        for v in backups:
            globals()[v] = backups[v]
    else:
        globals()[var] = backups[var]
    while this().current_subspace:
        try:
            pop_subspace()
        except ThisLookupError:
            pass

def new_register(name: str) -> None:
    parts = name.split('.')
    lparts = len(parts)
    if lparts <= 2:  # If there is more than one dot
        if lparts == 1:
            if len(parts[0]) <= 3:
                registers[name] = None
            else:
                invalidRegisterName(name)
        else:
            if len(parts[0])<=8 and len(parts[1])<=3:
                registers[name] = None
            else:
                invalidRegisterName(name)
    else:
        invalidRegisterName(name)

def set_register(name: str, value: Any) -> None:
    if name in registers:
        registers[name] = value
    else:
        invalidRegister(name)

def get_register(name: str) -> Any | None:
    if name in registers:
        return registers[name]
    else:
        invalidRegister(name)

def del_register(name: str) -> None:
    if name in registers:
        del registers[name]
    else:
        invalidRegister(name)

def new_namespace(name: str, _from: str, pref: str = '$') -> None:
    if _from == '_DEFAULT':
        if name not in namespaces:
            namespaces[name] = Namespace(name, pref)
    else:
        if name not in this(get_parent=True).subspaces:
            this(get_parent=True).add_subspace(Namespace(name, pref))

def rename_namespace(old: str, new: str) -> None:
    global current_namespace
    if old in this().subspaces:
        new_namespace(new, new, this().subspaces[old]._pref)
        del this().subspaces[old]
        append_subspace(new)
    elif old in namespaces:
        new_namespace(new, new, namespaces[old]._pref)
        namespaces[new].copy(namespaces[old])
        del namespaces[old]
        current_namespace = new
    else:
        invalidNamespaceError(old)

def delete_namespace(ns: str) -> None:
    if ns in this().subspaces:
        del this().subspaces[ns]
    elif ns in namespaces:
        del namespaces[ns]
    else:
        invalidNamespaceError(ns)

def define(what: Function | Subroutine | Class) -> None:
    global defining, deflen
    defining = what
    deflen = 1

def end_define() -> None:
    global defining, deflen
    defining = None
    deflen = 0

def call(what: Function | Subroutine | Lambda | object, args: list = []) -> Any:
    if hasattr(what, 'argdefs') and hasattr(what, 'has_catchall'):
        if (len(args)==len(what.argdefs)) or (len(args)>=len(what.argdefs) and what.has_catchall()):
            backup()
            parent = this()
            stack.append(what)
            r = what(args, parent)
            for _ in stack_needs_pop.copy():
                stack.pop()
                stack_needs_pop.pop()
            if not error: stack.pop()
            return r
        else:
            wrongCallableArguments(len(args), len(what.argdefs), what.has_catchall())
    else:
        backup()
        parent = this()
        stack.append(what)
        r = what(args, parent)
        for _ in stack_needs_pop.copy():
            stack.pop()
            stack_needs_pop.pop()
        if not error: stack.pop()
        return r

def run_if(condition: bool, then: Function | Subroutine | Lambda | object, args: list = []) -> Any:
    if len(if_stack) > 0: if_stack.clear()  # Clear the if stack if it isn't already empty
    if condition:
        r = call(then, args)
        if_stack.clear()
        return r
    else:
        if_stack.append(condition)

def run_elif(condition: bool, then: Function | Subroutine | Lambda | object, args: list = []) -> Any:
    if len(if_stack) > 0:
        if not any(if_stack) and condition:
            r = call(then, args)
            if_stack.clear()
            return r
        else:
            if_stack.append(condition)
    else:
        unmatchedOp('ELIF', 'IF')

def run_else(then: Function | Subroutine | Lambda | object, args: list = []) -> Any:
    if len(if_stack) > 0:
        r = call(then, args)
        if_stack.clear()
        return r
    else:
        unmatchedOp('ELSE', 'IF')

def init_try() -> None:
    global trying, aced_try
    trying = True
    aced_try = False

def run_when(when: str, then: Function | Subroutine | Lambda | object, args: list = []) -> Any:
    if trying:
        if catch(when):
            r = call(then, args)
            return r
    else:
        unmatchedOp('WHEN', 'TRY')

def run_ace(then: Function | Subroutine | Lambda | object, args: list = []) -> Any:
    if trying:
        if aced_try:
            r = call(then, args)
            return r
    else:
        unmatchedOp('ACE', 'TRY')

def run_then(then: Function | Subroutine | Lambda | object, args: list = []) -> Any:
    if trying:
        r = call(then, args)
        return r
    else:
        unmatchedOp('THEN', 'TRY')

def uninit_try() -> None:
    global trying, aced_try
    if trying:
        trying = False
        aced_try = False
    else:  # This is deliberate, as it ensures the situation is restored to default even when there was nothing to stop
        trying = False
        aced_try = False
        unmatchedOp('STOP', 'TRY')

# This was the legacy version of 'this'. It has been kept here for historical purposes, as a mean to thank it for its
# long service in older development versions of mlmcr 3 (and because it might still come in useful at some point).
# def this(name: Namespace | None = None, subs: list[str] | None = None, get_parent: bool = False) -> Namespace:
#     if get_parent:
#         if subs is None: subs = current_subspace[:-1]
#         if stack[:-1] and (name is None):
#             for entry in reversed(stack[:-1]):
#                 if hasattr(entry, 'scope'):
#                     return entry.scope
#         if name is None: name = namespaces[current_namespace]
#         if not subs:
#             return name
#         return this(name.subspaces[subs[0]], subs[1:])
#     else:
#         if subs is None: subs = current_subspace
#         if stack and (name is None):
#             for entry in reversed(stack):
#                 if hasattr(entry, 'scope'):
#                     return entry.scope
#         if name is None: name = namespaces[current_namespace]
#         if not subs:
#             return name
#         return this(name.subspaces[subs[0]], subs[1:])

def this(name: Namespace | None = None, get_parent: bool = False) -> Namespace:
    # name is for backwards compatibility: older iterations of 'this' used it as a fail-safe
    # and older libraries could still be using it; it doesn't hurt anyways

    # Initialize the search
    if name: current_scope = name
    else: current_scope = namespaces[current_namespace]
    current_parent = current_scope
    stack_not_exhausted = len(stack)>0
    # Start the search loop
    while True:
        scope_subspace = current_scope.current_subspace
        if stack_not_exhausted:  # If the stack has not been exhausted
            for entry in reversed(stack):  # For every item in the stack
                if hasattr(entry, 'scope'):  # Only consider it if it creates a new scope
                    current_parent = entry.parent
                    current_scope = entry.scope
                    stack_not_exhausted = False
                    break
            stack_not_exhausted = False
        else:  # If the stack is no longer relevant
            if scope_subspace is None:  # If this is the last subspace in the hierarchy
                if get_parent:
                    return current_parent
                return current_scope
            else:  # If there are other nested subspaces to consider
                current_parent = current_scope
                if scope_subspace in current_scope.subspaces:
                    current_scope = current_scope.subspaces[scope_subspace]
                else:
                    raise ThisLookupError(scope_subspace)

def append_subspace(sub: str) -> None:
    this().current_subspace = sub

def pop_subspace() -> None:
    this(get_parent=True).current_subspace = None

def get_subspace(get_parent: bool = False) -> str:
    return this(get_parent=get_parent).current_subspace

def convert(args: list[str]) -> list[Any]:
    a = []
    for arg in args:
        if arg.startswith('##'):
            a.append(to_float(arg))
        elif arg.startswith('#'):
            a.append(to_int(arg))
        elif arg.startswith('&'):
            a.append(to_str(arg))
        elif arg.startswith('!'):
            a.append(to_bool(arg))
        elif arg.startswith(':'):  # Lambda definition
            a.append(arg.removeprefix(':'))
        elif arg.startswith(('<->', '<-', '->')):  # Variable declaration
            a.append(arg.removeprefix('<->').removeprefix('<-').removeprefix('->'))
        elif arg.startswith('>>'):  # Special name idiom
            a.append(arg.removeprefix('>>'))
        elif arg.startswith('>'):  # Parameter declaration
            a.append(arg.removeprefix('>'))
        elif arg == '*':  # Any error idiom
            a.append('*')
        elif arg.startswith('*'):  # Lambda applicator
            ns, var = get_namespace(arg.removeprefix('*'))
            if ns == 'THIS':
                l = this().get_var(var)
            elif ns in this().subspaces:
                # Search the root function scope if we are looking for a default and the scope's prefix is different from _DEFAULT's
                if ns == '_DEFAULT' and (context_type=='function' or context_type=='lambda') and var.startswith(this()._pref):
                    l = this().get_var(var)
                else:
                    append_subspace(ns)
                    l = this().get_var(var)
                    pop_subspace()
            elif ns in namespaces:
                l = namespaces[ns].get_var(var)
            else:
                invalidNamespaceError(ns)
            if isinstance(l, Lambda):
                a.append(LambdaApplicator(l))
            else:
                cantDo("apply a lambda from", l)
        elif arg.startswith('?'):  # Catch-all parameter
            a.append(CatchAll(arg.removeprefix('?')))
        elif arg.startswith('^'):  # Lookback argument
            a.append(LookBack(arg.removeprefix('^')))
        elif arg.startswith('<>'):  # Register
            a.append(get_register(arg.removeprefix('<>')))
        else:
            ns, var = get_namespace(arg)
            if ns == 'THIS':
                a.append(this().get_var(var))
            elif ns in this().subspaces:
                # Search the root function scope if we are looking for a default and the scope's prefix is different from _DEFAULT's
                if ns == '_DEFAULT' and (context_type=='function' or context_type=='lambda') and var.startswith(this()._pref):
                    v = this().get_var(var)
                else:
                    append_subspace(ns)
                    v = this().get_var(var)
                    pop_subspace()
                a.append(v)
            elif ns in namespaces:
                a.append(namespaces[ns].get_var(var))
            else:
                invalidNamespaceError(ns)
    # Lambda resolution
    for i, x in enumerate(a.copy()):
        if isinstance(x, LambdaApplicator):
            if not x.ref.has_catchall():
                upto = i + len(x.ref.argdefs)
                a[i:upto+1] = (call(x.ref, a[i+1:upto+1]),)
            else:
                lambdaError("with a catch-all parameter")
    return a

def to_float(what: str) -> float | None:
    try:
        return float(what.removeprefix('##'))
    except ValueError:
        notaNumber(what.removeprefix('##'))

def to_int(what: str) -> int | None:
    try:
        return int(what.removeprefix('#'))
    except ValueError:
        notaNumber(what.removeprefix('#'))

def to_str(what: str) -> str:
    return what.removeprefix('&')

def to_bool(what: str) -> bool:
    if what == '!0': return False
    else: return True

def between(func: object, args: list[Any], min: int, max: int) -> None:  # here object = function
    if min <= len(args) <= max:
        func(args)
    else:
        opArgNumGenericError(current_namespace, current_op, min, max, len(args))

def atmost(func: object, args: list[Any], max: int) -> None:  # here object = function
    if len(args) <= max:
        func(args)
    else:
        opArgTooManyError(current_namespace, current_op, max, len(args))

def atleast(func: object, args: list[Any], min: int) -> None:  # here object = function
    if min <= len(args):
        func(args)
    else:
        opArgTooLittleError(current_namespace, current_op, min, len(args))

def when(func: object, args: list[Any], count: int) -> None:  # here object = function
    if len(args) == count:
        func(args)
    else:
        opArgNumWrongError(current_namespace, current_op, count, len(args))

def bind(func: object, op: str) -> None:  # here object = function
    this().new_op(op, func)

def check(arg: Any, t: Any) -> bool:  # Works exactly like isinstance, but is shorter to write
    return isinstance(arg, t)

def has(arg: Any, a: str) -> bool:  # Works exactly like hasattr, but is shorter to write
    return hasattr(arg, a)

def gettype(of: Any) -> str:
    if isinstance(of, bool):
        return 'BOOL'
    elif isinstance(of, int):
        return 'INT'
    elif isinstance(of, float):
        return 'FLPT'
    elif isinstance(of, str):
        return 'STR'
    elif of is None:
        return 'NULL'
    elif isinstance(of, LookBack):
        return 'LOOKBACK'
    elif isinstance(of, list):
        return 'SEQ'
    elif isinstance(of, PermaSequence):
        return 'PSEQ'
    elif isinstance(of, tuple):
        return 'PACK'
    elif isinstance(of, dict):
        return 'MAP'
    elif isinstance(of, range):
        return 'LOOP'
    elif isinstance(of, Subroutine):
        return 'SUBR'
    elif isinstance(of, Function):
        return 'FUNC'
    elif isinstance(of, Lambda):
        return 'PROC'
    elif isinstance(of, Class):
        return of._name
    else:
        return type(of).__name__

def tokenize(source: str) -> tuple[str, list[str]]:
    source = source.split(';;', maxsplit=1)[0]  # Remove comments
    tokens = source.split(' ', maxsplit=1)  # Separate opcode from arguments
    opcode = tokens[0].upper()  # Make the opcode uppercase
    if len(tokens) > 1:
        # Replace escaped ',' and ';;' sequences with placeholders in arguments
        tokens[1] = tokens[1].replace('/,/', '/|-|/').replace('/;;/', '/|;|/')
        args = tokens[1].split(',')  # Split into individual arguments
        for i, arg in enumerate(args):
            # Detect colons and amperstands and treat the values following them as instructions and string literals respectively
            found_colon = False
            colon_pos = 0
            found_amperstand = False
            amperstand_pos = len(args)
            for p, c in enumerate(arg):
                if c == ':' and not found_colon:
                    found_colon = True
                    colon_pos = p
                elif c == '&' and not found_amperstand:
                    found_amperstand = True
                    amperstand_pos = p
            if found_colon and colon_pos < amperstand_pos:
                # Join with all the successive arguments (with the original sequences replaced back), deleting them
                args[i:] = [','.join([a.replace('/|-|/', '/,/').replace('/|;|/', '/;;/') for a in args[i:]]).lstrip()]
            elif found_amperstand:
                args[i] = arg.replace('/|-|/', ',').replace('/|;|/', ';;').lstrip()  # Replace the placeholder sequences in strings
            else:
                args[i] = arg.replace(' ', '').upper()  # Remove spaces and make other arguments uppercase
            if args[i].isspace(): args[i] = ''  # Convert whitespace arguments to empty strings for later removal
        args = [arg for arg in args if arg != '']  # Make args a new list with the empty arguments removed
    else:
        args = []
    return opcode, args

def get_namespace(element: str) -> tuple[str, str]:
    parts = element.split('.', maxsplit=1)
    if len(parts) == 2:
        namespace, el = parts
        return namespace, el
    else:
        return '_DEFAULT', parts[0]

def run(source: list) -> None | Any:
    global error, n, s, in_pyblock, pyblock, current_namespace
    s = source
    for _n, line in enumerate(source):
        if not in_pyblock:
            if defining is None:
                opcode, args = tokenize(line.lstrip())
                if opcode != '':
                    # Special pyblock handling
                    if opcode == 'PYBLOCK':
                        in_pyblock = True
                        pyblock = []
                    else:
                        namespace, op = get_namespace(opcode)
                        args = convert(args)
                        try:
                            if namespace == 'THIS':
                                this().call_op(op, args)
                            elif namespace in this().subspaces:
                                append_subspace(namespace)
                                current_subspace_needs_cleanup.append(True)  # Functions will pop current_subspace on return if True
                                this().call_op(op, args)
                                pop_subspace()
                                current_subspace_needs_cleanup.pop()
                            elif namespace in namespaces:
                                namespaces[namespace].call_op(op, args)
                            else:
                                invalidNamespaceError(namespace)
                            # If the current error wasn't explicitly handled, report it
                            if current_error != ('Unknown error', 'if you see this, please file a bug report'):
                                try:
                                    if context_type=='function' or context_type=='lambda': n = _n + stack[-1].defline
                                    else: n = _n
                                except IndexError:
                                    n = "<can't load>"
                                report_error(*current_error)
                        except ThisLookupError as e:
                            thisLookupError(e.ref)
                        except Break:
                            cantUseAdvancedControlFlow()
                        except Continue:
                            cantUseAdvancedControlFlow()
            else:
                defining.add_instruction(line.lstrip())
        else:
            # "light-weight" line manipulation -> opcode
            if line.lstrip().split(' ', maxsplit=1)[0].upper() == 'PYEND':
                in_pyblock = False
                exec('\n'.join(pyblock))  # Execute the pyblock as python code
                # Check for any mlmcr errors thrown from the pyblock
                if current_error != ('Unknown error', 'if you see this, please file a bug report'):
                    report_error(*current_error)
                in_pyblock = False  # Reset the global flag again so that code in the pyblock can't mess it up
                pyblock = []  # Clean up pyblock just in case
            else:
                pyblock.append(line)

def run_file(path: str) -> None:
    if os.path.isfile(path):
        if not path.endswith('.mlmcr'):
            if path.endswith('.mlmch'):
                print("Interpreter warning: it seems like you are trying to run an mlmcr header file (.mlmch) as an mlmcr script file (.mlmcr)")
                print("Are you sure this is what you intended to do?")
            else:
                print("Interpreter warning: you are trying to run a file without the .mlmcr extension")
                print(f"Are you sure that '{path}' is a valid mlmcr script file?")
        with open(path) as f:
            l = f.readlines()
            for i, x in enumerate(l):
                # Hack for removing unescaped \n sequences from f
                l[i] = x.replace('\\n', '/|n|/').replace('\n', '').replace('/|n|/', '\\n')
            try:
                run(l)
            except EOFError:
                print("\nThis is the end of your current mlmcr session. See you next time!")
            except KeyboardInterrupt:
                print("\nThis is the end of your current mlmcr session. See you next time!")
            except MlmcrError:
                pass  # Catch MlmcrError and move on
            except RecursionError:
                recursionError()
            except MemoryError:
                memoryError()
            except Return as e:
                stackError(e.depth)
    else:
        print(f"Interpreter error: '{path}' does not exist or is not a file!")
        sys.exit(66)  # EX_NOINPUT

def splash() -> None:
    if sys.platform.startswith('win32'):  # Change the window title on Windows
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("mlmcr (revision 3)")
    print("mlmcr Revision 3")
    print("Copyright (C) 2023  BarbeMCR")
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} on {sys.platform}")
    print("BarbeMCR welcomes you to programming hell!")

def run_repl() -> None:
    global error
    while True:
        # Choose the right prompt to display
        if in_pyblock: prompt = '$ '
        elif defining: prompt = '> '  # should be 'defining is not None' but we don't have other falsy values here
        else: prompt = '@ '
        # Take input
        try:
            line = input('  ' + '    '*(deflen) + prompt)
        except EOFError:
            continue
        except KeyboardInterrupt:
            print("  <- this instruction wasn't executed")
            print("This is the end of your current mlmcr session. See you next time!")
            sys.exit(0)  # EX_OK
        try:
            run([line])  # line is wrapped in a list so that run can be reused in repl mode
        except MlmcrError:
            pass  # We don't need this exception block to do anything:
                  # all the error-related stuff gets already done long before MlmcrError gets raised
        except RecursionError:
            recursionError()
        except MemoryError:
            memoryError()
        error = False

def import_mlmch(file: str) -> None:
    global current_namespace
    path = file + '.mlmch'
    if os.path.isfile(path):
        _from = current_namespace
        if current_namespace != '_DEFAULT': append_subspace(os.path.basename(file.upper()))
        else: current_namespace = os.path.basename(file.upper())
        with open(path) as h:
            l = h.readlines()
            for i, x in enumerate(l):
                # Hack for removing unescaped \n sequences from h
                l[i] = x.replace('\\n', '/|n|/').replace('\n', '').replace('/|n|/', '\\n')
            if _from != '_DEFAULT': new_namespace(this(get_parent=True).current_subspace.upper(), _from)
            else: new_namespace(current_namespace.upper(), _from)
            try:
                run(l)
            except MlmcrError:
                pass
            except RecursionError:
                recursionError()
            except MemoryError:
                memoryError()
        if _from != '_DEFAULT': pop_subspace()
        current_namespace = _from
    else:
        invalidMlmch(path)

def report_error(err: str, info: str) -> None:
    if isinstance(n, int):
        try:
            if in_pyblock:
                print(f"{err} at <pyblock ending on line {n+1}>, filespace {current_namespace}...{this()._name if this()._name!=current_namespace else '<root>'}: {info}")
            else:
                print(f"{err} at line {n+1}, filespace {current_namespace}...{this()._name if this()._name!=current_namespace else '<root>'}: {info}")
                print(f"{s[n]}  <- detected here (might not be accurate)")
        except ThisLookupError:
            if in_pyblock:
                print(f"{err} at <pyblock ending on line {n+1}>, filespace {current_namespace}...<unknown>: {info}")
            else:
                print(f"{err} at line {n+1}, filespace {current_namespace}...<unknown>: {info}")
                print(f"{s[n]}  <- detected here (might not be accurate)")
    else:
        print(f"{err}: {info}")
        print("Warning: we couldn't determine the affected line due to a stack underflow error during handling!")
    global error, current_error
    error = True
    current_error = ('Unknown error', 'if you see this, please file a bug report')  # Clean up just in case
    restore()
    raise MlmcrError

def catch(err: str) -> bool:
    global caught_error, aced_try
    # If any error occured
    if err == '*' and caught_error != ('', ''):
        caught_error = ('', '')
        aced_try = False
        return True
    else:
        # If the current error matches what we want to catch
        if caught_error[0] == err:
            caught_error = ('', '')
            aced_try = False
            return True
        # Otherwise there must no error (or another one we haven't handled yet, but we eventually handle if it is relevant)
        else:
            aced_try = True  # We can assume there was no relevant error here since this flag will be reset if the error is handled
            return False

def throw(err: str, info: str = "no further information") -> None:
    global current_error, caught_error
    if trying:
        if caught_error == ('', ''):
            caught_error = (err, info)
    else:
        if current_error == ('Unknown error', 'if you see this, please file a bug report'):
            current_error = (err, info)

# Builtin error functions
# (those are specialized and needed for all sorts of errors so it makes sense to have them builtin instead of core)
def genericNameError(var, ns):
    if ns != '_DEFAULT': throw("Name error", f"variable {var} does not exist in namespace {ns}")
    else: throw("Name error", f"variable {var} does not exist")

def nameFormatError(var, pref):
    throw("Format error", f"variable {var} can't be created as its name isn't of the form\n{pref} + hexadecimal string (e.g. {pref}B4C0, {pref}77c5), or a declaration was put where an argument was supposed to go")

def notaNumber(val):
    throw("Number error", f"{val} is neither an INT nor a FLPT, and can't be converted to either")

def killListFullError(ns, size, var):
    if ns != '_DEFAULT': throw("Kill list full error", f"{ns}'s kill list, of size {size}, is full and can't accept variable {var}")
    else: throw("Kill list full error", f"kill list, of size {size}, is full and can't accept variable {var}")

def killTicketError(ticket, ns):
    if ns != '_DEFAULT': throw("Ticket error", f"kill ticket {ticket} does not exist in {ns}'s kill list")
    else: throw("Ticket error", f"kill ticket {ticket} does not exist")

def invalidOpError(ns, op):
    if ns != '_DEFAULT': throw("Opcode error", f"opcode {ns}.{op} does not exist")
    else: throw("Opcode error", f"opcode {op} does not exist")

def opFormatError(ns, op):
    if ns != '_DEFAULT': throw("Opcode error", f"something weird with opcode {ns}.{op} happened. Either:\n - you put a variable name where a declaration was supposed to go (e.g. $0 instead of ->$0)\n - you passed through some weird content which was not supposed to be here\n - or {ns}.{op} has an invalid format (check opcode definition and relevant bind call)")
    else: throw("Opcode error", f"something weird with opcode {op} happened. Either:\n - you put a variable name where a declaration was supposed to go (e.g. $0 instead of ->$0)\n - you passed through some weird content which was not supposed to be here\n - or {op} has an invalid format (if this is the case, file a bug report after excluding EVERYTHING else)")

def opArgNumGenericError(ns, op, req_min, req_max, count):
    if ns != '_DEFAULT': throw("Argument error", f"opcode {ns}.{op} requires between {req_min} and {req_max} argument(s), but {count} were passed")
    else: throw("Argument error", f"opcode {op} requires between {req_min} and {req_max} argument(s), but {count} were passed")

def opArgTooManyError(ns, op, req, count):
    if ns != '_DEFAULT': throw("Argument error", f"opcode {ns}.{op} requires at most {req} argument(s), but {count} were passed")
    else: throw("Argument error", f"opcode {op} requires at most {req} argument(s), but {count} were passed")

def opArgTooLittleError(ns, op, req, count):
    if ns != '_DEFAULT': throw("Argument error", f"opcode {ns}.{op} requires at least {req} argument(s), but {count} were passed")
    else: throw("Argument error", f"opcode {op} requires at least {req} argument(s), but {count} were passed")

def opArgNumWrongError(ns, op, req, count):
    if ns != '_DEFAULT': throw("Argument error", f"opcode {ns}.{op} requires {req} argument(s), but {count} were passed")
    else: throw("Argument error", f"opcode {op} requires {req} argument(s), but {count} were passed")

def opArgTypeError(ns, op, argn):
    if ns != '_DEFAULT': throw("Type error", f"argument #{argn+1} was of the wrong type for opcode {ns}.{op}")
    else: throw("Type error", f"argument #{argn+1} was of the wrong type for opcode {op}")

def typeErr(argn):  # opArgTypeError convenience function
    opArgTypeError(current_namespace, current_op, argn)

def cantUseOpHere():
    if current_namespace != '_DEFAULT': throw("Context error", f"opcode {current_namespace}.{current_op} can't be used here")
    else: throw("Context error", f"opcode {current_op} can't be used here")

def cantDo(what, on, t=None):
    throw("Operation type error", f"you can't {what} {on} of type {gettype(on) if t is None else t}")

def invalidNamespaceError(ns):
    if ns != '_DEFAULT': throw("Namespace error", f"namespace {ns} does not exist")
    else: throw("Namespace error", "the default namespace is missing!")

def namespaceFormatError(ns):
    throw("Namespace error", f"namespace {ns} has an invalid format (is it a Namespace or compatible class?)")

def arrayIndexError():
    throw("Index error", "array index out of bounds")

def mapKeyError(k):
    throw("Key error", f"inexistent map key {k}")

def invalidCatchalls():
    throw("Definition error", "there is more than one catch-all parameter (or it is misplaced)")

def cantDefineHere(what, context):
    throw("Definition error", f"can't define {what} in {context}")

def wrongCallableArguments(passed, req, catchall=False):
    throw("Argument count error", f"this callable requires {'at least ' if catchall else ''}{req} argument(s), but {passed} were passed")

def unmatchedOp(op, matcher):
    throw("Mismatch error", f"opcode {op.upper()} requires a {matcher.upper()} opcode beforehand")

def lambdaError(message):
    throw("Lambda error", f"you can't apply a lambda {message}")

def invalidRegisterName(name):
    throw("Invalid register name error", f"register name {name} is not valid, since it does not respect the [8.]3 rule for register names")

def invalidRegister(name):
    throw("Invalid register error", f"register {name} does not exist")

def cantUseAdvancedControlFlow():
    throw("Control flow error", "can't use advanced control flow here")

def stackError(d):
    throw("Stack error", f"the stack isn't deep enough to return another {d+1} level(s)")

def invalidMlmch(path):
    throw("Inexistent header file", f"there is no mlmcr header file at location {path.lower()}")

def thisLookupError(ref):
    throw("Fatal lookup error", f"{ref} is not a valid name in the current namespace hierarchy")

def recursionError():
    throw("Recursion error", "apparently something blew the stack. It looks like someone should think about handling recursion better...")

def memoryError():
    throw("Memory error", "apparently you ran out of available memory. How is this possible? Only BarbeMCR knows!\nSeriously though, you have some explaining to do...")

# Startup
if __name__ == '__main__':
    for core in cores:
        if os.path.isfile(os.path.join('cores', f'{core}.mlmch')):
            import_mlmch(os.path.join('cores', core))
        else:
            print(f"Interpreter warning: missing core {core}.mlmch!")
    backup('namespaces')
    if len(sys.argv) > 2:
        print("Interpreter error: too many command-line arguments!")
        print("Usage: mlmcr [script]")
        sys.exit(64)  # EX_USAGE
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        splash()
        run_repl()
