import ply.yacc as yacc
import c_lex

tokens = c_lex.tokens


def p_program(t):
    """
    program : program function_declaration
            | program variable_declaration
            | empty
    """
    t[0] = t[1]
    pass


def p_empty(t):
    "empty :"
    pass


def p_function_declaration(t):
    """
    function_declaration : type ID L_PAREN parameter_list R_PAREN statement_block
    """
    pass


def p_parameter_list(t):
    """
    parameter_list : parameter
                   | parameter_list COMMA parameter
                   | empty
    """
    pass


def p_parameter(t):
    """
    parameter : type ID
              | type
    """
    pass


def p_variable_declaration(t):
    """
    variable_declaration : type declaring_variables SEMICOLON
    """
    pass


def p_declaring_variables(t):
    """
    declaring_variables : declaring_variable
                        | declaring_variables COMMA declaring_variable
    """
    pass


def p_declaring_variable(t):
    """
    declaring_variable : ID
                       | ID EQUALS expression
    """
    pass


def p_s_conditional(t):
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


def p_type(t):
    """
    type : VOID
         | INT
    """
    pass


def p_expression(t):
    """
    expression : int_literal
               | L_PAREN expression R_PAREN
    """
    pass


def p_statement_block(t):
    """
    statement_block : L_BRACE statements R_BRACE
    """
    pass


def p_statements(t):
    """
    statements : statements statement
               | statement
    """
    pass


def p_statement(t):
    """
    statement : expression SEMICOLON
              | s_conditional
              | L_BRACE statement R_BRACE
              | statement_block
    """
    pass


def p_s_while(t):
    """
    s_while : WHILE L_PAREN expression R_PAREN statement
    """
    pass


def p_int_literal(t):
    """
    int_literal : INT_LITERAL
    """
    pass


def p_e_assign(t):
    """
    e_assign : ID EQUALS expression
    """
    pass


def p_e_plus(t):
    """
    e_plus : expression PLUS expression
    """
    pass


def p_e_minus(t):
    """
    e_minus : expression MINUS expression
    """
    pass


def p_e_times(t):
    """
    e_times : expression TIMES expression
    """
    pass


def p_e_divide(t):
    """
    e_divide : expression DIVIDE expression
    """
    pass


def p_e_mod(t):
    "e_mod : expression MOD expression"
    pass


def p_e_lor(t):
    "e_lor : expression LOR expression"
    pass


def p_e_land(t):
    "e_land : expression LAND expression"
    pass


def p_e_lnot(t):
    """
    e_lnot : LNOT expression
    """
    pass


def p_e_lt(t):
    """
    e_lnot : expression LT expression
    """
    pass


def p_e_gt(t):
    """
    e_gt : expression GT expression
    """
    pass


def p_e_le(t):
    """
    e_le : expression LE expression
    """
    pass


def p_e_ge(t):
    """
    e_ge : expression GE expression
    """
    pass


def p_e_eq(t):
    """
    e_eq : expression EQ expression
    """
    pass


def p_e_ne(t):
    """
    e_ne : expression NE expression
    """
    pass


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
