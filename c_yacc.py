import ply.yacc as yacc
import c_lex

tokens = c_lex.tokens


def p_conditional(t):
    """
    s_conditional : s_if
                  | s_if_else
    """
    pass


def p_s_if(t):
    """
    s_if : IF L_PAREN expression R_PAREN statement
    """
    pass


def p_s_if_else(t):
    """
    s_if_else : IF L_PAREN expression R_PAREN statement ELSE statement
    """
    pass


def p_program(t):
    t[0] = t[1]


def p_type(t):
    """
    type_specifier : VOID
                   | INT
    """
    pass


def p_variable_declaration(t):
    """
    variable_declaration : p_type declaring_variables SEMICOLON
    """
    pass


def p_declaring_variables(t):
    """
    declaring_variables : declaring_variable
                        | declaring_variables COMMA declaring_variable
    """


def p_declaring_variable(t):
    """
    declaring_variable : ID
                       | ID EQUALS expression
    """
    pass


def p_expression(t):
    """
    expression : int_literal
    """
    pass


def p_statement(t):
    """
    statement : int_literal
    """
    pass


def p_int_literal(t):
    """
    int_literal : INT_LITERAL
    """
    pass


def p_statement_assign(t, s):
    "statement : NAME EQUALS expression SEMICOLON"
    pass


def p_expression_plus(p):
    "expression : expression PLUS term"
    pass


def p_expression_plus(p):
    "expression : expression PLUS term"


def p_expression_minus(p):
    "expression : expression MINUS term"
    pass


def p_expression_term(p):
    "expression : term"


def p_term_times(p):
    "term : term TIMES factor"


def p_term_div(p):
    "term : term DIVIDE factor"
    pass


def p_term_factor(p):
    "term : factor"
    pass


def p_factor_num(p):
    "factor : NUMBER"
    pass


def p_factor_expr(p):
    "factor : LPAREN expression RPAREN"
    pass


def p_error(p):
    print("Syntax error in input!")


def p_puts(t):
    "puts : PUTS STRING_LITERAL SEMICOLON"
    pass


def p_putw(t):
    "putw : PUTW expression SEMICOLON"
    pass


parser = yacc.yacc()
if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    r = parser.parse(text)
    print(r)
