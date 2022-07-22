from collections import deque
import numpy as np

class Node:
    def __init__(self):
        self.id = ''
        self.token = None
        self.dtype = None
        self.shape = np.zeros(2, dtype=int)
        self.scope = None
        self.locals = dict()
        self.value = None
        self.udef = True

    def get_unicode(self):
        if isinstance(self.value, str):
            return ord(self.value)
        elif isinstance(self.value, int):
            return chr(self.value)
        return None
    def __str__(self):
        return f"{self.id},{self.token},{self.dtype},{self.shape},{self.scope},{self.locals},#,\n"


class SymbolTable:
    def __init__(self, f):
        self.table = dict()
        self.err = open(f + '.err', 'a')
        self.exe = open(f + '.eje', 'a')
        self.lineno = 1
        self.exe_string = ''
        self.logical = [['Y', 'O', 'NO'], [15, 16, 17]]
        self.relational = [['<', '>', '<=', '>=', '<>', '='], [9, 10, 11, 12, 13, 14]]
        self.block_stmts = deque()
        self.labels = dict()
        self.stmts = ['LEE', 'IMPRIME', 'IMPRIMENL', 'INTERRUMPE', 'CONTINUA', 'LIMPIA', 'REGRESA',
                      'SI', 'SINO', 'DESDE', 'REPETIR', 'MIENTRAS', 'CUANDO', 'HACER', 'SEA',
                      'EL', 'QUE', 'SE', 'VALOR', 'CUMPLA', 'OTRO', 'OK']

    def __str__(self):
        s = ""
        for k, v in self.table.items():
            s += f"{k},{v.token},{v.dtype},{v.shape[0]},{v.shape[1]},"
            if v.locals != None:
                s += self.get_locals(v.locals)
            s += '#,\n'
        return s

    def get_symtab_string(self):
        s = ""
        for k, v in self.table.items():
            s += f"{k},{v.token},{v.dtype},{v.shape[0]},{v.shape[1]},"
            if v.locals != None:
                s += self.get_locals(v.locals)
            s += '#,\n'
        return s

    def get_locals(self, subtable):
        s = ""
        for k, v in subtable.items():
            s += f"{v.token},{v.dtype},{v.shape[0]},{v.shape[1]},{k},"
        return s

    def put(self, key, node, line, ident):
        if self.exists(key):
            self.new_err(line, node.id, f'{ident}: Variable redeclaration', 'semantic')
        else:
            self.table[key] = node

    def get(self, key):
        if key in self.table.keys():
            return self.table[key]
        return None

    def exists(self, key):
        if key in self.table.keys():
            return True
        return False

    # order top-bottom: value-C-dtype-id
    def handle_const(self, stack, line, ident):
        while len(stack) > 0:
            n = Node()
            n.value = stack.pop()
            n.token = 'C'
            n.dtype = stack.pop() # E R
            if n.dtype == 'E':
                n.value = int(n.value)
            elif n.dtype == 'R':
                n.value = float(n.value)
            n.id = stack.pop()

            if self.exists(n.id):
                self.new_err(line, n.id, f'{ident}: Constant redeclaration', 'semantic')
            else:
                self.table[n.id] = n
    def handle_var(self, stack, line, dtype, token):
        arr_stack = deque()
        while True:
            print(stack)
            print(arr_stack)
            n = Node()
            curr = stack.pop()
            if curr == ';':
                break
            elif curr == 'ARRAY':
                # before ARRAY there was the array name, so pop it
                n.id = stack.pop()
                n.token = token
                n.dtype = dtype
                arr_stack.append(n)
            elif curr == 'dim':
                n = arr_stack.pop()
                # extra dim
                #stack.pop()
                next_next = stack.pop()
                if next_next == 'dim':
                    next_next = stack.pop()
                    self.validate_dim(next_next, n, 1, line)
                    next_next = stack.pop()
                self.validate_dim(next_next, n, 0, line)
                self.put(n.id, n, line, n.id)
                print(n)
            else:
                n.id = curr
                n.token = token
                n.dtype = dtype
                n.udef = False
                self.put(n.id, n, line, n.id)
                print(n)
            if len(stack) == 0:
                break

    def handle_params(self, stack, token, func_node):
        types = ['ENTERO', 'REAL', 'ALFABETICO', 'LOGICO']
        if token.upper() in types:
            while True:
                print(stack)
                curr = stack.pop()
                # end of params mark
                if curr == ';':
                    break
                if self.exists(curr):
                    n = Node()
                    # params are P tokens
                    n.token = 'P'
                    # first letter is type
                    n.dtype = token.upper()[0]
                    n.scope = func_node.id
                    scope_node = self.get(curr)
                    if scope_node:
                        scope_node.locals[func_node.id] = n
        else:
            # append params type again
            stack.append(token)

    def handle_protfunc(self, stack, line):
        print('start', stack)
        # pop the protfunc string
        stack.pop()
        func_node = Node()
        func_node.id = stack.pop()
        func_node.token = 'F'
        # pop return type
        func_node.dtype = stack.pop().upper()[0]
        self.put(func_node.id, func_node, line, func_node.id)
        # pop params type
        token = stack.pop()
        self.handle_params(stack, token, func_node)
        print('end', stack)

    def handle_protproc(self, stack, line):
        print(stack)
        # pop protproc string
        stack.pop()
        proc_node = Node()
        proc_node.id = stack.pop()
        # procedures have no type
        proc_node.token = 'P'
        proc_node.dtype = 'I'
        self.put(proc_node.id, proc_node, line, proc_node.id)
        token = stack.pop()
        self.handle_params(stack, token, proc_node)

    def decide_code(self, curr, line):
        if '"' in curr:
            s = f'{self.lineno} LIT {curr}, 0\n'
            self.lineno += 1
            return s
        if self.exists(curr):
            s = f'{self.lineno} LOD {curr}, 0\n'
            self.lineno += 1
            return s
        else:
            self.new_err(line, curr, 'Access to undeclared variable inside statement', 'semantic')
            return None

    def handle_if(self, stack, line):
        print(stack)
        load = None
        if_stack = deque()
        while len(stack) > 0:
            print(stack)
            print(if_stack)
            curr = stack.pop()
            if curr in self.logical[0]:
                for l, c in zip(self.logical[0], self.logical[1]):
                    if curr == l:
                        if_stack.append(f'{self.lineno} OPR 0, {c}\n')
                        self.lineno += 1
            elif curr in self.relational[0]:
                for r, c in zip(self.relational[0], self.relational[1]):
                    if curr == r:
                        if_stack.append(f'{self.lineno} OPR 0, {c}\n')
                        self.lineno += 1
            elif curr in self.stmts:
                if curr == 'OK':
                    load = curr
                else:
                    stack.append(curr)
                    if load:
                        stack.append(load)
                    return if_stack
            else:
                if_stack.append(self.decide_code(curr, line))
        if load:
            stack.append(load)
        return if_stack

    def handle_stmt(self, stack, line):
        print(stack)
        curr_stack = deque()
        while len(stack) > 0:
            curr = stack.pop()
            curr_stack = deque()
            if curr == 'SI':
                curr_stack = self.handle_if(stack, line)
            elif curr == 'SEA':
                pass
            else:
                break
        print(curr_stack)
        return curr_stack

    def handle_imprime(self, stack):
        print(stack)
        stack.pop()
        while len(stack) > 0:
            curr = stack.pop()
            if curr == ';':
                break
            if curr == 'IMPRIME':
                lit = stack.pop()
                # load literal to execution stack
                self.add_eje(self.lineno, 'LIT', lit, 0)
                # show the literal on screen
                self.add_eje(self.lineno, 'OPR', 0, 20)

    def handle_imprimenl(self, stack, line):
        # semicolon mark
        stack.pop()
        param_stack = deque()
        while len(stack) > 0:
            curr = stack.pop()
            if curr == ';':
                break
            if curr == 'IMPRIMENL':
                curr = stack.pop()
                try:
                    param_stack.append(curr)
                except IndexError:
                    self.new_err(line, 'Imprimenl', 'No parameters in Imprimenl function', 'semantic')

        while len(param_stack) > 0:
            to_print = param_stack.pop()
            if '"' in to_print:
                # load literal to execution stack
                self.add_eje(self.lineno, 'LIT', to_print, 0)
                # show the literal on screen
                self.add_eje(self.lineno, 'OPR', 0, 21)
            else:
                # printing a variable
                if self.exists(to_print):
                    # load literal to execution stack
                    self.add_eje(self.lineno, 'LIT', to_print, 0)
                    # show the literal on screen
                    self.add_eje(self.lineno, 'OPR', 0, 21)
                else:
                    self.new_err(line, to_print, f"Unable to print value of undeclared variable '{to_print}'", 'semantic')

    def handle_lee(self, stack, line):
        # get semicolon
        stack.pop()
        # get LEE
        stack.pop()
        id = stack.pop()
        if not self.exists(id):
            self.new_err(line, id, f"Unable to store input in undeclared variable '{id}'", 'semantic')
        else:
            self.add_eje(self.lineno, 'OPR', id, 19)

    def handle_lee_dim(self, stack, line):
        # get semicolon
        print(stack)
        stack.pop()
        # get LEE
        stack.pop()
        id = stack.pop()
        if not self.exists(id):
            self.new_err(line, id, f"Unable to store input in undeclared variable '{id}'", 'semantic')
        else:
            while len(stack) > 0:
                print(stack)
                curr = stack.pop()
                if curr == 'dim':
                    idx = stack.pop()
                    if idx.isdigit():
                        self.add_eje(self.lineno, 'LIT', idx, 0)
                        self.add_eje(self.lineno, 'STO', 0, id)
                    elif self.exists(idx):
                        self.add_eje(self.lineno, 'LOD', idx, 0)
                        self.add_eje(self.lineno, 'STO', 0, id)

    def validate_dim(self, next_next, n, idx, line):
        if next_next.isdigit():
            n.shape[idx] = int(next_next)
        else:
            try:
                # error: float as dimension
                err_val = float(next_next)
                self.new_err(line, next_next, 'Array dimensions must be integer - float found', 'semantic')
            except ValueError:
                # variable as dimension size
                if self.exists(next_next):
                    v = self.get(next_next)
                    if v.dtype == 'E':
                        if v.value:
                            n.shape[idx] = v.value
                        else:
                            self.new_err(line, next_next, 'Cannot use unassigned variable as array dimension', 'semantic')
                    elif v.dtype == 'R':
                        self.new_err(line, next_next, 'Array dimensions must be integer - float variable found', 'semantic')
                else:
                    self.new_err(line, next_next, 'Undeclared variable as array dimension', 'semantic')

    def new_err(self, line, value, error, type):
        self.err.write(f"{line}\t{value}\t<{type}>{error}\n")

    def add_eje(self, line, code, param1, param2):
        #self.exe.write(f"{line} {code} {param1}, {param2}\n")
        self.exe_string += f"{line} {code} {param1}, {param2}\n"
        self.lineno += 1

    def write_exe(self):
        self.exe.write(self.get_symtab_string())
        self.exe.write('@\n')
        self.exe.write(self.exe_string)