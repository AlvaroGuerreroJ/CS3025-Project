import ply.lex as lex

reserved = (
    "CONTINUE",
    "ELSE",
    "FOR",
    "IF",
    "INT",
    "RETURN",
    "VOID",
    "WHILE",
    # Exercise specific
    "MAIN",
    "PUTW",
    "PUTS",
)
reserved_dict = {r.lower(): r for r in reserved}

tokens = reserved + (
    # Function/variable identifier
    "ID",
    # Literals
    "INT_LITERAL",
    "STRING_LITERAL",
    # Arithmetic operators (+, -, *, /, %)
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    # Logic operators (||, &&, !)
    "LOR",
    "LAND",
    "LNOT",
    # Comparison operators (<, <=, >, >=, ==, !=)
    "LT",
    "LE",
    "GT",
    "GE",
    "EQ",
    "NE",
    # Assignment (=)
    "EQUALS",
    # Parens ()
    "L_PAREN",
    "R_PAREN",
    # Braces {}
    "L_BRACE",
    "R_BRACE",
    "COMMA",
    "SEMICOLON",
)

# Operators
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"%"
t_LOR = r"\|\|"
t_LAND = r"&&"
t_LNOT = r"!"
t_LT = r"<"
t_GT = r">"
t_LE = r"<="
t_GE = r">="
t_EQ = r"=="
t_NE = r"!="

# Assignment operators

t_EQUALS = r"="

# Delimiters
t_L_PAREN = r"\("
t_R_PAREN = r"\)"
t_L_BRACE = r"\{"
t_R_BRACE = r"\}"
t_COMMA = r","
t_SEMICOLON = r";"

t_INT_LITERAL = r"-?\d+"
t_STRING_LITERAL = r"\"([^\\\n]|(\\.))*?\""

t_ignore = " \t"


def t_ID(t):
    r"[A-Za-z_][\w_]*"
    t.type = reserved_dict.get(t.value.lower(), "ID")
    return t


def t_comment(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
if __name__ == "__main__":
    lex.runmain(lexer)
