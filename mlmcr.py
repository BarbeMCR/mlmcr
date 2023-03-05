# mlmcr, the unnecessary Assembly-like programming language
# Copyright (C) 2023  BarbeMCR

import sys
import string
import time
import random
import math
import ctypes

if sys.platform.startswith('win32') and __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW("mlmcr (revision 2)")

class PermaSequence:
    """Read-only list interface."""
    def __init__(self):
        self.sequence = []
    def __getitem__(self, index):
        return self.sequence[index]
    def __contains__(self, value):
        return value in self.sequence
    def __len__(self):
        return len(self.sequence)
    def __iter__(self):
        return iter(self.sequence)
    def __str__(self):
        return str(self.sequence)
    def append(self, item):
        self.sequence.append(item)
    def extend(self, item):
        self.sequence.extend(item)
    def index(self, value):
        return self.sequence.index(value)
    def clear(self):
        self.sequence.clear()
    def copy(self):
        return self.sequence.copy()
    def insert(self, index, object):
        print("PSEQ values are read-only!")
    def pop(self, index=-1):
        print("PSEQ values are read-only!")
    def remove(self, value):
        print("PSEQ values are read-only!")
        
class Subroutine:
    """The subroutine interface."""
    def __init__(self):
        self.instructions = []
    def add_instruction(self, namespace, instruction):
        self.instructions.append(instruction)
        _parse_subr_func_rts(namespace, instruction)
    def run(self, namespace):
        for instruction in self.instructions:
            namespace['executing_subr'] = True
            parse(namespace, instruction)
            
class Function:
    """The function interface."""
    def __init__(self, argdefs):
        self.instructions = []
        self.argdefs = argdefs
    def report_argdefs_validity(self):
        argdefs_valid = True
        for argdef in self.argdefs:
            if not argdef.startswith('@') or not all(char in set(string.hexdigits) for char in argdef.removeprefix('@')):
                print("Arguments must start with '@' and contain only hexadecimal characters.")
                argdefs_valid = False
        return argdefs_valid
    def add_instruction(self, namespace, instruction):
        self.instructions.append(instruction)
        _parse_end(namespace, instruction)
    def run(self, namespace, arguments):
        namespace_copy = namespace
        namespace = {
            'vars': {self.argdefs[i]: arguments[i] for i in range(len(self.argdefs))},
            '_vars': namespace['vars'],
            'killed_vars': [],
            'kill_length': 0,
            'stack': namespace['stack'],
            'stack_pointer': namespace['stack_pointer'],
            'if_stack': namespace['if_stack'],
            'executing_subr': namespace['executing_subr'],
            'executing_func': True
        }
        returns = []
        for instruction in self.instructions:
            namespace['executing_func'] = True
            returns.append(_parse_give_take_sync(namespace, namespace_copy, instruction))
            parse(namespace, instruction)
            for var in namespace['vars']:
                if not var.startswith('@') or not all(char in set(string.hexdigits) for char in var.removeprefix('@')):
                    del namespace['vars']
                    print("Local variables must start with '@' and contain only hexadecimal characters.")
        for val in returns:
            if val is None:
                returns.remove(val)
        if len(returns) > 0:
            return returns[-1]

def get_input(prompt):
    """Grab input from the user.
    
    Arguments:
    prompt -- the prompt to display
    """
    user_input = input(prompt).lstrip()
    return user_input
    
def get_bool(value):
    """Get a boolean from a !-prefixed string.
    
    Arguments:
    value -- the string to convert
    """
    return bool(int(str(value).removeprefix('!')))
    
def _parse_subr_func_rts(namespace, instruction):
    """Parse an mlmcr instruction (only checking for a SUBR, a FUNC or a RTS).
    
    Arguments:
    namespace -- the namespace
    instruction -- the instruction to parse
    """
    vars = namespace['vars']
    opcode = instruction.upper()
    opcode = opcode.split(' ', 1)[0]
    args = instruction.split(',')
    args[0] = args[0].split(' ', 1)
    args = args[0] + args[1:]
    args.pop(0)
    for index, arg in enumerate(args):
        args[index] = arg.lstrip()
        if args[index].startswith('$') or args[index].startswith('@'):
            args[index] = args[index].upper()
    if opcode == 'SUBR':
        if len(args) == 1:
            vars[args[0]] = Subroutine()
            namespace['stack'].append(vars[args[0]])
            namespace['stack_pointer'] += 1
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'FUNC':
        if len(args) >= 1:
            vars[args[0]] = Function(args[1:])
            argdefs_valid = vars[args[0]].report_argdefs_validity()
            if not argdefs_valid:
                del vars[args[0]]
            else:
                namespace['stack'].append(vars[args[0]])
                namespace['stack_pointer'] += 1
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'RTS':
        namespace['stack'][namespace['stack_pointer']].instructions.pop()
        if namespace['stack_pointer'] > 0:
            namespace['stack'].pop()
            namespace['stack_pointer'] -= 1
        else:
            namespace['stack'][0] = None
            namespace['stack_pointer'] = 0
            
def _parse_end(namespace, instruction):
    """Parse an mlmcr instruction (only checking for a END).
    
    Arguments:
    namespace -- the namespace
    instruction -- the instruction to parse
    """
    opcode = instruction.upper()
    opcode = opcode.split(' ', 1)[0]
    if opcode == 'END':
        namespace['stack'][namespace['stack_pointer']].instructions.pop()
        if namespace['stack_pointer'] > 0:
            namespace['stack'].pop()
            namespace['stack_pointer'] -= 1
        else:
            namespace['stack'][0] = None
            namespace['stack_pointer'] = 0
            
