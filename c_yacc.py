import a_code as c
import c_lex
import ply.yacc as yacc

tokens = c_lex.tokens

precedence = (
    ("left", "EQUALS"),
    ("left", "LOR"),
    ("left", "LAND"),
    ("left", "EQ", "NE"),
    ("left", "LT", "LE", "GT", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MOD"),
    ("left", "LNOT"),
)


def p_program(t):
    """
    program : program function_definition
            | program variable_declaration
            | empty
    """
    if len(t) == 3:
        t[0] = c.Block(t[1].statements + [t[2]])
    else:
        t[0] = c.Block([])


def p_empty(t):
    """
    empty :
    """
    t[0] = ("empty",)


def p_id(t):
    """
    id : ID
    """
    t[0] = c.Id(t[1])


def p_fid(t):
    """
    fid : ID
    """
    t[0] = c.FId(t[1])


def p_function_definition(t):
    """
    function_definition : type fid L_PAREN parameter_list R_PAREN statement_block
    """
    sts = c.NSBlock(t[6].statements)
    t[0] = c.FunctionDefinition(t[2], t[1], t[4], sts)


def p_parameter_list(t):
    """
    parameter_list : empty
                   | parameter parameter_list_others
    """
    if len(t) == 3:
        t[0] = [t[1]] + t[2]
    else:
        t[0] = []


def p_parameter_list_others(t):
    """
    parameter_list_others : parameter_list_others COMMA parameter
                          | empty
    """
    if len(t) == 2:
        t[0] = []
    else:
        t[0] = t[1] + [t[3]]


def p_parameter(t):
    """
    parameter : type id
              | type
    """
    if len(t) == 3:
        t[0] = (t[1], t[2])
    else:
        t[0] = (t[1],)


def p_variable_declaration(t):
    """
    variable_declaration : type declaring_variables SEMICOLON
    """
    ret = []
    for tup in t[2]:
        if len(tup) == 2:
            ret.append(c.VariableDeclaration(tup[0], t[1]))
            ret.append(c.Assignment(tup[0], tup[1]))
        else:
            ret.append(c.VariableDeclaration(tup[0], t[1]))

    t[0] = c.NSBlock(ret)


def p_declaring_variables(t):
    """
    declaring_variables : declaring_variable
                        | declaring_variables COMMA declaring_variable
    """
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]


def p_declaring_variable(t):
    """
    declaring_variable : id
                       | id EQUALS expression
    """
    if len(t) == 2:
        t[0] = (t[1],)
    else:
        t[0] = (t[1], t[3])


def p_s_conditional(t):
    """
    s_conditional : s_if
                  | s_if_else
    """
    t[0] = t[1]


def p_s_if(t):
    """
    s_if : IF L_PAREN expression R_PAREN statement
    """
    t[0] = c.If(t[3], t[5])


def p_s_if_else(t):
    """
    s_if_else : IF L_PAREN expression R_PAREN statement ELSE statement
    """
    t[0] = c.IfElse(t[3], t[5], t[7])


def p_type_1(t):
    """
    type : INT
    """
    t[0] = c.Type.INT


def p_type_2(t):
    """
    type : BOOL
    """
    t[0] = c.Type.BOOL


def p_expression(t):
    """
    expression : L_PAREN expression R_PAREN
               | id
               | bool_literal
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
    t[0] = c.Block(t[2])


def p_statements(t):
    """
    statements : statements statement
               | empty
    """
    if len(t) == 2:
        t[0] = []
    else:
        t[0] = t[1] + [t[2]]


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
    t[0] = c.While(t[3], t[5])


def p_bool_literal_1(t):
    """
    bool_literal : TRUE
    """
    t[0] = c.BoolLiteral(True)


def p_bool_literal_2(t):
    """
    bool_literal : FALSE
    """
    t[0] = c.BoolLiteral(False)


def p_int_literal(t):
    """
    int_literal : INT_LITERAL
    """
    t[0] = c.IntLiteral(int(t[1]))


def p_e_assign(t):
    """
    e_assign : id EQUALS expression
    """
    t[0] = c.Assignment(t[1], t[3])


def p_e_plus(t):
    """
    e_plus : expression PLUS expression
    """
    t[0] = c.Plus(t[1], t[3])


def p_e_minus(t):
    """
    e_minus : expression MINUS expression
    """
    t[0] = c.Minus(t[1], t[3])


def p_e_times(t):
    """
    e_times : expression TIMES expression
    """
    t[0] = c.Times(t[1], t[3])


def p_e_divide(t):
    """
    e_divide : expression DIVIDE expression
    """
    t[0] = c.Divide(t[1], t[3])


def p_e_mod(t):
    "e_mod : expression MOD expression"
    t[0] = c.Mod(t[1], t[3])


def p_e_lor(t):
    "e_lor : expression LOR expression"
    t[0] = c.LOr(t[1], t[3])


def p_e_land(t):
    "e_land : expression LAND expression"
    t[0] = c.LAnd(t[1], t[3])


def p_e_lnot(t):
    """
    e_lnot : LNOT expression
    """
    t[0] = c.LNot(t[2])


def p_e_lt(t):
    """
    e_lt : expression LT expression
    """
    t[0] = c.LT(t[1], t[3])


def p_e_gt(t):
    """
    e_gt : expression GT expression
    """
    t[0] = c.GT(t[1], t[3])


def p_e_le(t):
    """
    e_le : expression LE expression
    """
    t[0] = c.LE(t[1], t[3])


def p_e_ge(t):
    """
    e_ge : expression GE expression
    """
    t[0] = c.GE(t[1], t[3])


def p_e_eq(t):
    """
    e_eq : expression EQ expression
    """
    t[0] = c.EQ(t[1], t[3])


def p_e_ne(t):
    """
    e_ne : expression NE expression
    """
    t[0] = c.NE(t[1], t[3])


def p_string_literal(t):
    """
    string_literal : STRING_LITERAL
    """
    s = t[1][1:-1]
    t[0] = s


def p_s_puts(t):
    """
    s_puts : PUTS L_PAREN string_literal R_PAREN SEMICOLON
    """
    t[0] = c.Puts(t[3])


def p_s_putw(t):
    """
    s_putw : PUTW L_PAREN expression R_PAREN SEMICOLON
    """
    t[0] = c.Putw(t[3])


parser = yacc.yacc(debug=True)
if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    r = parser.parse(text, tracking=True)
    print(r)
