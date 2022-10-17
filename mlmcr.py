# mlmcr, the unnecessary Assembly-like programming language
# Copyright (C) 2022  BarbeMCR

import sys
import string
import time

class PermaSequence:
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
    def index(self, value):
        return self.sequence.index(value)
    def clear(self):
        self.sequence.clear()

def get_input(prompt):
    user_input = input(prompt).lstrip()
    return user_input
    
def get_bool(value):
    return bool(int(value.removeprefix('!')))
    
def parse(vars, killed_vars, kill_lenght, instruction):
    opcode = instruction.upper()[:4]
    args = instruction.split(',')
    args[0] = args[0].split(' ', 1)
    args = args[0] + args[1:]
    args.pop(0)
    for index, arg in enumerate(args):
        args[index] = arg.lstrip()
    if opcode.startswith(';'):
        pass  # Starting a line with ; allows for comments as elif is used below
    elif opcode.startswith('PUT'):
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
            print("Wrong arguments!")
    elif opcode.startswith('DEL'):
        if len(args) == 1:
            del vars[args[0]]
        else:
            print("Wrong arguments!")
    elif opcode.startswith('KILL'):
        if len(args) == 1:
            killed_vars.append(vars[args[0]])
            if len(killed_vars) > kill_lenght:
                killed_vars.pop(0)
            del vars[args[0]]
        elif len(args) == 2:
            killed_vars.append(vars[args[0]])
            if len(killed_vars) > kill_lenght:
                killed_vars.pop(0)
            del vars[args[0]]
            vars[args[1]] = len(killed_vars) - 1
        else:
            print("Wrong arguments!")
    elif opcode.startswith('WAKE'):
        if len(args) == 2:
            if args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            vars[args[1]] = killed_vars[args[0]]
            killed_vars.pop(args[0])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('KSET'):
        if len(args) == 1:
            if args[0].startswith('#'):
                args[0] = int(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            if 0 <= args[0] <= 65536:
                kill_lenght = args[0]
            elif args[0] < 0:
                kill_lenght = 0
            else:
                kill_lenght = 65536
        else:
            print("Wrong arguments!")
    elif opcode.startswith('KGET'):
        if len(args) == 1:
            vars[args[0]] = len(killed_vars) - 1
        else:
            print("Wrong arguments!")
    elif opcode.startswith('HALT'):
        if len(args) == 1:
            if args[0].startswith('#'):
                args[0] = float(args[0].removeprefix('##').removeprefix('#'))
            else:
                args[0] = vars[args[0]]
            time.sleep(args[0])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('SEQ'):
        vars[args[0]] = []
        if len(args) >= 2:
            for arg in args[1:]:
                if arg.startswith('##'):
                    arg = float(arg.removeprefix('##'))
                elif arg.startswith('#'):
                    arg = int(arg.removeprefix('#'))
                elif arg.startswith('&'):
                    arg = arg.removeprefix('&')
                else:
                    arg = vars[arg]
                vars[args[0]].append(arg)
    elif opcode.startswith('PSEQ'):
        vars[args[0]] = PermaSequence()
        if len(args) >= 2:
            for arg in args[1:]:
                if arg.startswith('##'):
                    arg = float(arg.removeprefix('##'))
                elif arg.startswith('#'):
                    arg = int(arg.removeprefix('#'))
                elif arg.startswith('&'):
                    arg = arg.removeprefix('&')
                else:
                    arg = vars[arg]
                vars[args[0]].append(arg)
    elif opcode.startswith('PACK'):
        temp_list = []
        if len(args) >= 2:
            for arg in args[1:]:
                if arg.startswith('##'):
                    arg = float(arg.removeprefix('##'))
                elif arg.startswith('#'):
                    arg = int(arg.removeprefix('#'))
                elif arg.startswith('&'):
                    arg = arg.removeprefix('&')
                else:
                    arg = vars[arg]
                temp_list.append(arg)
        vars[args[0]] = tuple(temp_list)
    elif opcode.startswith('ADD'):
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
    elif opcode.startswith('SUB'):
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
    elif opcode.startswith('MUL'):
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
    elif opcode.startswith('DIV'):
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
    elif opcode.startswith('FDIV'):
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
    elif opcode.startswith('MOD'):
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
    elif opcode.startswith('POW'):
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
    elif opcode.startswith('INC'):
        if len(args) == 1:
            vars[args[0]] += 1
        elif len(args) == 2:
            vars[args[0]] += int(args[1].removeprefix('##').removeprefix('#'))
        else:
            print("Wrong arguments!")
    elif opcode.startswith('DEC'):
        if len(args) == 1:
            vars[args[0]] -= 1
        elif len(args) == 2:
            vars[args[0]] -= int(args[1].removeprefix('##').removeprefix('#'))
        else:
            print("Wrong arguments!")
    elif opcode.startswith('PUSH'):
        print(*[vars[arg.upper()] for arg in args])
    elif opcode.startswith('PULL'):
        vars[args[0]] = input(args[1] if len(args) > 1 else '')
    elif opcode.startswith('INT'):
        if len(args) == 1:
            vars[args[0]] = int(vars[args[0]])
        elif len(args) == 2:
            vars[args[1]] = int(vars[args[0]])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('FLPT'):
        if len(args) == 1:
            vars[args[0]] = float(vars[args[0]])
        elif len(args) == 2:
            vars[args[1]] = float(vars[args[0]])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('STR'):
        if len(args) == 1:
            vars[args[0]] = str(vars[args[0]])
        elif len(args) == 2:
            vars[args[1]] = str(vars[args[0]])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('BOOL'):
        var = get_bool(vars[args[0]])
        if len(args) == 1:
            vars[args[0]] = var
        if len(args) == 2:
            vars[args[1]] = var
        else:
            print("Wrong arguments!")
    elif opcode.startswith('LINK'):
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
            print("Wrong arguments!")
    elif opcode.startswith('FSTR'):
        if len(args) == 2:
            vars[args[1]] = vars[args[0]].split()
        elif len(args) == 3:
            if args[2].startswith('&'):
                vars[args[1]] = vars[args[0]].split(args[2].removeprefix('&'))
            else:
                vars[args[1]] = vars[args[0]].split(vars[args[2]])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('TSTR'):
        if len(args) == 2:
            vars[args[1]] = ' '.join(vars[args[0]])
        elif len(args) == 3:
            if args[2].startswith('&'):
                vars[args[1]] = args[2].removeprefix('&').join(vars[args[0]])
            else:
                vars[args[1]] = vars[args[2]].join(vars[args[0]])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('JOIN'):
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
                else:
                    arg = vars[arg]
                    if isinstance(arg, (list, PermaSequence, tuple)):
                        vars[args[0]].extend(arg)
                    else:
                        vars[args[0]].append(arg)
        else:
            print("Wrong arguments!")
    elif opcode.startswith('NEST'):
        if len(args) >= 2:
            for arg in args[1:]:
                if isinstance(vars[arg], (list, PermaSequence, tuple)):
                    vars[args[0]].append(vars[arg])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('POP'):
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
    elif opcode.startswith('REM'):
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
    elif opcode.startswith('GETI'):
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
            print("Wrong arguments!")
    elif opcode.startswith('GET'):
        if len(args) == 3:
            if args[1].startswith('#'):  # This handles both ints and floats
                i = int(args[1].removeprefix('##').removeprefix('#'))
            else:
                i = vars[args[1]]
            vars[args[2]] = vars[args[0]][i]
        else:
            print("Wrong arguments!")
    elif opcode.startswith('SET'):
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
            else:
                args[2] = vars[args[2]]
            vars[args[0]].insert(i, args[2])
    elif opcode.startswith('REPL'):
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
            print("Wrong arguments!")
    elif opcode.startswith('LEN'):
        if len(args) == 2:
            vars[args[1]] = len(vars[args[0]])
        else:
            print("Wrong arguments!")
    elif opcode.startswith('IN'):
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
            vars[args[2]] = args[1] in vars[args[0]]
    elif opcode.startswith('WIPE'):
        vars[args[0]].clear()
    elif opcode.startswith('EXIT'):
        sys.exit()
    else:
        print("Unknown instruction")
    vars = {var.upper(): vars[var] for var in vars}
    return vars, kill_lenght

vars = {}
killed_vars = []
kill_lenght = 256
if len(sys.argv) == 1:
    print("mlmcr Revision 1")
    print("Copyright (C) 2022  BarbeMCR")
    print(f"Python {sys.version} on {sys.platform}")
    print("BarbeMCR welcomes you to programming hell!")
    while True:
        try:
            invalid_vars = []
            instruction = get_input('  @ ')
            if instruction.upper()[:6].startswith('PYEVAL'):  # Check special 'PYEVAL' and 'PYEXEC' opcodes
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
                    print("'PYEVAL' requires at most two arguments.")
            elif instruction.upper()[:6].startswith('PYEXEC'):
                args = instruction.split(' ', 1)
                args.pop(0)
                exec(args[0])
            else:
                vars, kill_lenght = parse(vars, killed_vars, kill_lenght, instruction)
            for var in vars:
                if not var.startswith('$') or not all(char in set(string.hexdigits) for char in var.removeprefix('$')):
                    print("Variables names must start with '$' and contain only hexadecimal characters")
                    invalid_vars.append(var)
            for var in invalid_vars:
                del vars[var]
        except KeyboardInterrupt:
            print("\nInput interrupted. Type 'EXIT' if you want to quit")
        except Exception:
            print("Exception: Generic run-time error")
else:
    if sys.argv[1].endswith('.mlmcr'):
        with open(sys.argv[1], 'r') as file:
            for line in file:
                try:
                    invalid_vars = []
                    line = line.lstrip().rstrip('\n')
                    if line.upper()[:6].startswith('PYEVAL'):  # Check special 'PYEVAL' and 'PYEXEC' opcodes
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
                            print("'PYEVAL' requires at most two arguments.")
                    elif line.upper()[:6].startswith('PYEXEC'):
                        args = line.split(' ', 1)
                        args.pop(0)
                        exec(args[0])
                    else:
                        vars, kill_lenght = parse(vars, killed_vars, kill_lenght, line)
                    for var in vars:
                        if not var.startswith('$') or not all(char in set(string.hexdigits) for char in var.removeprefix('$')):
                            print("Variables names must start with '$' and contain only hexadecimal characters")
                            invalid_vars.append(var)
                    for var in invalid_vars:
                        del vars[var]
                except KeyboardInterrupt:
                    exit()
                except Exception:
                    print("Exception: Generic run-time error")
    else:
        print("File name must end with '.mlmcr' to be parsed")
        exit()