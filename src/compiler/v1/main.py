import sys
from lexanalyzer import Lexical
from syntaxanalyzer import Syntactical

if len(sys.argv) < 2:
    print("[ERROR] No source file provided.")
else:
    filename = sys.argv[1]
    f = open(filename)
    lines = []
    with open(filename) as file:
        lines = file.readlines()

    no_ext = filename.split('.')[0]
    ext = filename.split('.')[1]

    lex = Lexical(no_ext, lines)
    lex.build()
    syntax = Syntactical(no_ext, lines)
    syntax.build()

    o = syntax.parser.parse(f.read())

    lex.out.close()
    lex.err.close()
    print(lex.errors)
    print(syntax.errors)
    print(syntax.symtab)
    print(syntax.stack)
    syntax.symtab.write_exe()