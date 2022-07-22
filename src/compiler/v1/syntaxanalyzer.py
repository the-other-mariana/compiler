from lexanalyzer import Lexical
import ply.yacc as yacc
from collections import deque
from commons import SymbolTable

# docs here: https://www.dabeaz.com/ply/ply.html#ply_nn23

class Syntactical(object):
    tokens = Lexical.tokens
    stack = deque()
    # which tokens have the same precedence and type of precedence
    precedence = (
        ('left', 'MAS', 'MENOS'),
        ('left', 'MULTI', 'DIV'),
        ('left', 'MOD'),
        ('left', 'OP_REL'),
        ('left', 'PAREN_EMPIEZA', 'PAREN_TERMINA'),
        ('right', 'CORCHETE_EMPIEZA', 'CORCHETE_TERMINA'),
        ('left', 'FIN'),

        ('right', 'OP_ASIG'),
        ('right', 'PROTOTIPOS'),
        ('right', 'PUNTO_COMA'),
        ('right', 'CONSTANTES', 'VARIABLES'),
        ('right', 'PROCEDIMIENTO', 'FUNCION'),
        ('left', 'IDENT', 'INICIO', 'SI', 'MIENTRAS')
    )


    def __init__(self, f, lines):
        self.err = open(f + '.err', 'a')
        self.exe = open(f + '.eje', 'a')
        self.lines = lines
        self.errors = []
        self.symtab = SymbolTable(f)

    def p_programa(self, p):
        'program : constantes variables protfuncproc funcproc PROGRAMA block FIN DE PROGRAMA PUNTO'

    def p_variables(self, p):
        '''variables : VARIABLES gpovars
                     | empty
        '''
        print("[found] variables")

    def p_gpovars(self, p):
        '''gpovars : gpoids PUNTOS_DOBLES TIPO PUNTO_COMA gpovars
                   | gpoids PUNTOS_DOBLES TIPO PUNTO_COMA
        '''
        # gpo_vars is found at every line of var declaration
        print('[found] gpo_vars')
        # not empty

        # print type: L R E A
        print(p[3].upper(), p[3][0].upper())
        # take out last ; so that stack is ready to handle
        if self.stack[-1] == ';':
            self.stack.pop()
        # send to handle var
        self.symtab.handle_var(self.stack, p.lineno(3), p[3][0].upper(), 'V')

    def p_gpovars_empty(self, p):
        'gpovars : empty'

    def p_gpovars_error(self, p):
        '''gpovars : gpoids error TIPO PUNTO_COMA gpovars
                   | gpoids error TIPO PUNTO_COMA
        '''
        print("Expected PUNTOS_DOBLES in variable declaration")
        self.new_err(p.lineno(2), p[2].value, "Expected PUNTOS_DOBLES in variable declaration")

    def p_gpovars_error2(self, p):
        '''gpovars : gpoids PUNTOS_DOBLES error PUNTO_COMA gpovars
                   | gpoids PUNTOS_DOBLES error PUNTO_COMA
        '''
        print("Expected TIPO in variable definition")
        self.new_err(p.lineno(3), p[3].value, "Expected TIPO in variable definition")

    def p_gpoids(self, p):
        '''gpoids : IDENT COMA gpoidsinner
                  | IDENT opasig COMA gpoidsinner
        '''
        print("[found] gpoids")
        # push ident and ; since end of gpids production
        self.stack.append(p[1])
        self.stack.append(";")

    def p_gpoids_dim(self, p):
        '''gpoids : IDENT dimens COMA gpoidsinner
                  | IDENT dimens
        '''
        print("[found] gpoids_dim", p[1], p[2])
        if p[2] != None:
            self.stack.append(p[1])
            self.stack.append('ARRAY')
            self.stack.append(";")
        else:
            self.stack.append(p[1])
            self.stack.append(";")

    def p_gpoids_inner(self, p):
        '''gpoidsinner : IDENT COMA gpoidsinner
                       | IDENT opasig COMA gpoidsinner
                       | IDENT
        '''
        # push ident only since inner id production
        self.stack.append(p[1])

    def p_gpoids_inner_dim(self, p):
        '''gpoidsinner : IDENT dimens COMA gpoidsinner
                       | IDENT dimens
        '''
        # push ident only since inner id production
        print('[found] gpoids_inner_dim')
        self.stack.append(p[1])
        self.stack.append('ARRAY')

    def p_gpoids_empty(self, p):
        'gpoids : empty'

    def p_gpoids_inner_empty(self, p):
        'gpoidsinner : empty'

    def p_gpoids_error1(self, p):
        '''gpoids : IDENT dimens error gpoids
                  | IDENT error gpoids
                  | IDENT opasig error gpoids
        '''
        print("Expected COMA between each variable declaration")
        self.new_err(p.lineno(2), p[2].value, "Expected COMA between each variable declaration")

    def p_dimens(self, p):
        'dimens : CORCHETE_EMPIEZA valor CORCHETE_TERMINA dimens'
        print("[found] dimension", p[1], p[2], p[3])
        self.stack.append('dim')

    def p_dimens_empty(self, p):
        'dimens : empty'

    def p_dimens_error1(self, p):
        '''dimens : CORCHETE_EMPIEZA valor error dimens
        '''
        print("Expected CORCHETE_TERMINA to close dimensions")
        self.new_err(p.lineno(3), p[3].value, "Expected CORCHETE_TERMINA to close dimensions")

    def p_dimens_error2(self, p):
        '''dimens : error valor CORCHETE_TERMINA dimens
        '''
        print("Expected CORCHETE_EMPIEZA of dimension")
        self.new_err(p.lineno(1), p[1].value, "Expected CORCHETE_EMPIEZA of dimension")

    def p_opasig1(self, p):
        'opasig : OP_ASIG CTE_ENTERA'

    def p_opasig2(self, p):
        'opasig : OP_ASIG IDENT'

    def p_opasigEmpty(self, p):
        'opasig : empty'

    def p_valor(self, p):
        '''valor : exprlog
        '''
        print('[found] valor')

    def p_constantes(self, p):
        '''constantes : CONSTANTES gpoconst
                      | empty
        '''
        print('[found] constantes')

    def p_gpoconst_int(self, p):
        '''gpoconst : IDENT OP_ASIG CTE_ENTERA PUNTO_COMA
                    | IDENT OP_ASIG CTE_ENTERA PUNTO_COMA gpoconst
        '''
        print('[found] gpo_const_int')
        # push ident
        self.stack.append(p[1])
        value = p[3]
        # push type
        self.stack.append('E')
        # push value
        self.stack.append(value)
        print(self.stack)
        self.symtab.handle_const(self.stack, p.lineno(1), p[1])

    def p_gpoconst_float(self, p):
        '''gpoconst : IDENT OP_ASIG CTE_REAL PUNTO_COMA
                    | IDENT OP_ASIG CTE_REAL PUNTO_COMA gpoconst
                    | empty
        '''
        print('[found] gpo_const_float')
        # push ident
        self.stack.append(p[1])
        value = p[3]
        # push type
        self.stack.append('R')
        # push value
        self.stack.append(value)
        print(self.stack)
        self.symtab.handle_const(self.stack, p.lineno(1), p[1])


    def p_prototipo1(self, p):
        '''protfuncproc : PROTOTIPOS gpofuncproc FIN DE PROTOTIPOS PUNTO_COMA
                        | empty
        '''
        print("[found] function prototype")

    def p_protfuncproc(self, p):
        '''gpofuncproc : protfunc
                        | protproc
                        | protproc gpofuncproc
                        | protfunc gpofuncproc
                        '''

    def p_protfunc(self, p):
        'protfunc : FUNCION IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO PUNTO_COMA'
        print('[found] funcproc')
        # push return type
        self.stack.append(p[7])
        # push ident
        self.stack.append(p[2])
        self.stack.append('protfunc')
        self.symtab.handle_protfunc(self.stack, p.lineno(2))


    def p_protfunc_error1(self, p):
        'protfunc : FUNCION error PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO PUNTO_COMA'
        print("Expected identifier in function prototype")
        self.new_err(p.lineno(2), p[2].value, "Expected identifier in function prototype")

    def p_protproc(self, p):
        'protproc : PROCEDIMIENTO IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTO_COMA'
        print("[found] procedimiento prototype")
        # push ident
        self.stack.append(p[2])
        self.stack.append('protproc')
        self.symtab.handle_protproc(self.stack, p.lineno(2))

    def p_protproc_empty(self, p):
        'protproc : empty'

    def p_protproc_error1(self, p):
        'protproc : PROCEDIMIENTO error PAREN_EMPIEZA params PAREN_TERMINA  PUNTO_COMA'
        print("Expected identififier in proc prototype")
        self.new_err(p.lineno(2), p[2].value, "Expected identififier in proc prototype")

    def p_params(self, p):
        'params : gpopars PUNTOS_DOBLES TIPO params2'
        print('[found] params')
        # push type
        self.stack.append(p[3])

    def p_params_empty(self, p):
        'params : empty'

    def p_params_error1(self, p):
        '''params : gpopars PUNTOS_DOBLES error params2
        '''
        print("Error in parameter type")
        self.new_err(p.lineno(3), p[3].value, "Error in parameter type")

    def p_params_error2(self, p):
        'params : gpopars error TIPO params2'
        print("Expected PUNTOS_DOBLES before type of param")
        self.new_err(p.lineno(2), p[2].value, "Expected PUNTOS_DOBLES before type of param")

    def p_params2(self, p):
        'params2 : PUNTO_COMA params'

    def p_params2_empty(self, p):
        'params2 : empty'

    def p_gpopars(self, p):
        '''gpopars : IDENT COMA gpopars2
        '''
        # end of params mark
        #self.stack.append(';')
        # push ident
        self.stack.append(p[1])

    def p_gpopars_end(self, p):
        'gpopars : IDENT'
        self.stack.append(';')
        self.stack.append(p[1])

    def p_gpopars2(self, p):
        '''gpopars2 : IDENT COMA gpopars2
        '''
        # push ident
        self.stack.append(p[1])

    def p_gpopars2_end(self, p):
        'gpopars2 : IDENT'
        self.stack.append(';')
        self.stack.append(p[1])

    def p_funcproc(self, p):
        '''funcproc : procedimiento funcproc
                    | funcion funcproc
                    | empty
        '''
        print("[found] funcproc")

    def p_procedimiento(self, p):
        '''procedimiento : PROCEDIMIENTO IDENT PAREN_EMPIEZA params PAREN_TERMINA variables INICIO block FIN DE PROCEDIMIENTO PUNTO_COMA'''
        print('[found] full procedimiento')
        # push ident
        self.stack.append(p[2])
        self.stack.append('proc')

    def p_funcion(self, p):
        '''funcion : FUNCION IDENT PAREN_EMPIEZA params PAREN_TERMINA PUNTOS_DOBLES TIPO variables INICIO block FIN DE FUNCION PUNTO_COMA'''
        print('[found] full funcion')
        # push type
        self.stack.append(p[7])
        # push ident
        self.stack.append(p[2])
        self.stack.append('func')

    def p_block(self, p):
        '''block : estatuto PUNTO_COMA block
                 | estatuto PUNTO_COMA
        '''
        print("[found] block")

    def p_semicolon_error(self, p):
        '''block : estatuto error
                 | estatuto error block
        '''
        print("Expected PUNTO_COMA at the end of line", p.lineno(2))
        self.new_err(p.lineno(2), p[2].value, "Expected PUNTO_COMA at the end of line")

    def p_estatuto(self, p):
        '''estatuto : si
                    | lfunc
                    | LIMPIA
                    | desde
                    | repetir
                    | mientras
                    | cuando
                    | regresa
                    | asigna
                    | imprime
                    | imprimenl
                    | lee
                    | INTERRUMPE
                    | CONTINUA
                    | empty
        '''
        print("[found] estatuto")

    def p_si(self, p):
        'si : SI PAREN_EMPIEZA exprlog PAREN_TERMINA HACER bckesp sino'
        print('[found] si')
        self.stack.append('SI')
        stmt_stack = self.symtab.handle_stmt(self.stack, p.lineno(1))
        while len(stmt_stack) > 0:
            code = stmt_stack.pop()
            if code:
                self.symtab.exe_string += code

    def p_sino(self, p):
        '''sino : SINO bckesp
                | empty
        '''
        print('[found] sino')

    def p_bckesp(self, p):
        '''bckesp : estatuto
                  | INICIO block FIN
                  | empty
        '''
        print("[found] bckesp")

    def p_desde(self, p):
        '''desde : DESDE EL VALOR DE asigna HASTA expr DECR CTE_ENTERA bckesp
                 | DESDE EL VALOR DE asigna HASTA expr INCR CTE_ENTERA bckesp
        '''
        print("[found] desde")

    def p_desde_error1(self, p):
        '''desde : DESDE EL VALOR DE asigna HASTA expr error bckesp'''
        print("Expected incr/decr in desde", p.lineno(8))
        self.new_err(p.lineno(8), p[8].value, "Expected incr/decr in desde")

    def p_repetir(self, p):
        'repetir : REPETIR block HASTA QUE PAREN_EMPIEZA exprlog PAREN_TERMINA'
        print("[found] repetir")

    def p_mientras(self, p):
        'mientras : MIENTRAS SE CUMPLA QUE exprlog bckesp'
        print("[found] mientras")

    def p_asigna(self, p):
        'asigna : IDENT udim OP_ASIG exprlog'
        print("[found] asigna")

    def p_cuando(self, p):
        'cuando : CUANDO EL VALOR DE IDENT INICIO gposea otro FIN'
        print("[found] cuando")
        # push ident
        self.stack.append(p[5])
        self.stack.append('cuando')

    def p_otro(self, p):
        '''otro : OTRO PUNTOS_DOBLES bckesp
                | empty
        '''
        print("[found] otro")

    def p_gposea(self, p):
        '''gposea : SEA gpoconst PUNTOS_DOBLES bckesp gposea
        '''
        print("[found] gposea")
        self.stack.append('SEA')

    def p_gposea_empty(self, p):
        'gposea : empty'

    def p_gpoconst(self, p):
        'gpoconst : CTE_ALFA gpoconst2'
        self.stack.append(p[1])

    def p_gpoconst3(self, p):
        'gpoconst3 : CTE_ALFA gpoconst2'
        self.stack.append(p[1])

    def p_gpoconst2(self, p):
        'gpoconst2 : COMA gpoconst3'

    def p_gpoconst2_empty(self, p):
        'gpoconst2 : empty'
        self.stack.append(';')

    def p_regresa(self, p):
        'regresa : REGRESA PAREN_EMPIEZA exprlog PAREN_TERMINA'
        print("[found] regresa")

    def p_udim(self, p):
        '''udim : CORCHETE_EMPIEZA expr CORCHETE_TERMINA udim
                | empty
        '''
        print("[found] udim")

    def p_exprlog(self, p):
        '''exprlog : opy
                   | opy O exprlog
        '''
        print("[found] exprlog")
        if len(p) > 2:
            self.stack.append(p[2].upper())

    def p_opy(self, p):
        '''opy : opno
               | opno Y opy
        '''
        print("[found] opy")
        if len(p) > 2:
            self.stack.append(p[2].upper())

    def p_opno(self, p):
        '''opno : oprel
                | NO oprel
        '''
        print("[found] opno")
        if len(p) > 2:
            self.stack.append(p[1].upper())

    def p_oprel(self, p):
        '''oprel : expr
                 | expr OP_REL oprel
        '''
        print("[found] oprel")
        if len(p) > 2:
            self.stack.append(p[2])

    def p_expr(self, p):
        '''expr : multi
                | multi MAS expr
                | multi MENOS expr
        '''
        print("[found] expr")
        if len(p) > 2:
            self.stack.append(p[2])

    def p_multi(self, p):
        '''multi : expo
                 | expo MULTI multi
                 | expo DIV multi
                 | expo MOD multi
                 | empty
        '''
        print("[found] multi")
        if len(p) > 2:
            self.stack.append(p[2])

    def p_expo(self, p):
        '''expo : signo
                | signo POTENCIA expo
        '''
        print("[found] exponent")
        if len(p) > 2:
            self.stack.append(p[2])

    def p_signo(self, p):
        '''signo : termino
                 | MENOS termino
        '''
        print("[found] signo")
        if len(p) > 2:
            self.stack.append(p[2])

    # check ident dimens
    def p_termino(self, p):
        '''termino : IDENT
                   | CTE_ENTERA
                   | CTE_REAL
                   | CTE_ALFA
                   | VERDADERO
                   | FALSO
        '''
        print("[found] simple termino", p[1])
        # push either ident or value
        self.stack.append(p[1])

    def p_termino2(self, p):
        '''termino :
                   | IDENT udim
                   | lfunc'''
        print("[found] complex termino")

    def p_lfunc(self, p):
        'lfunc : IDENT PAREN_EMPIEZA uparams PAREN_TERMINA'
        print("[found] lfunc")
        # push ident
        self.stack.append(p[1])

    def p_lfunc_error1(self, p):
        'lfunc : IDENT PAREN_EMPIEZA error PAREN_TERMINA'
        print("Expected logical expression in function call", p.lineno(3))
        self.new_err(p.lineno(3), p[3].value, "Expected logical expression in function call")

    def p_imprime(self, p):
        'imprime : IMPRIME begin gpoexp PAREN_TERMINA'
        print('[found] imprime func')
        print('b4', self.stack)
        if len(self.stack) > 0 and self.stack[0] != ';':
            self.stack.appendleft(';')
        self.stack.append("IMPRIME")
        self.stack.append(";")
        print(self.stack)
        self.symtab.handle_imprime(self.stack)

    def p_begin(self, p):
        'begin : PAREN_EMPIEZA'
        print('[found] begin', p[1])
        print('begin', self.stack)
        if len(self.stack) > 0 and self.stack[0] != ';':
            self.stack.appendleft(';')
        if len(self.stack) > 0 and self.stack[-1] != ';':
            self.stack.append(';')

    def p_imprime_error1(self, p):
        'imprime : IMPRIME error gpoexp PAREN_TERMINA'
        print("Expected parenthesis at the start of IMPRIME statement", p.lineno(2))
        self.new_err(p.lineno(2), p[2].value, "Expected parenthesis at the start of IMPRIME statement")

    def p_imprime_error2(self, p):
        'imprime : IMPRIME begin gpoexp error'
        print("Expected parenthesis at the end of IMPRIME statement", p.lineno(4))
        self.new_err(p.lineno(4), p[4].value, "Expected parenthesis at the end of IMPRIME statement")

    def p_imprimenl(self, p):
        'imprimenl : IMPRIMENL begin gpoexp PAREN_TERMINA'
        print('[found] imprimenl func')
        print('b4', self.stack)
        if len(self.stack) > 0 and self.stack[0] != ';':
            self.stack.appendleft(';')
        self.stack.append("IMPRIMENL")
        self.stack.append(";")
        print(self.stack)
        self.symtab.handle_imprimenl(self.stack, p.lineno(3))

    def p_imprimenl_error1(self, p):
        'imprimenl : IMPRIMENL begin gpoexp error'
        print("Expected parenthesis at the end of IMPRIMENL statement", p.lineno(4))
        self.new_err(p.lineno(4), p[4].value, "Expected parenthesis at the end of IMPRIMENL statement ")

    def p_imprimenl_error2(self, p):
        'imprimenl : IMPRIMENL error gpoexp PAREN_TERMINA'
        print("Expected parenthesis at the start of IMPRIMENL statement", p.lineno(2))
        self.new_err(p.lineno(2), p[2].value, "Expected parenthesis at the start of IMPRIMENL statement")

    def p_lee(self, p):
        'lee : LEE PAREN_EMPIEZA IDENT PAREN_TERMINA'
        print("[found] lee", p[3], p[4])
        # push ident
        self.stack.append(p[3])
        self.stack.append('LEE')
        self.stack.append(';')
        self.symtab.handle_lee(self.stack, p.lineno(3))

    def p_lee_dim(self, p):
        'lee : LEE PAREN_EMPIEZA IDENT dimens PAREN_TERMINA'
        print("[found] lee_dim", p[1], p[2], p[3], p[4], p[5])
        # push ident
        self.stack.append(p[3])
        self.stack.append('LEE_DIM')
        self.stack.append(';')
        self.symtab.handle_lee_dim(self.stack, p.lineno(3))

    def p_gpoexp(self, p):
        '''gpoexp : exprlog
                  | exprlog COMA gpoexp
        '''
        print("[found] gpoexp")

    def p_uparams(self, p):
        '''uparams : exprlog
                   | exprlog COMA uparams
        '''
        print("[found] uparams")

    def p_empty(self, p):
        'empty :'
        pass

    # write syntax errors in .err file
    def new_err(self, line, value, desc):
        self.err.write(f"{line}\t{value}\t<syntax>{desc}\t{self.lines[line-1]}\n")
        self.errors.append(f"{line}\t{value}\t<syntax>{desc}\t{self.lines[line-1]}\n")

    # syntax error general

    def p_error(self, p):

        if p:
            print(f"Syntax error at '{p.value}' ({p.type}), in line: {p.lineno}, col {p.lexpos}")
            self.new_err(p.lineno, p.value, f"Syntax error at '{p.value}' ({p.type}), in line: {p.lineno}, col {p.lexpos}")
        else:
            print("Syntax error at EOF")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)