def _parse_give_take_sync(namespace, namespace_copy, instruction):
    """Parse an mlmcr instruction (only checking for a GIVE, a TAKE or a SYNC).
    
    Arguments:
    namespace -- the namespace
    namespace_copy -- the reference to the original namespace
    instruction -- the instruction to parse
    """
    vars = namespace['vars']
    opcode = instruction.upper()
    opcode = opcode.split(' ', 1)[0]
    args = instruction.split(',')
    args[0] = args[0].split(' ', 1)
    args = args[0] + args[1:]
    args.pop(0)
    for index, arg in enumerate(args):
        args[index] = arg.lstrip()
        if args[index].startswith('$') or args[index].startswith('@'):
            args[index] = args[index].upper()
    if opcode == 'GIVE':
        if len(args) == 1:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            return args[0]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'TAKE':
        if len(args) == 2:
            if isinstance(namespace['_vars'][args[0]], Subroutine):  # Change $ for @ in subroutines
                for inst_index, inst in enumerate(namespace['_vars'][args[0]].instructions):
                    inst_list = list(inst)
                    found_amperstand = False
                    for i, char in enumerate(inst_list):
                        if char == '&':
                            found_amperstand = True
                        elif char == ',' and found_amperstand:
                            found_amperstand = False
                        elif char == '$' and not found_amperstand:
                            inst_list[i] = '@'
                    namespace['_vars'][args[0]].instructions[inst_index] = ''.join(inst_list)
            vars[args[1]] = namespace['_vars'][args[0]]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'SYNC':
        if len(args) == 2:
            namespace_copy['vars'][args[1]] = vars[args[0]]
        else:
            print(f"Wrong arguments in {instruction}")
    
