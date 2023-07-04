import ply.yacc as yacc
import c_lex

tokens = c_lex.tokens

precedence = (
    ("left", "LT", "LE", "GT", "GE", "EQ", "NE"),  # Nonassociative operators
    (
        "left",
        "LOR",
        "LAND",
        "LNOT",
    ),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MOD"),
)


def p_program(t):
    """
    program : program function_definition
            | program variable_declaration
            | empty
    """
    if len(t) == 3:
        t[0] = ("program",) + t[1][1:] + (t[2],)
    else:
        t[0] = ("program",)


def p_empty(t):
    """
    empty :
    """
    t[0] = ("empty",)


def p_id(t):
    """
    id : ID
    """
    t[0] = ("identifier", t[1])


def p_function_definition(t):
    """
    function_definition : type id L_PAREN parameter_list R_PAREN statement_block
    """
    t[0] = ("function_definition", t[1], t[2], t[4], t[6])


def p_parameter_list(t):
    """
    parameter_list : empty
                   | parameter parameter_list_others
    """
    if len(t) == 3:
        t[0] = ("parameter_list", t[1]) + t[2][1:]
    else:
        t[0] = ("parameter_list",)


def p_parameter_list_others(t):
    """
    parameter_list_others : parameter_list_others COMMA parameter
                          | empty
    """
    if len(t) == 2:
        t[0] = ("parameter_list_others",)
    else:
        t[0] = ("parameter_list_others",) + t[1][1:] + (t[3],)


def p_parameter(t):
    """
    parameter : type id
              | type
    """
    if len(t) == 3:
        t[0] = ("parameter", t[1], t[2])
    else:
        t[0] = ("parameter", t[1])


def p_variable_declaration(t):
    """
    variable_declaration : type declaring_variables SEMICOLON
    """
    t[0] = ("variable_declaration", t[1], t[2])


def p_declaring_variables(t):
    """
    declaring_variables : declaring_variable
                        | declaring_variables COMMA declaring_variable
    """
    if len(t) == 2:
        t[0] = ("declaring_variables", t[1])
    else:
        t[0] = ("declaring_variables",) + t[1][1:] + (t[3],)


def p_declaring_variable(t):
    """
    declaring_variable : id
                       | id EQUALS expression
    """
    if len(t) == 2:
        t[0] = ("declaring_variable", t[1])
    else:
        t[0] = ("declaring_variable", t[1], t[3])


def p_s_conditional(t):
    """
    s_conditional : s_if
                  | s_if_else
    """
    t[0] = ("conditional", t[1])


def p_s_if(t):
    """
    s_if : IF L_PAREN expression R_PAREN statement
    """
    t[0] = ("if", t[3], t[5])


def p_s_if_else(t):
    """
    s_if_else : IF L_PAREN expression R_PAREN statement ELSE statement
    """
    t[0] = ("if_else", t[3], t[5], t[7])


def p_type(t):
    """
    type : VOID
         | INT
    """
    t[0] = ("type", t[1])


def p_expression(t):
    """
    expression : L_PAREN expression R_PAREN
               | id
               | int_literal
               | e_assign
               | e_plus
               | e_minus
               | e_times
               | e_divide
               | e_mod
               | e_lor
               | e_land
               | e_lnot
               | e_lt
               | e_gt
               | e_le
               | e_ge
               | e_eq
               | e_ne
    """
    if len(t) == 4:
        t[0] = t[2]
    else:
        t[0] = t[1]


def p_statement_block(t):
    """
    statement_block : L_BRACE statements R_BRACE
    """
    t[0] = t[2]


def p_statements(t):
    """
    statements : statements statement
               | empty
    """
    if len(t) == 2:
        t[0] = ("statements",)
    else:
        t[0] = ("statements",) + t[1][1:] + (t[2],)


def p_statement(t):
    """
    statement : expression SEMICOLON
              | s_conditional
              | s_while
              | s_puts
              | s_putw
              | statement_block
              | variable_declaration
    """
    t[0] = t[1]


def p_s_while(t):
    """
    s_while : WHILE L_PAREN expression R_PAREN statement
    """
    t[0] = ("while", t[3], t[5])


def p_int_literal(t):
    """
    int_literal : INT_LITERAL
    """
    t[0] = ("int_literal", int(t[1]))


def p_e_assign(t):
    """
    e_assign : id EQUALS expression
    """
    t[0] = ("assigns", t[1], t[3])


def p_e_plus(t):
    """
    e_plus : expression PLUS expression
    """
    t[0] = ("plus", t[1], t[3])


def p_e_minus(t):
    """
    e_minus : expression MINUS expression
    """
    t[0] = ("minus", t[1], t[3])


def p_e_times(t):
    """
    e_times : expression TIMES expression
    """
    t[0] = ("times", t[1], t[3])


def p_e_divide(t):
    """
    e_divide : expression DIVIDE expression
    """
    t[0] = ("divide", t[1], t[3])


def p_e_mod(t):
    "e_mod : expression MOD expression"
    t[0] = ("mod", t[1], t[3])


def p_e_lor(t):
    "e_lor : expression LOR expression"
    t[0] = ("lor", t[1], t[3])


def p_e_land(t):
    "e_land : expression LAND expression"
    t[0] = ("land", t[1], t[3])


def p_e_lnot(t):
    """
    e_lnot : LNOT expression
    """
    t[0] = ("lnot", t[1], t[3])


def p_e_lt(t):
    """
    e_lt : expression LT expression
    """
    t[0] = ("lt", t[1], t[3])


def p_e_gt(t):
    """
    e_gt : expression GT expression
    """
    t[0] = ("gt", t[1], t[3])


def p_e_le(t):
    """
    e_le : expression LE expression
    """
    t[0] = ("le", t[1], t[3])


def p_e_ge(t):
    """
    e_ge : expression GE expression
    """
    t[0] = ("ge", t[1], t[3])


def p_e_eq(t):
    """
    e_eq : expression EQ expression
    """
    t[0] = ("eq", t[1], t[3])


def p_e_ne(t):
    """
    e_ne : expression NE expression
    """
    t[0] = ("ne", t[1], t[3])


def p_string_literal(t):
    """
    string_literal : STRING_LITERAL
    """
    s = t[1][1:-1]
    t[0] = ("string_literal", s)


def p_s_puts(t):
    """
    s_puts : PUTS L_PAREN string_literal R_PAREN SEMICOLON
    """
    t[0] = ("puts", t[3])


def p_s_putw(t):
    """
    s_putw : PUTW L_PAREN expression R_PAREN SEMICOLON
    """
    t[0] = ("putw", t[3])


parser = yacc.yacc(debug=True)
if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    r = parser.parse(text, tracking=True)
    print(r)
