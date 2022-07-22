import ply.lex as lex

class Lexical(object):
    #tokens = ('IDENT', 'OP_ARIT', 'DELIM', 'CTE_REAL', 'OP_LOG', 'CTE_ALFA', 'PAL_RES', 'OP_REL', 'CTE_ENTERA', 'COMMENT')
    tokens = ('IDENT', 'COMENTARIO', 'CTE_ENTERA', 'CTE_REAL', 'CTE_ALFA',
              'OP_ASIG', 'OP_REL',
              'TIPO', 'CONSTANTES', 'VARIABLES', 'PROGRAMA', 'FIN', 'DE', 'FUNCION', 'PROCEDIMIENTO',
              'INICIO', 'LIMPIA', 'SI', 'DESDE', 'REPETIR', 'MIENTRAS', 'CUANDO', 'REGRESA', 'IMPRIMENL',
              'IMPRIME', 'LEE', 'INTERRUMPE', 'CONTINUA', 'HACER', 'SINO', 'EL', 'VALOR', 'HASTA', 'QUE', 'SE',
              'CUMPLA', 'SEA', 'OTRO', 'PROTOTIPOS','DECR', 'INCR', 'Y', 'O', 'NO',
              'PAREN_EMPIEZA', 'PAREN_TERMINA', 'CORCHETE_EMPIEZA', 'CORCHETE_TERMINA', 'PUNTOS_DOBLES', 'PUNTO_COMA',
              'PUNTO', 'COMA', 'MAS', 'MENOS', 'MOD', 'MULTI', 'DIV', 'POTENCIA', 'FALSO', 'VERDADERO',
              'PROGRAMA_ERR', 'CTE_REAL_ERR', 'FIN_ERR', 'TIPO_ERR', 'INICIO_ERR', 'CTE_REAL_ERR2', 'CTE_ENTERA_ERR', 'POTENCIA_ERR', 'newline'
              )

    def __init__(self, f, lines):
        self.lines = lines
        self.lexemes = []
        self.filename = f
        self.out = open(f + '.lex', 'a')
        self.out.write('------------------------------------\n')
        self.out.write('Lexeme      Token       Line\n')
        self.out.write('------------------------------------\n')
        self.err = open(f + '.err', 'a')
        self.err.write('------------------------------------\n')
        self.err.write('Line      Error       Desc      Line (Exp)\n')
        self.err.write('------------------------------------\n')
        self.errors = []

    def new_lex(self, token_name, attr_value, line):
        self.lexemes.append([token_name, attr_value])
        self.out.write(f"<{token_name}>: {attr_value}   [{line}]\n")

    def new_err(self, line, value, desc):
        self.err.write(f"{line}\t{value}\t<lexical>{desc}\t{self.lines[line-1]}\n")
        self.errors.append(f"{line}\t{value}\t<lexical>{desc}\t{self.lines[line-1]}\n")

    # line counter for error handling
    def t_newline(self, t):
        r'\n+'
        #print('newline found', t.lexer.lineno)
        t.lexer.lineno += len(t.value)


    # pattern for lexemes of a token: regex
    # must be named t_TOKEN

    # comments
    def t_COMENTARIO(self, t):
        r'//.*'
        #print(f"COMMENT {t.value}")
        self.new_lex("COMENTARIO", t.value, t.lexer.lineno)

    # strings
    def t_CTE_ALFA(self, t):
        r'"[a-zA-Z0-9_ \[\]\)\(<:\¿\?,\$\#\'\?\!\¡/=*+-\^{}%°\|]*"'
        #print(f"CTE_ALFA {t.value}")
        self.new_lex("CTE_ALFA", t.value, t.lexer.lineno)
        return t

    # a?!(s) will match a if a is not followed by s
    # here are all tokens for each reserved words
    def t_TIPO(self, t):
        r'[e|E]ntero(?![a-zA-Z0-9])|[r|R]eal(?![a-zA-Z0-9])|[a|A]lfabetico(?![a-zA-Z0-9])|[l|L]ogico(?![a-zA-Z0-9])'
        self.new_lex("TIPO", t.value, t.lexer.lineno)
        return t

    def t_CONSTANTES(self, t):
        r'[c|C]onstantes(?![a-zA-Z0-9])'
        self.new_lex("CONSTANTES", t.value, t.lexer.lineno)
        return t

    def t_VARIABLES(self, t):
        r'[v|V]ariables(?![a-zA-Z0-9])'
        self.new_lex("VARIABLES", t.value, t.lexer.lineno)
        return t

    def t_PROGRAMA(self, t):
        r'[p|P]rograma(?![a-zA-Z0-9])'
        self.new_lex("PROGRAMA", t.value, t.lexer.lineno)
        return t

    def t_ignore_PROGRAMA_ERR(self, t):
        r'[p|P]rograma([a-zA-Z0-9]+)'
        self.new_err(t.lexer.lineno, t.value, "Unexpected keyword for PROGRAMA token")
        #self.parser.errok()
        #self.parser.token()
        #return t

    def t_FIN(self, t):
        r'[f|F]in(?![a-zA-Z0-9])'
        self.new_lex("FIN", t.value, t.lexer.lineno)
        return t

    def t_ignore_FIN_ERR(self, t):
        r'[f|F]in([a-zA-Z0-9]+)'
        self.new_err(t.lexer.lineno, t.value, "Unexpected keyword for FIN token")

    def t_DE(self, t):
        r'[d|D]e(?![a-zA-Z0-9])'
        self.new_lex("DE", t.value, t.lexer.lineno)
        return t

    def t_FUNCION(self, t):
        r'[f|F]uncion(?![a-zA-Z0-9])'
        self.new_lex("FUNCION", t.value, t.lexer.lineno)
        return t

    def t_PROCEDIMIENTO(self, t):
        r'[p|P]rocedimiento(?![a-zA-Z0-9])'
        self.new_lex("PROCEDIMIENTO", t.value, t.lexer.lineno)
        return t

    def t_INICIO(self, t):
        r'([i|I]nicio)(?![a-zA-Z0-9])'
        self.new_lex("INICIO", t.value, t.lexer.lineno)
        return t

    def t_ignore_INICIO_ERR(self, t):
        r'[i|I]nicio([a-zA-Z0-9]+)'
        self.new_err(t.lexer.lineno, t.value, "Unexpected keyword for INICIO token")

    def t_LIMPIA(self, t):
        r'[l|L]impia(?![a-zA-Z0-9])'
        self.new_lex("LIMPIA", t.value, t.lexer.lineno)
        return t

    def t_SI(self, t):
        r'[s|S]i(?![a-zA-Z0-9])'
        self.new_lex("SI", t.value, t.lexer.lineno)
        return t

    def t_DESDE(self, t):
        r'[d|D]esde(?![a-zA-Z0-9])'
        self.new_lex("DESDE", t.value, t.lexer.lineno)
        return t

    def t_REPETIR(self, t):
        r'[r|R]epetir(?![a-zA-Z0-9])'
        self.new_lex("REPETIR", t.value, t.lexer.lineno)
        return t

    def t_MIENTRAS(self, t):
        r'[m|M]ientras(?![a-zA-Z0-9])'
        self.new_lex("MIENTRAS", t.value, t.lexer.lineno)
        return t

    def t_CUANDO(self, t):
        r'[c|C]uando(?![a-zA-Z0-9])'
        self.new_lex("CUANDO", t.value, t.lexer.lineno)
        return t

    def t_REGRESA(self, t):
        r'[r|R]egresa(?![a-zA-Z0-9])'
        self.new_lex("REGRESA", t.value, t.lexer.lineno)
        return t

    def t_IMPRIMENL(self, t):
        r'[i|I]mprimenl(?![a-zA-Z0-9])'
        self.new_lex("IMPRIMENL", t.value, t.lexer.lineno)
        return t

    def t_IMPRIME(self, t):
        r'[i|I]mprime(?![a-zA-Z0-9])'
        self.new_lex("IMPRIME", t.value, t.lexer.lineno)
        return t

    def t_LEE(self, t):
        r'[l|L]ee(?![a-zA-Z0-9])'
        self.new_lex("LEE", t.value, t.lexer.lineno)
        return t

    def t_INTERRUMPE(self, t):
        r'[i|I]nterrumpe(?![a-zA-Z0-9])'
        self.new_lex("INTERRUMPE", t.value, t.lexer.lineno)
        return t

    def t_CONTINUA(self, t):
        r'[c|C]ontinua(?![a-zA-Z0-9])'
        self.new_lex("CONTINUA", t.value, t.lexer.lineno)
        return t

    def t_HACER(self, t):
        r'[h|H]acer(?![a-zA-Z0-9])'
        self.new_lex("HACER", t.value, t.lexer.lineno)
        return t

    def t_SINO(self, t):
        r'[s|S]ino(?![a-zA-Z0-9])'
        self.new_lex("SINO", t.value, t.lexer.lineno)
        return t

    def t_EL(self, t):
        r'[e|E]l(?![a-zA-Z0-9])'
        self.new_lex("EL", t.value, t.lexer.lineno)
        return t

    def t_VALOR(self, t):
        r'[v|V]alor(?![a-zA-Z0-9])'
        self.new_lex("VALOR", t.value, t.lexer.lineno)
        return t

    def t_HASTA(self, t):
        r'[h|H]asta(?![a-zA-Z0-9])'
        self.new_lex("HASTA", t.value, t.lexer.lineno)
        return t

    def t_QUE(self, t):
        r'[q|Q]ue(?![a-zA-Z0-9])'
        self.new_lex("QUE", t.value, t.lexer.lineno)
        return t

    def t_SE(self, t):
        r'[S|s]e(?![a-zA-Z0-9])'
        self.new_lex("SE", t.value, t.lexer.lineno)
        return t

    def t_CUMPLA(self, t):
        r'[c|C]umpla(?![a-zA-Z0-9])'
        self.new_lex("CUMPLA", t.value, t.lexer.lineno)
        return t

    def t_SEA(self, t):
        r'[s|S]ea(?![a-zA-Z0-9])'
        self.new_lex("SEA", t.value, t.lexer.lineno)
        return t

    def t_OTRO(self, t):
        r'[o|O]tro(?![a-zA-Z0-9])'
        self.new_lex("OTRO", t.value, t.lexer.lineno)
        return t

    def t_PROTOTIPOS(self, t):
        r'[p|P]rototipos(?![a-zA-Z0-9])'
        self.new_lex("PROTOTIPOS", t.value, t.lexer.lineno)
        return t

    def t_DECR(self, t):
        r'[d|D]ecr(?![a-zA-Z0-9])'
        self.new_lex("DECR", t.value, t.lexer.lineno)
        return t

    def t_INCR(self, t):
        r'[i|I]ncr(?![a-zA-Z0-9])'
        self.new_lex("INCR", t.value, t.lexer.lineno)
        return t

    # relational
    def t_OP_REL(self, t):
        r'=|<>|<|>|<=|>='
        #print(f"OP_REL {t.value}")
        self.new_lex("OP_REL", t.value, t.lexer.lineno)
        return t

    # logic
    def t_O(self, t):
        r'o(?![\S])'
        self.new_lex("O", t.value, t.lexer.lineno)
        return t

    def t_Y(self, t):
        r'y(?![\S])'
        self.new_lex("Y", t.value, t.lexer.lineno)
        return t

    def t_NO(self, t):
        r'no(?![\S])'
        self.new_lex("NO", t.value, t.lexer.lineno)
        return t

    def t_VERDADERO(self, t):
        r'[v|V]erdadero(?![\S])'
        self.new_lex("VERDADERO", t.value, t.lexer.lineno)
        return t

    def t_FALSO(self, t):
        r'[f|F]also(?![\S])'
        self.new_lex("FALSO", t.value, t.lexer.lineno)
        return t

    # identifiers
    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        #print(f"IDENT {t.value}")
        self.new_lex("IDENT", t.value, t.lexer.lineno)
        return t

    # floats: 3.2 or 3E10 accepted
    def t_CTE_REAL(self, t):
        r'([0-9]+[\.][0-9]+)|([0-9]+(e|E)[0-9]+)'
        #print(f"CTE_REAL {t.value}")
        self.new_lex("CTE_REAL", t.value, t.lexer.lineno)
        return t

    def t_ignore_CTE_REAL_ERR(self, t):
        r'[0-9]+[\.][a-zA-Z]+'
        self.new_err(t.lexer.lineno, t.value, "Floating point number ends with non digit")

    def t_ignore_CTE_REAL_ERR2(self, t):
        r'[0-9]+[\.][( |\t|\s)]+'
        self.new_err(t.lexer.lineno, t.value, "Floating point number cannot end with a dot")

    # integers
    def t_CTE_ENTERA(self, t):
        r'[1-9][0-9]*(?![a-zA-Z])'
        #print(f"CTE_ENTERA {t.value}")
        self.new_lex("CTE_ENTERA", t.value, t.lexer.lineno)
        return t

    def t_ignore_CTE_ENTERA_ERR(self, t):
        r'[1-9][0-9]*([a-zA-Z])+'
        self.new_err(t.lexer.lineno, t.value, "Unexpected alpha value in integer: did you miss an identifier?")

    # assignment
    def t_OP_ASIG(self, t):
        r':='
        #print(f"OP_ASIG {t.value}")
        self.new_lex("OP_ASIG", t.value, t.lexer.lineno)
        return t

    # punctuation
    def t_PAREN_EMPIEZA(self, t):
        r'\('
        self.new_lex("PAREN_EMPIEZA", t.value, t.lexer.lineno)
        return t

    def t_PAREN_TERMINA(self, t):
        r'\)'
        self.new_lex("PAREN_TERMINA", t.value, t.lexer.lineno)
        return t

    def t_CORCHETE_EMPIEZA(self, t):
        r'\['
        self.new_lex("CORCHETE_EMPIEZA", t.value, t.lexer.lineno)
        return t

    def t_CORCHETE_TERMINA(self, t):
        r'\]'
        self.new_lex("CORCHETE_TERMINA", t.value, t.lexer.lineno)
        return t

    def t_PUNTOS_DOBLES(self, t):
        r':'
        self.new_lex("PUNTOS_DOBLES", t.value, t.lexer.lineno)
        return t

    def t_PUNTO_COMA(self, t):
        r';'
        self.new_lex("PUNTO_COMA", t.value, t.lexer.lineno)
        return t

    def t_PUNTO(self, t):
        r'\.'
        self.new_lex("PUNTO", t.value, t.lexer.lineno)
        return t

    def t_COMA(self, t):
        r','
        self.new_lex("COMA", t.value, t.lexer.lineno)
        return t

    # operators
    def t_MAS(self, t):
        r'[\+]'
        self.new_lex("MAS", t.value, t.lexer.lineno)
        return t

    def t_MENOS(self, t):
        r'[\-]'
        self.new_lex("MENOS", t.value, t.lexer.lineno)
        return t

    def t_MOD(self, t):
        r'[\%]'
        self.new_lex("MOD", t.value, t.lexer.lineno)
        return t

    def t_MULTI(self, t):
        r'[\*]'
        self.new_lex("MULTI", t.value, t.lexer.lineno)
        return t

    def t_DIV(self, t):
        r'[\/]'
        self.new_lex("DIV", t.value, t.lexer.lineno)
        return t

    def t_POTENCIA(self, t):
        r'[\^]'
        self.new_lex("POTENCIA", t.value, t.lexer.lineno)
        return t

    def t_ignore_POTENCIA_ERR(self, t):
        r'(?!")\*\*(?!")'
        self.new_err(t.lexer.lineno, t.value, "Unexpected '**' found: power expresions use ^")


    t_ignore = ' \t'

    # do not interrupt execution when an error is found
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.new_err(t.lexer.lineno, t.value, "Unexpected character '%s'" % t.value[0])
        # skip ahead one character
        t.lexer.skip(1)

    # init the lex
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)