def parse(namespace, instruction):
    """Parse an mlmcr instruction.
    
    Arguments:
    namespace -- a dict representing the namespace
                 It must contain the following items:
                 - 'vars': a dict where every key represents a variable name and every item its value
                 - 'killed_vars': a list containing all the values in the kill list
                 - 'kill_length': an int representing the maximum length of the kill list
                 - 'stack': a list representing the declaration stack
                 - 'stack_pointer': an int representing the stack index in which instructions are being processed
                 - 'executing_subr': a bool representing whether a subroutine is being executed
                 - 'executing_func': a bool representing whether a function is being executed
    instruction -- the instruction to parse
    """
    vars = namespace['vars']
    killed_vars = namespace['killed_vars']
    kill_length = namespace['kill_length']
    opcode = instruction.upper()
    opcode = opcode.split(' ', 1)[0]
    args = instruction.split(',')
    args[0] = args[0].split(' ', 1)
    args = args[0] + args[1:]
    args.pop(0)
    for index, arg in enumerate(args):
        args[index] = arg.lstrip()
        if args[index].startswith('$') or args[index].startswith('@'):
            args[index] = args[index].upper()
    if opcode.startswith(';'):
        pass  # Starting a line with ; allows for comments as elif is used below
    elif opcode == 'PUT':
        if len(args) == 2:
            if args[0].startswith('$'):
                vars[args[1]] = vars[args[0]]
            elif args[0].startswith('##'):
                vars[args[1]] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                vars[args[1]] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                vars[args[1]] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                vars[args[1]] = get_bool(args[0])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'DEL':
        if len(args) == 1:
            del vars[args[0]]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'NEW':
        if len(args) >= 2:
            obj = type(vars[args[0]])
            constructor_args = args[2:]
            for i, arg in enumerate(constructor_args):
                if arg.startswith('##'):
                    constructor_args[i] = float(arg.removeprefix('##'))
                elif arg.startswith('#'):
                    constructor_args[i] = int(arg.removeprefix('#'))
                elif arg.startswith('&'):
                    constructor_args[i] = arg.removeprefix('&')
                elif arg.startswith('!'):
                    constructor_args[i] = get_bool(arg)
                else:
                    constructor_args[i] = vars[arg]
            vars[args[1]] = obj(*constructor_args)
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'SWAP':
        if len(args) == 2:
            vars[args[0]], vars[args[1]] = vars[args[1]], vars[args[0]]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'KILL':
        if not namespace['executing_func']:
            if len(args) == 1:
                killed_vars.append(vars[args[0]])
                if len(killed_vars) > kill_length:
                    killed_vars.pop(0)
                del vars[args[0]]
            elif len(args) == 2:
                killed_vars.append(vars[args[0]])
                if len(killed_vars) > kill_length:
                    killed_vars.pop(0)
                del vars[args[0]]
                vars[args[1]] = len(killed_vars) - 1
            else:
                print(f"Wrong arguments in {instruction}")
    elif opcode == 'WAKE':
        if not namespace['executing_func']:
            if len(args) == 2:
                if args[0].startswith('#'):
                    args[0] = int(args[0].removeprefix('##').removeprefix('#'))
                else:
                    args[0] = vars[args[0]]
                vars[args[1]] = killed_vars[args[0]]
                killed_vars.pop(args[0])
            else:
                print(f"Wrong arguments in {instruction}")
    elif opcode == 'KSET':
        if not namespace['executing_func']:
            if len(args) == 1:
                if args[0].startswith('#'):
                    args[0] = int(args[0].removeprefix('##').removeprefix('#'))
                else:
                    args[0] = vars[args[0]]
                if 0 <= args[0] <= 65536:
                    namespace['kill_length'] = args[0]
                elif args[0] < 0:
                    namespace['kill_length'] = 0
                else:
                    namespace['kill_length'] = 65536
            else:
                print(f"Wrong arguments in {instruction}")
    elif opcode == 'KGET':
        if not namespace['executing_func']:
            if len(args) == 1:
                vars[args[0]] = len(killed_vars) - 1
            else:
                print(f"Wrong arguments in {instruction}")
    elif opcode == 'HALT':
        if len(args) == 1:
            if args[0].startswith('#'):
                args[0] = float(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            time.sleep(args[0])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'SUBR':
        if not (namespace['executing_subr'] or namespace['executing_func']):
            if len(args) == 1:
                vars[args[0]] = Subroutine()
                namespace['stack'][0] = vars[args[0]]
            else:
                print(f"Wrong arguments in {instruction}")
    elif opcode == 'JUMP':
        if len(args) == 1:
            if isinstance(vars[args[0]], Subroutine):
                vars[args[0]].run(namespace)
                namespace['executing_subr'] = False
            else:
                print(f"{args[0]} is not a subroutine.")
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'FUNC':
        if not (namespace['executing_func'] or namespace['executing_subr']):
            if len(args) >= 1:
                vars[args[0]] = Function(args[1:])
                argdefs_valid = vars[args[0]].report_argdefs_validity()
                if not argdefs_valid:
                    del vars[args[0]]
                else:
                    namespace['stack'][0] = vars[args[0]]
            else:
                print(f"Wrong arguments in {instruction}")
    elif opcode == 'CALL':
        if len(args) >= 1:
            if isinstance(vars[args[0]], Function):
                if len(args[1:-1]) == len(vars[args[0]].argdefs):
                    for i, arg in enumerate(args[1:-1]):
                        i += 1  # This accounts for the fact that we are excluding args[0]
                        if arg.startswith('##'):
                            args[i] = float(arg.removeprefix('##'))
                        elif arg.startswith('#'):
                            args[i] = int(arg.removeprefix('#'))
                        elif arg.startswith('&'):
                            args[i] = arg.removeprefix('&')
                        elif arg.startswith('!'):
                            args[i] = get_bool(arg)
                        else:
                            args[i] = vars[args[i]]
                    vars[args[-1]] = vars[args[0]].run(namespace, args[1:-1])
                    namespace['executing_func'] = False
                else:  # This simulates an exception
                    print(f"Function arguments do not match definitions in {args[0]}")
                    namespace['stack'] = [None]
                    namespace['stack_pointer'] = 0
                    namespace['executing_subr'] = False
                    namespace['executing_func'] = False
            else:
                print(f"{args[0]} is not a function")
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'SEQ':
        vars[args[0]] = []
        if len(args) >= 2:
            for arg in args[1:]:
                if arg.startswith('##'):
                    arg = float(arg.removeprefix('##'))
                elif arg.startswith('#'):
                    arg = int(arg.removeprefix('#'))
                elif arg.startswith('&'):
                    arg = arg.removeprefix('&')
                elif arg.startswith('!'):
                    arg = get_bool(arg)
                else:
                    arg = vars[arg]
                vars[args[0]].append(arg)
    elif opcode == 'PSEQ':
        vars[args[0]] = PermaSequence()
        if len(args) >= 2:
            for arg in args[1:]:
                if arg.startswith('##'):
                    arg = float(arg.removeprefix('##'))
                elif arg.startswith('#'):
                    arg = int(arg.removeprefix('#'))
                elif arg.startswith('&'):
                    arg = arg.removeprefix('&')
                elif arg.startswith('!'):
                    arg = get_bool(arg)
                else:
                    arg = vars[arg]
                vars[args[0]].append(arg)
    elif opcode == 'PACK':
        temp_list = []
        if len(args) >= 2:
            for arg in args[1:]:
                if arg.startswith('##'):
                    arg = float(arg.removeprefix('##'))
                elif arg.startswith('#'):
                    arg = int(arg.removeprefix('#'))
                elif arg.startswith('&'):
                    arg = arg.removeprefix('&')
                elif arg.startswith('!'):
                    arg = get_bool(arg)
                else:
                    arg = vars[arg]
                temp_list.append(arg)
        vars[args[0]] = tuple(temp_list)
    elif opcode == 'MAP':
        vars[args[0]] = {}
        if len(args) >= 2:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'ADD':
        if args[0].startswith('##'):
            sum = float(args[0].removeprefix('##'))
        elif args[0].startswith('#'):
            sum = int(args[0].removeprefix('#'))
        else:
            sum = vars[args[0]]
        for arg in args[1:-1]:
            if arg.startswith('##'):
                sum += float(arg.removeprefix('##'))
            elif arg.startswith('#'):
                sum += int(arg.removeprefix('#'))
            else:
                sum += vars[arg]
        vars[args[-1:][0]] = sum
    elif opcode == 'SUB':
        if args[0].startswith('##'):
            diff = float(args[0].removeprefix('##'))
        elif args[0].startswith('#'):
            diff = int(args[0].removeprefix('#'))
        else:
            diff = vars[args[0]]
        for arg in args[1:-1]:
            if arg.startswith('##'):
                diff -= float(arg.removeprefix('##'))
            elif arg.startswith('#'):
                diff -= int(arg.removeprefix('#'))
            else:
                diff -= vars[arg]
        vars[args[-1:][0]] = diff
    elif opcode == 'MUL':
        if args[0].startswith('##'):
            prod = float(args[0].removeprefix('##'))
        elif args[0].startswith('#'):
            prod = int(args[0].removeprefix('#'))
        else:
            prod = vars[args[0]]
        for arg in args[1:-1]:
            if arg.startswith('##'):
                prod *= float(arg.removeprefix('##'))
            elif arg.startswith('#'):
                prod *= int(arg.removeprefix('#'))
            else:
                prod *= vars[arg]
        vars[args[-1:][0]] = prod
    elif opcode == 'DIV':
        if args[0].startswith('##'):
            quot = float(args[0].removeprefix('##'))
        elif args[0].startswith('#'):
            quot = int(args[0].removeprefix('#'))
        else:
            quot = vars[args[0]]
        for arg in args[1:-1]:
            if arg.startswith('##'):
                quot /= float(arg.removeprefix('##'))
            elif arg.startswith('#'):
                quot /= int(arg.removeprefix('#'))
            else:
                quot /= vars[arg]
        vars[args[-1:][0]] = quot
    elif opcode == 'FDIV':
        if args[0].startswith('##'):
            quot = float(args[0].removeprefix('##'))
        elif args[0].startswith('#'):
            quot = int(args[0].removeprefix('#'))
        else:
            quot = vars[args[0]]
        for arg in args[1:-1]:
            if arg.startswith('##'):
                quot //= float(arg.removeprefix('##'))
            elif arg.startswith('#'):
                quot //= int(arg.removeprefix('#'))
            else:
                quot //= vars[arg]
        vars[args[-1:][0]] = quot
    elif opcode == 'MOD':
        if args[0].startswith('##'):
            mod = float(args[0].removeprefix('##'))
        elif args[0].startswith('#'):
            mod = int(args[0].removeprefix('#'))
        else:
            mod = vars[args[0]]
        for arg in args[1:-1]:
            if arg.startswith('##'):
                mod %= float(arg.removeprefix('##'))
            elif arg.startswith('#'):
                mod %= int(arg.removeprefix('#'))
            else:
                mod %= vars[arg]
        vars[args[-1:][0]] = mod
    elif opcode == 'POW':
        if args[0].startswith('##'):
            pow = float(args[0].removeprefix('##'))
        elif args[0].startswith('#'):
            pow = int(args[0].removeprefix('#'))
        else:
            pow = vars[args[0]]
        for arg in args[1:-1]:
            if arg.startswith('##'):
                pow **= float(arg.removeprefix('##'))
            elif arg.startswith('#'):
                pow **= int(arg.removeprefix('#'))
            else:
                pow **= vars[arg]
        vars[args[-1:][0]] = pow
    elif opcode == 'ABS':
        if len(args) == 2:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            vars[args[1]] = abs(args[0])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'SQRT':
        if len(args) == 2:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            vars[args[1]] = math.sqrt(args[0])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'CBRT':
        if len(args) == 2:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            vars[args[1]] = math.cbrt(args[0])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'INC':
        if len(args) == 1:
            vars[args[0]] += 1
        elif len(args) == 2:
            vars[args[0]] += int(args[1].removeprefix('##').removeprefix('#'))
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'DEC':
        if len(args) == 1:
            vars[args[0]] -= 1
        elif len(args) == 2:
            vars[args[0]] -= int(args[1].removeprefix('##').removeprefix('#'))
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'PUSH':
        for arg in args:
            if arg.startswith(('#', '##', '&')):
                arg = arg.removeprefix('##').removeprefix('#').removeprefix('&')
            else:
                arg = vars[arg]
            print(arg, end='')
        print()
    elif opcode == 'PULL':
        if len(args) == 1:
            vars[args[0]] = input()
        elif len(args) == 2:
            if args[1].startswith(('#', '##', '&')):
                args[1] = args[1].removeprefix('##').removeprefix('#').removeprefix('&')
            else:
                args[1] = vars[args[1]]
            vars[args[0]] = input(args[1])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'INT':
        if len(args) == 1:
            vars[args[0]] = int(vars[args[0]])
        elif len(args) == 2:
            vars[args[1]] = int(vars[args[0]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'FLPT':
        if len(args) == 1:
            vars[args[0]] = float(vars[args[0]])
        elif len(args) == 2:
            vars[args[1]] = float(vars[args[0]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'STR':
        if len(args) == 1:
            vars[args[0]] = str(vars[args[0]])
        elif len(args) == 2:
            vars[args[1]] = str(vars[args[0]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'BOOL':
        var = get_bool(vars[args[0]])
        if len(args) == 1:
            vars[args[0]] = var
        elif len(args) == 2:
            vars[args[1]] = var
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'NULL':
        if len(args) == 1:
            vars[args[0]] = None
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'TYPE':
        if len(args) == 2:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if isinstance(args[0], int):
                t = "INT"
            elif isinstance(args[0], float):
                t = "FLPT"
            elif isinstance(args[0], str):
                t = "STR"
            elif isinstance(args[0], bool):
                t = "BOOL"
            elif args[0] is None:
                t = "NULL"
            elif isinstance(args[0], list):
                t = "SEQ"
            elif isinstance(args[0], PermaSequence):
                t = "PSEQ"
            elif isinstance(args[0], tuple):
                t = "PACK"
            elif isinstance(args[0], dict):
                t = "MAP"
            elif isinstance(args[0], Subroutine):
                t = "SUBR"
            elif isinstance(args[0], Function):
                t = "FUNC"
            else:
                t = "UNKNOWN"
            vars[args[1]] = t
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'LINK':
        if len(args) == 3:
            if args[0].startswith('&') and args[1].startswith('&'):
                vars[args[2]] = args[0].removeprefix('&') + args[1].removeprefix('&')
            elif args[0].startswith('&') and not args[1].startswith('&'):
                vars[args[2]] = args[0].removeprefix('&') + vars[args[1]]
            elif not args[0].startswith('&') and args[1].startswith('&'):
                vars[args[2]] = vars[args[0]] + args[1].removeprefix('&')
            else:
                vars[args[2]] = vars[args[0]] + vars[args[1]]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'FSTR':
        if len(args) == 2:
            vars[args[1]] = vars[args[0]].split()
        elif len(args) == 3:
            if args[2].startswith('&'):
                vars[args[1]] = vars[args[0]].split(args[2].removeprefix('&'))
            else:
                vars[args[1]] = vars[args[0]].split(vars[args[2]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'TSTR':
        if len(args) == 2:
            vars[args[1]] = ' '.join(vars[args[0]])
        elif len(args) == 3:
            if args[2].startswith('&'):
                vars[args[1]] = args[2].removeprefix('&').join(vars[args[0]])
            else:
                vars[args[1]] = vars[args[2]].join(vars[args[0]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'MIN':
        if len(args) >= 2:
            if len(args) == 2 and isinstance(vars[args[0]], (list, PermaSequence, tuple, dict)):
                vars[args[1]] = min(vars[args[0]])
            else:
                for i, arg in enumerate(args[:-1]):
                    if arg.startswith('##'):
                        args[i] = float(arg.removeprefix('##'))
                    elif arg.startswith('#'):
                        args[i] = int(arg.removeprefix('#'))
                    elif arg.startswith('&'):
                        args[i] = arg.removeprefix('&')
                    elif arg.startswith('!'):
                        args[i] = get_bool(arg)
                    else:
                        args[i] = vars[arg]
                vars[args[-1]] = min(args[:-1])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'MAX':
        if len(args) >= 2:
            if len(args) == 2 and isinstance(vars[args[0]], (list, PermaSequence, tuple, dict)):
                vars[args[1]] = max(vars[args[0]])
            else:
                for i, arg in enumerate(args[:-1]):
                    if arg.startswith('##'):
                        args[i] = float(arg.removeprefix('##'))
                    elif arg.startswith('#'):
                        args[i] = int(arg.removeprefix('#'))
                    elif arg.startswith('&'):
                        args[i] = arg.removeprefix('&')
                    elif arg.startswith('!'):
                        args[i] = get_bool(arg)
                    else:
                        args[i] = vars[arg]
                vars[args[-1]] = max(args[:-1])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'JOIN':
        if len(args) >= 2:
            for arg in args[1:]:
                if arg.startswith('##'):
                    arg = float(arg.removeprefix('##'))
                    vars[args[0]].append(arg)
                elif arg.startswith('#'):
                    arg = int(arg.removeprefix('#'))
                    vars[args[0]].append(arg)
                elif arg.startswith('&'):
                    arg = arg.removeprefix('&')
                    vars[args[0]].append(arg)
                elif arg.startswith('!'):
                    arg = get_bool(arg)
                else:
                    arg = vars[arg]
                    if isinstance(arg, (list, PermaSequence, tuple, dict)):
                        vars[args[0]].extend(arg)
                    else:
                        vars[args[0]].append(arg)
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'NEST':
        if len(args) >= 2:
            for arg in args[1:]:
                if isinstance(vars[arg], (list, PermaSequence, tuple, dict)):
                    vars[args[0]].append(vars[arg])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'POP':
        if len(args) == 2:
            if args[1].startswith('#'):
                i = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                i = vars[args[1]]
            vars[args[0]].pop(i)
        elif len(args) == 3:
            if args[1].startswith('#'):
                i = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                i = vars[args[1]]
            vars[args[2]] = vars[args[0]].pop(i)
    elif opcode == 'REM':
        if len(args) == 2:
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[2].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[2] = vars[args[2]]
            vars[args[0]].remove(args[1])
    elif opcode == 'GETI':
        if len(args) == 3:
            if args[1].startswith('#'):  # This handles both ints and floats
                v = int(args[1].removeprefix('##').removeprefix('#'))
            elif args[1].startswith('&'):
                v = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                v = get_bool(args[1])
            else:
                v = vars[args[1]]
            vars[args[2]] = vars[args[0]].index(v)
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'GET':
        if len(args) == 3:
            if args[1].startswith('#'):  # This handles both ints and floats
                i = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                i = vars[args[1]]
            vars[args[2]] = vars[args[0]][i]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'REST':
        if len(args) == 3:
            if args[1].startswith(('##', '#')):
                args[1] = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = vars[args[0]][args[1]:]
        elif len(args) == 4:
            if args[1].startswith(('##', '#')):
                args[1] = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                args[1] = vars[args[1]]
            if args[2].startswith(('##', '#')):
                args[2] = int(args[2].removeprefix('##').removeprefix('#'))
            else:
                args[2] = vars[args[2]]
            vars[args[3]] = vars[args[0]][args[1]:args[2]]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'SET':
        if len(args) == 3:
            if args[1].startswith('#'):  # This handles both ints and floats
                i = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                i = vars[args[1]]
            if args[2].startswith('##'):
                args[2] = float(args[2].removeprefix('##'))
            elif args[2].startswith('#'):
                args[2] = int(args[2].removeprefix('#'))
            elif args[2].startswith('&'):
                args[2] = args[2].removeprefix('&')
            elif args[2].startswith('!'):
                args[2] = get_bool(args[2])
            else:
                args[2] = vars[args[2]]
            vars[args[0]].insert(i, args[2])
    elif opcode == 'REPL':
        if len(args) == 3:
            if isinstance(vars[args[0]], (list, tuple)):
                if args[1].startswith('#'):
                    i = int(args[1].removeprefix('##').removeprefix('#'))
                else:
                    i = vars[args[1]]
                if args[2].startswith('##'):
                    args[2] = float(args[2].removeprefix('##'))
                    vars[args[0]][i] = args[2]
                elif args[2].startswith('#'):
                    args[2] = int(args[2].removeprefix('#'))
                    vars[args[0]][i] = args[2]
                elif args[2].startswith('&'):
                    args[2] = args[2].removeprefix('&')
                    vars[args[0]][i] = args[2]
                else:
                    args[2] = vars[args[2]]
                    vars[args[0]][i] = args[2]
            elif isinstance(vars[args[0]], PermaSequence):
                print("PSEQ values are read-only!")
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'MSET':
        if len(args) == 3:
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            if args[2].startswith('##'):
                args[2] = float(args[2].removeprefix('##'))
            elif args[2].startswith('#'):
                args[2] = int(args[2].removeprefix('#'))
            elif args[2].startswith('&'):
                args[2] = args[2].removeprefix('&')
            elif args[2].startswith('!'):
                args[2] = get_bool(args[2])
            else:
                args[2] = vars[args[2]]
            vars[args[0]][args[1]] = args[2]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'MGET':
        if len(args) == 3:
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = vars[args[0]][args[1]]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'MPOP':
        if len(args) == 2:
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[0]].pop(args[1])
        elif len(args) == 3:
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = vars[args[0]].pop(args[1])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'MPLI':
        if len(args) == 2:
            vars[args[1]] = vars[args[0]].popitem()
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'GRAB':
        if len(args) == 2:
            vars[args[1]] = tuple(vars[args[0]].items())
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'KEYS':
        if len(args) == 2:
            vars[args[1]] = tuple(vars[args[0]].keys())
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'VALS':
        if len(args) == 2:
            vars[args[1]] = tuple(vars[args[0]].values())
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'LEN':
        if len(args) == 2:
            vars[args[1]] = len(vars[args[0]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'WIPE':
        if len(args) == 1:
            vars[args[0]].clear()
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'COPY':
        if len(args) == 2:
            vars[args[1]] = vars[args[0]].copy()
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'EQ':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] == args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'NE':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] != args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'GT':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] > args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'LT':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] < args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'GE':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] >= args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'LE':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] <= args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'AND':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] and args[1]
    elif opcode == 'OR':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] or args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'NOT':
        if len(args) == 2:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            vars[args[1]] = not args[0]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'IS':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            if args[1].startswith('##'):
                args[1] = float(args[1].removeprefix('##'))
            elif args[1].startswith('#'):
                args[1] = int(args[1].removeprefix('#'))
            elif args[1].startswith('&'):
                args[1] = args[1].removeprefix('&')
            elif args[1].startswith('!'):
                args[1] = get_bool(args[1])
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = args[0] is args[1]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'IN':
        if len(args) == 3:
            if args[0].startswith('##'):
                args[0] = float(args[0].removeprefix('##'))
            elif args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('#'))
            elif args[0].startswith('&'):
                args[0] = args[0].removeprefix('&')
            elif args[0].startswith('!'):
                args[0] = get_bool(args[0])
            else:
                args[0] = vars[args[0]]
            vars[args[2]] = args[0] in vars[args[1]]
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'LOOP':
        if len(args) == 2:
            if args[0].startswith(('##', '#')):
                args[0] = int(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            vars[args[1]] = range(args[0])
        elif len(args) == 3:
            if args[0].startswith(('##', '#')):
                args[0] = int(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            if args[1].startswith(('##', '#')):
                args[1] = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = range(args[0], args[1])
        elif len(args) == 4:
            if args[0].startswith(('##', '#')):
                args[0] = int(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            if args[1].startswith(('##', '#')):
                args[1] = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                args = vars[args[1]]
            if args[2].startswith(('##', '#')):
                args[2] = int(args[2].removeprefix('##').removeprefix('#'))
            else:
                args[2] = vars[args[2]]
            vars[args[3]] = range(args[0], args[1], args[2])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'IF':
        if len(args) >= 2:
            if len(namespace['if_stack']) > 0:
                namespace['if_stack'].clear()  # Clear the if stack if it isn't already empty
            if vars[args[0]]:
                if isinstance(vars[args[1]], Subroutine):
                    vars[args[1]].run(namespace)
                    namespace['executing_subr'] = False
                else:  # This allows for custom Python types to be run
                    if len(args[2:-1]) == len(vars[args[1]].argdefs):
                        for i, arg in enumerate(args[2:-1]):
                            i += 2  # This accounts for the fact that we are excluding args[0] and args[1]
                            if arg.startswith('##'):
                                args[i] = float(arg.removeprefix('##'))
                            elif arg.startswith('#'):
                                args[i] = int(arg.removeprefix('#'))
                            elif arg.startswith('&'):
                                args[i] = arg.removeprefix('&')
                            elif arg.startswith('!'):
                                args[i] = get_bool(arg)
                            else:
                                args[i] = vars[args[i]]
                        vars[args[-1]] = vars[args[1]].run(namespace, args[2:-1])
                        namespace['executing_func'] = False
                    else:  # This simulates an exception
                        print(f"Function arguments do not match definitions in {args[1]}")
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                namespace['if_stack'].clear()
            else:
                namespace['if_stack'].append(vars[args[0]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'ELIF':
        if len(args) >= 2:
            if len(namespace['if_stack']) > 0:
                if not any(namespace['if_stack']) and vars[args[0]]:
                    if isinstance(vars[args[1]], Subroutine):
                        vars[args[1]].run(namespace)
                        namespace['executing_subr'] = False
                    else:  # This allows for custom Python types to be run
                        if len(args[2:-1]) == len(vars[args[1]].argdefs):
                            for i, arg in enumerate(args[2:-1]):
                                i += 2  # This accounts for the fact that we are excluding args[0] and args[1]
                                if arg.startswith('##'):
                                    args[i] = float(arg.removeprefix('##'))
                                elif arg.startswith('#'):
                                    args[i] = int(arg.removeprefix('#'))
                                elif arg.startswith('&'):
                                    args[i] = arg.removeprefix('&')
                                elif arg.startswith('!'):
                                    args[i] = get_bool(arg)
                                else:
                                    args[i] = vars[args[i]]
                            vars[args[-1]] = vars[args[1]].run(namespace, args[2:-1])
                            namespace['executing_func'] = False
                        else:  # This simulates an exception
                            print(f"Function arguments do not match definitions in {args[1]}")
                            namespace['stack'] = [None]
                            namespace['stack_pointer'] = 0
                            namespace['executing_subr'] = False
                            namespace['executing_func'] = False
                    namespace['if_stack'].clear()
                else:
                    namespace['if_stack'].append(vars[args[0]])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'ELSE':
        if len(args) >= 1:
            if len(namespace['if_stack']) > 0:
                if isinstance(vars[args[0]], Subroutine):
                    vars[args[0]].run(namespace)
                    namespace['executing_subr'] = False
                else:  # This allows for custom Python types to be run
                    if len(args[1:-1]) == len(vars[args[0]].argdefs):
                        for i, arg in enumerate(args[1:-1]):
                            i += 1  # This accounts for the fact that we are excluding args[0]
                            if arg.startswith('##'):
                                args[i] = float(arg.removeprefix('##'))
                            elif arg.startswith('#'):
                                args[i] = int(arg.removeprefix('#'))
                            elif arg.startswith('&'):
                                args[i] = arg.removeprefix('&')
                            elif arg.startswith('!'):
                                args[i] = get_bool(arg)
                            else:
                                args[i] = vars[args[i]]
                        vars[args[-1]] = vars[args[0]].run(namespace, args[1:-1])
                        namespace['executing_func'] = False
                    else:  # This simulates an exception
                        print(f"Function arguments do not match definitions in {args[0]}")
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                namespace['if_stack'].clear()
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'FOR':
        if len(args) >= 3:
            for item in vars[args[1]]:
                vars[args[0]] = item
                if isinstance(vars[args[2]], Subroutine):
                    vars[args[2]].run(namespace)
                    namespace['executing_subr'] = False
                else:  # This allows for custom Python types to be run
                    if len(args[3:-1]) == len(vars[args[2]].argdefs):
                        args_list = []
                        for i, arg in enumerate(args[3:-1]):
                            if arg.startswith('##'):
                                args_list.append(float(arg.removeprefix('##')))
                            elif arg.startswith('#'):
                                args_list.append(int(arg.removeprefix('#')))
                            elif arg.startswith('&'):
                                args_list.append(arg.removeprefix('&'))
                            elif arg.startswith('!'):
                                args_list.append(get_bool(arg))
                            else:
                                args_list.append(vars[args[i+3]])
                        vars[args[-1]] = vars[args[2]].run(namespace, args_list)
                        namespace['executing_func'] = False
                    else:  # This simulates an exception
                        print(f"Function arguments do not match definitions in {args[0]}")
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'FORI':
        if len(args) >= 4:
            for index, item in enumerate(vars[args[2]]):
                vars[args[0]] = index
                vars[args[1]] = item
                if isinstance(vars[args[3]], Subroutine):
                    vars[args[3]].run(namespace)
                    namespace['executing_subr'] = False
                else:  # This allows for custom Python types to be run
                    if len(args[4:-1]) == len(vars[args[3]].argdefs):
                        args_list = []
                        for i, arg in enumerate(args[4:-1]):
                            if arg.startswith('##'):
                                args_list.append(float(arg.removeprefix('##')))
                            elif arg.startswith('#'):
                                args_list.append(int(arg.removeprefix('#')))
                            elif arg.startswith('&'):
                                args_list.append(arg.removeprefix('&'))
                            elif arg.startswith('!'):
                                args_list.append(get_bool(arg))
                            else:
                                args_list.append(vars[args[i+4]])
                        vars[args[-1]] = vars[args[3]].run(namespace, args_list)
                        namespace['executing_func'] = False
                    else:  # This simulates an exception
                        print(f"Function arguments do not match definitions in {args[0]}")
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'ALA':
        if len(args) >= 2:
            while vars[args[0]]:
                if isinstance(vars[args[1]], Subroutine):
                    vars[args[1]].run(namespace)
                    namespace['executing_subr'] = False
                else:  # This allows for custom Python types to be run
                    if len(args[2:-1]) == len(vars[args[1]].argdefs):
                        args_list = []
                        for i, arg in enumerate(args[2:-1]):
                            if arg.startswith('##'):
                                args_list.append(float(arg.removeprefix('##')))
                            elif arg.startswith('#'):
                                args_list.append(int(arg.removeprefix('#')))
                            elif arg.startswith('&'):
                                args_list.append(arg.removeprefix('&'))
                            elif arg.startswith('!'):
                                args_list.append(get_bool(arg))
                            else:
                                args_list.append(vars[args[i+2]])
                        vars[args[-1]] = vars[args[1]].run(namespace, args_list)
                        namespace['executing_func'] = False
                    else:  # This simulates an exception
                        print(f"Function arguments do not match definitions in {args[0]}")
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'DALA':
        if len(args) >= 2:
            while True:
                if isinstance(vars[args[1]], Subroutine):
                    vars[args[1]].run(namespace)
                    namespace['executing_subr'] = False
                else:  # This allows for custom Python types to be run
                    if len(args[2:-1]) == len(vars[args[1]].argdefs):
                        args_list = []
                        for i, arg in enumerate(args[2:-1]):
                            if arg.startswith('##'):
                                args_list.append(float(arg.removeprefix('##')))
                            elif arg.startswith('#'):
                                args_list.append(int(arg.removeprefix('#')))
                            elif arg.startswith('&'):
                                args_list.append(arg.removeprefix('&'))
                            elif arg.startswith('!'):
                                args_list.append(get_bool(arg))
                            else:
                                args_list.append(vars[args[i+2]])
                        vars[args[-1]] = vars[args[1]].run(namespace, args_list)
                        namespace['executing_func'] = False
                    else:  # This simulates an exception
                        print(f"Function arguments do not match definitions in {args[0]}")
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                if not vars[args[0]]:
                    break
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'RAND':
        if len(args) == 1:
            vars[args[0]] = random.randrange(0, 65536)
        elif len(args) == 3:
            if args[0].startswith(('##', '#')):
                args[0] = int(args[0].removeprefix('##').removeprefix('#'))
            else:
                args = vars[args[0]]
            if args[1].startswith(('##', '#')):
                args[1] = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                args[1] = vars[args[1]]
            vars[args[2]] = random.randrange(args[0], args[1])
        else:
            print(f"Wrong arguments in {instruction}")
    elif opcode == 'EXIT':
        if len(args) == 0:
            sys.exit()
        elif len(args) == 1:
            if args[0].startswith(('##', '#')):
                args[0] = int(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            sys.exit(args[0])
        else:
            print(f"Wrong arguments in {instruction}")
    else:
        if opcode != '' and opcode not in ('GIVE','TAKE','SYNC'):
            print(f"Unknown instruction {instruction}")
    vars = {var.upper(): vars[var] for var in vars}

namespace = {
    'vars': {},
    'killed_vars': [],
    'kill_length': 0,
    'stack': [None],
    'stack_pointer': 0,
    'if_stack': [],
    'executing_subr': False,
    'executing_func': False
}
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("mlmcr Revision 2")
        print("Copyright (C) 2023  BarbeMCR")
        print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} on {sys.platform}")
        print("BarbeMCR welcomes you to programming hell!")
        while True:
            try:
                invalid_vars = []
                if namespace['stack'][0] is not None:
                    if isinstance(namespace['stack'][namespace['stack_pointer']], Function):
                        prompt = '    ' + '  '*(len(namespace['stack'])-1) + '> '
                    else:
                        prompt = '    ' + '  '*(len(namespace['stack'])-1) + '@ '
                else:
                    prompt = '  @ '
                instruction = get_input(prompt)
                if instruction.upper()[:6] == 'PYEVAL':  # Check special 'PYEVAL' and 'PYEXEC' opcodes
                    args = instruction.split(',')
                    args[0] = args[0].split(' ', 1)
                    args = args[0] + args[1:]
                    args.pop(0)
                    for index, arg in enumerate(args):
                        args[index] = arg.lstrip()
                    if len(args) == 1:
                        eval(args[0])
                    elif len(args) == 2:
                        vars[args[1]] = eval(args[0])
                    else:
                        print("'PYEVAL' requires at most two arguments")
                elif instruction.upper()[:6] == 'PYEXEC':
                    args = instruction.split(' ', 1)
                    args.pop(0)
                    exec(args[0])
                else:
                    if namespace['stack'][0] is not None:
                        namespace['stack'][namespace['stack_pointer']].add_instruction(namespace, instruction)
                    else:
                        parse(namespace, instruction)
                for var in namespace['vars']:
                    if not var.startswith('$') or not all(char in set(string.hexdigits) for char in var.removeprefix('$')):
                        print("Variables names must start with '$' and contain only hexadecimal characters")
                        invalid_vars.append(var)
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                        namespace['if_stack'] = []
                for var in invalid_vars:
                    del namespace['vars'][var]
            except KeyboardInterrupt:
                namespace['stack'] = [None]
                namespace['stack_pointer'] = 0
                namespace['executing_subr'] = False
                namespace['executing_func'] = False
                namespace['if_stack'] = []
                print("\nInput interrupted. Type 'EXIT' if you want to quit")
            except KeyError:
                namespace['stack'] = [None]
                namespace['stack_pointer'] = 0
                namespace['executing_subr'] = False
                namespace['executing_func'] = False
                namespace['if_stack'] = []
                print(f"Exception in {instruction}: Unknown variable or key")
            except RecursionError:
                namespace['stack'] = [None]
                namespace['stack_pointer'] = 0
                namespace['executing_subr'] = False
                namespace['executing_func'] = False
                namespace['if_stack'] = []
                print(f"Exception in {instruction}: Recursion too deep")
            except Exception:
                namespace['stack'] = [None]
                namespace['stack_pointer'] = 0
                namespace['executing_subr'] = False
                namespace['executing_func'] = False
                namespace['if_stack'] = []
                print(f"Exception in {instruction}: Generic run-time error")
    else:
        if sys.argv[1].endswith('.mlmcr'):
            with open(sys.argv[1], 'r') as file:
                for line in file:
                    try:
                        invalid_vars = []
                        line = line.lstrip().rstrip('\n')
                        if line.upper()[:6] == 'PYEVAL':  # Check special 'PYEVAL' and 'PYEXEC' opcodes
                            args = line.split(',')
                            args[0] = args[0].split(' ', 1)
                            args = args[0] + args[1:]
                            args.pop(0)
                            for index, arg in enumerate(args):
                                args[index] = arg.lstrip()
                            if len(args) == 1:
                                eval(args[0])
                            elif len(args) == 2:
                                vars[args[1]] = eval(args[0])
                            else:
                                print("'PYEVAL' requires at most two arguments")
                        elif line.upper()[:6] == 'PYEXEC':
                            args = line.split(' ', 1)
                            args.pop(0)
                            exec(args[0])
                        else:
                            if namespace['stack'][0] is not None:
                                namespace['stack'][namespace['stack_pointer']].add_instruction(namespace, line)
                            else:
                                parse(namespace, line)
                        for var in namespace['vars']:
                            if not var.startswith('$') or not all(char in set(string.hexdigits) for char in var.removeprefix('$')):
                                print("Variables names must start with '$' and contain only hexadecimal characters")
                                invalid_vars.append(var)
                        for var in invalid_vars:
                            del vars[var]
                    except KeyboardInterrupt:
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                        namespace['if_stack'] = []
                        sys.exit()
                    except KeyError:
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                        namespace['if_stack'] = []
                        print(f"Exception in {line}: Unknown variable or key")
                    except RecursionError:
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                        namespace['if_stack'] = []
                        print(f"Exception in {line}: Recursion too deep")
                    except Exception:
                        namespace['stack'] = [None]
                        namespace['stack_pointer'] = 0
                        namespace['executing_subr'] = False
                        namespace['executing_func'] = False
                        namespace['if_stack'] = []
                        print(f"Exception in {line}: Generic run-time error")
        else:
            print("File name must end with '.mlmcr' to be parsed")
            sys.exit()