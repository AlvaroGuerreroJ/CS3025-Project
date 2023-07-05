import graphviz

label_n = 1


def gen_label():
    global label_n
    label = f":G{label_n}"
    label_n += 1
    return label


class DotHelper:
    __slots__ = ("n", "dot")

    def __init__(self, dot):
        self.dot = dot
        self.n = 0

    def give_id(self):
        r = self.n
        self.n += 1
        return r

    def create_node(self, name):
        id_ = self.give_id()
        self.dot.node(str(id_), name)
        return id_

    def create_edge(self, id1, id2, comment=None):
        self.dot.edge(str(id1), str(id2), comment)


def draw(node):
    dot = graphviz.Digraph(comment="AST")
    dih = DotHelper(dot)

    node.draw(dih)

    return dot


class Node:
    def draw():
        pass


class NSBlock(Node):
    __slots__ = "statements"

    def __init__(self, statements):
        self.statements = statements

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("ns_block")

        for s in self.statements:
            on = s.draw(dih)
            dih.create_edge(id_, on)

        return id_


class Block(Node):
    __slots__ = "statements"

    def __init__(self, statements):
        self.statements = statements

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("block")

        for s in self.statements:
            on = s.draw(dih)
            dih.create_edge(id_, on)

        return id_


class Id(Node):
    __slots__ = "var_name"

    def __init__(self, var_name):
        self.var_name = var_name

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("ID")
        var_id = dih.create_node(self.var_name)
        dih.create_edge(id_, var_id)

        return id_


class FId(Node):
    __slots__ = "var_name"

    def __init__(self, var_name):
        self.var_name = var_name

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("FID")
        var_id = dih.create_node(self.var_name)
        dih.create_edge(id_, var_id)

        return id_


class FunctionDefinition(Node):
    __slots__ = ("fname", "return_type", "parameters", "body")

    def __init__(self, fname, return_type, parameters, body):
        self.fname: FId = fname
        self.return_type: str = return_type
        self.parameters = parameters
        self.body = body

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("FunctionDefinition")
        fname_id = self.fname.draw(dih)
        dih.create_edge(id_, fname_id, "fname")

        return_type_id = dih.create_node(self.return_type)
        dih.create_edge(id_, return_type_id, "return_type")

        parameters_id = dih.create_node(f"{str(self.parameters)}")
        dih.create_edge(id_, parameters_id, "parameters")

        body_id = self.body.draw(dih)
        dih.create_edge(id_, body_id, "body")

        return id_


class VariableDeclaration(Node):
    __slots__ = ("var_name", "v_type")

    def __init__(self, var_name, v_type):
        self.var_name = var_name
        self.v_type = v_type

    def draw(self, dih: DotHelper):
        id_ = dih.create_node(f"VariableDeclaration")

        var_name_id = self.var_name.draw(dih)
        dih.create_edge(id_, var_name_id)

        type_id = dih.create_node(self.v_type)
        dih.create_edge(id_, type_id, "type")

        return id_


class If(Node):
    __slots__ = ("condition", "then_statement")

    def __init__(self, condition, then_statement):
        self.condition = condition
        self.then_statement = then_statement

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("If")

        condition_id = self.condition.draw(dih)
        dih.create_edge(id_, condition_id, "condition")

        then_id = self.then_statement.draw(dih)
        dih.create_edge(id_, then_id, "then")

        return id_


class IfElse(Node):
    __slots__ = ("condition", "then_statement", "else_statement")

    def __init__(self, condition, then_statement, else_statement):
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("If")

        condition_id = self.condition.draw(dih)
        dih.create_edge(id_, condition_id, "condition")

        then_id = self.then_statement.draw(dih)
        dih.create_edge(id_, then_id, "then")

        else_id = self.else_statement.draw(dih)
        dih.create_edge(id_, else_id, "else")

        return id_


class While(Node):
    __slots__ = ("condition", "body")

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("While")

        condition_id = self.condition.draw(dih)
        dih.create_edge(id_, condition_id, "condition")

        body_id = self.body.draw(dih)
        dih.create_edge(id_, body_id, "body")

        return id_


class For(Node):
    __slots__ = ("initialization", "condition", "update", "body")

    def __init__(self, initialization, condition, update, body):
        self.initialization = initialization
        self.conditon = condition
        self.update = update
        self.body = body

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("For")

        init_id = self.initialization.draw(dih)
        dih.create_edge(id_, init_id, "initialization")

        condition_id = self.condition.draw(dih)
        dih.create_edge(id_, condition_id, "condition")

        update_id = self.update.draw(dih)
        dih.create_edge(id_, update_id, "update")

        body_id = self.body.draw(dih)
        dih.create_edge(id_, body_id, "body")

        return id_


class IntLiteral(Node):
    __slots__ = "value"

    def __init__(self, value):
        self.value = value

    def draw(self, dih: DotHelper):
        id_ = dih.create_node(str(self.value))

        return id_


class Assignment(Node):
    __slots__ = ("id_", "exp")

    def __init__(self, id_, exp):
        self.id_ = id_
        self.exp = exp

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("Assignment")

        var_id = self.id_.draw(dih)
        dih.create_edge(id_, var_id, "id")

        exp_id = self.exp.draw(dih)
        dih.create_edge(id_, exp_id, "exp")

        return id_


class BinaryExp(Node):
    __slots__ = ("exp1", "exp2")

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def draw(self, dih: DotHelper):
        id_ = dih.create_node(self.c_op_name)

        exp1_id = self.exp1.draw(dih)
        dih.create_edge(id_, exp1_id)

        exp2_id = self.exp2.draw(dih)
        dih.create_edge(id_, exp2_id)

        return id_


class Plus(BinaryExp):
    c_op_name = "Plus"


class Minus(BinaryExp):
    c_op_name = "Minus"


class Times(BinaryExp):
    c_op_name = "Times"


class Divide(BinaryExp):
    c_op_name = "Divide"


class Mod(BinaryExp):
    c_op_name = "Mod"


class LOr(BinaryExp):
    c_op_name = "LOr"


class LAnd(BinaryExp):
    c_op_name = "LAnd"


class LNot(BinaryExp):
    c_op_name = "LNot"


class LT(BinaryExp):
    c_op_name = "LT"


class GT(BinaryExp):
    c_op_name = "GT"


class LE(BinaryExp):
    c_op_name = "LE"


class GE(BinaryExp):
    c_op_name = "GE"


class EQ(BinaryExp):
    c_op_name = "EQ"


class NE(BinaryExp):
    c_op_name = "NE"


class Puts(Node):
    __slots__ = "string"

    def __init__(self, string):
        self.string = string

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("Puts")

        string_id = dih.create_node(self.string)
        dih.create_edge(id_, string_id)

        return id_


class Putw(Node):
    __slots__ = "exp"

    def __init__(self, exp):
        self.exp = exp

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("Putw")

        exp_id = self.exp.draw(dih)
        dih.create_edge(id_, exp_id)

        return id_
