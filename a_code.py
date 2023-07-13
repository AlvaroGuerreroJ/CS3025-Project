import graphviz
from collections import defaultdict
import io
import enum


class TypeCheckingError(Exception):
    pass


class Type(enum.StrEnum):
    INT = "int"
    BOOL = "bool"


class FunctionType:
    __slots__ = ("return_", "parameters")

    def __init__(self, return_type, parameters_types):
        self.return_ = return_type
        self.parameters = parameters_types

    def __repr__(self):
        return f'<FunctionType {self.return_}({", ".join(self.parameters)})>'


class Definitions:
    __slots__ = ("scopes",)

    def __init__(self):
        self.scopes = []

    def has(self, id_):
        for i, (sname, s) in enumerate(reversed(self.scopes), start=1):
            if id_ in s:
                return -i

        return False

    def get(self, id_):
        i = self.has(id_)

        if i is False:
            raise IndexError("No such variable")

        return self.scopes[i][1][id_]

    def real_name(self, id_):
        i = self.has(id_)

        if i is False:
            raise IndexError("No such variable")

        rn = f"{self.scopes[i][0]}_{id_}"
        return rn

    def define(self, var_name, type_, index=-1):
        self.scopes[index][1][var_name] = type_

    def add_scope(self, sname: str):
        self.scopes.append((sname, dict()))

    def pop_scope(self):
        self.scopes.pop()


class CodeGen:
    __slots__ = ("out", "label_n", "temp_n")

    def __init__(self):
        self.out = io.StringIO()
        self.label_n = defaultdict(int)
        self.temp_n = 1

    def gen_label(self, prefix):
        label = f":{prefix}_{self.label_n[prefix]}"
        self.label_n[prefix] += 1
        return label

    def gen_temp(self):
        temp = f"t{self.temp_n}"
        self.temp_n += 1
        return temp

    def write(self, string):
        self.out.write(string + "\n")


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
    pass


class Expression(Node):
    __slots__ = ("type_",)

    def gen_code(self, codegen: CodeGen):
        self.rvalue(codegen)


class NSBlock(Node):
    __slots__ = ("statements",)

    def __init__(self, statements):
        self.statements = statements

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("ns_block")

        for s in self.statements:
            on = s.draw(dih)
            dih.create_edge(id_, on)

        return id_

    def gen_code(self, codegen: CodeGen):
        for st in self.statements:
            st.gen_code(codegen)

    def type_check(self, defs: Definitions):
        for s in self.statements:
            s.type_check(defs)


class Block(Node):
    __slots__ = ("statements",)

    def __init__(self, statements):
        self.statements = statements

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("block")

        for s in self.statements:
            on = s.draw(dih)
            dih.create_edge(id_, on)

        return id_

    def gen_code(self, codegen: CodeGen):
        for st in self.statements:
            st.gen_code(codegen)

    def type_check(self, defs: Definitions):
        defs.add_scope(f"block_{id(self)}")
        for s in self.statements:
            s.type_check(defs)
        defs.pop_scope()


class Id(Expression):
    __slots__ = ("var_name", "real_name")

    def __init__(self, var_name):
        self.var_name = var_name

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("ID")
        var_id = dih.create_node(self.var_name)
        dih.create_edge(id_, var_id)

        return id_

    def lvalue(self, codegen: CodeGen):
        return self.real_name

    def rvalue(self, codegen: CodeGen):
        return self.real_name

    def type_check(self, defs: Definitions):
        try:
            type_ = defs.get(self.var_name)
        except IndexError:
            raise TypeCheckingError(f"Variable '{self.var_name}' not in scope")

        self.real_name = defs.real_name(self.var_name)

        self.type_ = type_


class FId(Node):
    __slots__ = ("var_name", "real_name")

    def __init__(self, var_name):
        self.var_name = var_name

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("FID")
        var_id = dih.create_node(self.var_name)
        dih.create_edge(id_, var_id)

        return id_

    def lvalue(self, codegen: CodeGen):
        return self.real_name

    def rvalue(self, codegen: CodeGen):
        return self.real_name

    def type_check(self, defs: Definitions):
        try:
            type_ = defs.get(self.var_name)
        except IndexError:
            raise TypeCheckingError(f"Function '{self.var_name}' not in scope")

        self.real_name = defs.real_name(self.var_name)

        self.type_ = type_


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

        parameters_id = dih.create_node("parameters")
        dih.create_edge(id_, parameters_id, "parameters")

        for p in self.parameters:
            p_id = dih.create_node("parameter")
            dih.create_edge(parameters_id, p_id)

            p_type_id = dih.create_node(p[0])
            dih.create_edge(p_id, p_type_id, "type")

            if len(p) == 2:
                p_id_id = p[1].draw(dih)
                dih.create_edge(p_id, p_id_id, "var_name")

        body_id = self.body.draw(dih)
        dih.create_edge(id_, body_id, "body")

        return id_

    def gen_code(self, codegen: CodeGen):
        l_f = f":{self.fname.real_name}"

        l_f_end = f"{l_f}_end"
        codegen.write(f"goto {l_f_end}")

        codegen.write(l_f)

        for p_type, p_id in self.parameters:
            codegen.write(f"pop {p_id.real_name}")

        self.body.gen_code(codegen)
        codegen.write("return")
        codegen.write(l_f_end)

    def type_check(self, defs: Definitions):
        defs.add_scope(f"f_{self.fname.var_name}_{id(self)}")

        for (p_type, p_id) in self.parameters:
            p_name = p_id.var_name
            if defs.has(p_name) == -1:
                raise TypeCheckingError(f"Repeated parameter {p_name}.")

            defs.define(p_name, p_type)

        # TODO: Define types for functions, will be needed for function calls
        defs.define(
            self.fname.var_name,
            FunctionType(self.return_type, [p[0] for p in self.parameters]),
            -2,
        )
        self.fname.type_check(defs)
        self.body.type_check(defs)

        defs.pop_scope()


class VariableDeclaration(Node):
    __slots__ = ("var", "v_type")

    def __init__(self, var, v_type):
        self.var = var
        self.v_type = v_type

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("VariableDeclaration")

        var_id = self.var.draw(dih)
        dih.create_edge(id_, var_id)

        type_id = dih.create_node(self.v_type)
        dih.create_edge(id_, type_id, "type")

        return id_

    def gen_code(self, codegen: CodeGen):
        # NOTE: Variable declarations are only for typechecking, no code is produced
        pass

    def type_check(self, defs: Definitions):
        if defs.has(self.var.var_name) == -1:
            raise TypeCheckingError(
                f"Variable '{self.var.var_name}' already defined in scope"
            )

        defs.define(self.var.var_name, self.v_type)


class Return(Node):
    __slots__ = ("exp",)

    def __init__(self, exp):
        self.exp = exp

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("Return")

        exp_id = self.exp.draw(dih)
        dih.create_edge(id_, exp_id)

        return id_

    def gen_code(self, codegen: CodeGen):
        exp_rv = self.exp.rvalue(codegen)
        codegen.write(f"return {exp_rv}")

    def type_check(self, defs: Definitions):
        self.exp.type_check(defs)

        # TODO: Check that the value being returned is of the return type of the closest subroutine


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

    def gen_code(self, codegen: CodeGen):
        l_if = codegen.gen_label("if")
        l_if_skip = f"{l_if}_skip"

        test_rv = self.condition.rvalue(codegen)

        codegen.write(f"ifFalse {test_rv} goto {l_if_skip}")
        self.then_statement.gen_code(codegen)
        codegen.write(l_if_skip)

    def type_check(self, defs: Definitions):
        self.condition.type_check(defs)

        if self.condition.type_ != Type.BOOL:
            raise TypeCheckingError("Condition of If statement is not of Bool type")

        self.then_statement.type_check(defs)


class IfElse(Node):
    __slots__ = ("condition", "then_statement", "else_statement")

    def __init__(self, condition, then_statement, else_statement):
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("IfElse")

        condition_id = self.condition.draw(dih)
        dih.create_edge(id_, condition_id, "condition")

        then_id = self.then_statement.draw(dih)
        dih.create_edge(id_, then_id, "then")

        else_id = self.else_statement.draw(dih)
        dih.create_edge(id_, else_id, "else")

        return id_

    def gen_code(self, codegen: CodeGen):
        l_if = codegen.gen_label("if")
        l_if_else = f"{l_if}_else"
        l_if_end = f"{l_if}_end"

        test_rv = self.condition.rvalue(codegen)

        codegen.write(f"ifFalse {test_rv} goto {l_if_else}")
        self.then_statement.gen_code(codegen)
        codegen.write(f"goto {l_if_end}")

        codegen.write(l_if_else)
        self.else_statement.gen_code(codegen)

        codegen.write(l_if_end)

    def type_check(self, defs: Definitions):
        self.condition.type_check(defs)

        if self.condition.type_ != Type.BOOL:
            raise TypeCheckingError("Condition of IfElse statement is not of Bool type")

        self.then_statement.type_check(defs)
        self.else_statement.type_check(defs)


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

    def gen_code(self, codegen: CodeGen):
        l_while = codegen.gen_label("while")
        l_while_start = f"{l_while}_start"
        l_while_end = f"{l_while}_end"

        codegen.write(l_while_start)

        test_rv = self.condition.rvalue(codegen)
        codegen.write(f"ifFalse {test_rv} goto {l_while_end}")
        self.body.gen_code(codegen)
        codegen.write(f"goto {l_while_start}")

        codegen.write(l_while_end)

    def type_check(self, defs: Definitions):
        self.condition.type_check(defs)

        if self.condition.type_ != Type.BOOL:
            raise TypeCheckingError("Condition of While statement is not of Bool type")

        self.body.type_check(defs)


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


class BoolLiteral(Expression):
    __slots__ = ("value",)
    type_ = Type.BOOL

    def __init__(self, value):
        self.value = value

    def draw(self, dih: DotHelper):
        id_ = dih.create_node(str(self.value))

        return id_

    def rvalue(self, codegen: CodeGen):
        return self.value

    def type_check(self, defs: Definitions):
        # NOTE: Literals are trivially type correct
        pass


class IntLiteral(Expression):
    __slots__ = ("value",)
    type_ = Type.INT

    def __init__(self, value):
        self.value = value

    def draw(self, dih: DotHelper):
        id_ = dih.create_node(str(self.value))

        return id_

    def rvalue(self, codegen: CodeGen):
        return self.value

    def type_check(self, defs: Definitions):
        # NOTE: Literals are trivially type correct
        pass


class FunctionCall(Expression):
    __slots__ = ("fname", "arguments")

    def __init__(self, fname, arguments):
        self.fname = fname
        self.arguments = arguments

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("FunctionCall")

        fname_id = self.fname.draw(dih)
        dih.create_edge(id_, fname_id, "fname")

        arguments_id = dih.create_node("arguments")
        dih.create_edge(id_, arguments_id)

        for ae in self.arguments:
            ae_id = ae.draw(dih)
            dih.create_edge(arguments_id, ae_id)

        return id_

    def rvalue(self, codegen: CodeGen):
        aa = []
        for a in self.arguments:
            aa.append(a.rvalue(codegen))

        # Inserted in reverse order so that the first argument ends on the top of the
        # stack
        for t_a in reversed(aa):
            codegen.write(f"push {t_a}")

        tv = codegen.gen_temp()
        codegen.write(f"fcall :{self.fname.real_name}")
        codegen.write(f"pop {tv}")

        return tv

    def type_check(self, defs: Definitions):
        self.fname.type_check(defs)

        if len(self.fname.type_.parameters) != len(self.arguments):
            raise TypeCheckingError(
                f"Wrong number arguments for call to {self.fname.var_name}, "
                f"expected {len(self.fname.type_.parameters)} but given {len(self.arguments)}"
            )

        for argument in self.arguments:
            argument.type_check(defs)

        for i, (parameter_type, argument_type) in enumerate(
            zip(self.fname.type_.parameters, (a.type_ for a in self.arguments)),
            start=1,
        ):
            if parameter_type != argument_type:
                raise TypeCheckingError(
                    f"Argument {i} for call to {self.fname.var_name} "
                    f"should be of type {parameter_type} but {argument_type} was given."
                )

        self.type_ = self.fname.type_.return_


class Assignment(Expression):
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

    def rvalue(self, codegen: CodeGen):
        exp_rv = self.exp.rvalue(codegen)
        id_lv = self.id_.lvalue(codegen)
        codegen.write(f"{id_lv} = {exp_rv}")
        return self.id_

    def type_check(self, defs: Definitions):
        self.id_.type_check(defs)
        self.exp.type_check(defs)

        if self.id_.type_ != self.exp.type_:
            raise TypeCheckingError(
                f"Trying to assign expression of type {self.exp.type_} to variable {self.id_.type_} of type {self.id_.type_}"
            )

        self.type_ = self.id_.type_


class LNot:
    __slots__ = ("exp",)

    type_ = Type.BOOL

    def __init__(self, exp):
        self.exp = exp

    def rvalue(self, codegen: CodeGen):
        exp_rv = self.exp.rvalue(codegen)
        tv = codegen.gen_temp()
        codegen.write(f"{tv} = not {exp_rv}")

        return tv

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("Not")
        exp_id = self.exp.draw(dih)
        dih.create_edge(id_, exp_id)

        return id_

    def type_check(self, defs: Definitions):
        self.exp.type_check(defs)

        if self.exp.type_ != Type.BOOL:
            raise TypeCheckingError("Not (!) operator must be applied to a boolean")


class BinaryExp(Expression):
    __slots__ = ("exp1", "exp2", "exp1_type", "exp2_type")

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

    def rvalue(self, codegen: CodeGen):
        exp1_rv = self.exp1.rvalue(codegen)
        exp2_rv = self.exp2.rvalue(codegen)

        tv = codegen.gen_temp()

        codegen.write(f"{tv} = {exp1_rv} {self.op} {exp2_rv}")

        return tv

    def type_check(self, defs: Definitions):
        self.exp1.type_check(defs)
        if self.exp1.type_ != self.exp1_type:
            raise TypeCheckingError(
                f"{self.c_op_name} ({self.op}) operator first operand must be of type {self.exp1_type}"
            )

        self.exp2.type_check(defs)
        if self.exp2.type_ != self.exp2_type:
            raise TypeCheckingError(
                f"{self.c_op_name} ({self.op}) operator second operand must be of type {self.exp2_type}"
            )


class Plus(BinaryExp):
    c_op_name = "Plus"
    op = "+"

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.INT


class Minus(BinaryExp):
    c_op_name = "Minus"
    op = "-"

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.INT


class Times(BinaryExp):
    c_op_name = "Times"
    op = "*"

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.INT


class Divide(BinaryExp):
    c_op_name = "Divide"
    op = "/"

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.INT


class Mod(BinaryExp):
    c_op_name = "Mod"
    op = "mod"

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.INT


class LOr(BinaryExp):
    c_op_name = "LOr"
    op = "||"

    exp1_type = Type.BOOL
    exp2_type = Type.BOOL
    type_ = Type.BOOL


class LAnd(BinaryExp):
    c_op_name = "LAnd"
    op = "&&"

    exp1_type = Type.BOOL
    exp2_type = Type.BOOL
    type_ = Type.BOOL


class LT(BinaryExp):
    c_op_name = "LT"
    op = "<"

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.BOOL


class GT(BinaryExp):
    c_op_name = "GT"
    op = ">"

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.BOOL


class LE(BinaryExp):
    c_op_name = "LE"
    op = "<="

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.BOOL


class GE(BinaryExp):
    c_op_name = "GE"
    op = ">="

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.BOOL


class EQ(BinaryExp):
    c_op_name = "EQ"
    op = "=="

    type_ = Type.BOOL

    def type_check(self, defs: Definitions):
        self.exp1.type_check(defs)
        self.exp2.type_check(defs)

        if self.exp1.type_ != self.exp2.type_:
            raise TypeCheckingError(
                f"{self.c_op_name} ({self.op}) operators must be of the same type (given {self.exp1.type_} and {self.exp2.type_})"
            )


class NE(BinaryExp):
    c_op_name = "NE"
    op = "!="

    exp1_type = Type.INT
    exp2_type = Type.INT
    type_ = Type.BOOL

    def type_check(self, defs: Definitions):
        self.exp1.type_check(defs)
        self.exp2.type_check(defs)

        if self.exp1.type_ != self.exp2.type_:
            raise TypeCheckingError(
                f"{self.c_op_name} ({self.op}) operators must be of the same type (given {self.exp1.type_} and {self.exp2.type_})"
            )


class Puts(Node):
    __slots__ = ("string",)

    def __init__(self, string):
        self.string = string

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("Puts")

        string_id = dih.create_node(self.string)
        dih.create_edge(id_, string_id)

        return id_

    def gen_code(self, codegen: CodeGen):
        codegen.write(f"puts {repr(self.string)}")

    def type_check(self, defs: Definitions):
        pass


class Putw(Node):
    __slots__ = ("exp",)

    def __init__(self, exp):
        self.exp = exp

    def draw(self, dih: DotHelper):
        id_ = dih.create_node("Putw")

        exp_id = self.exp.draw(dih)
        dih.create_edge(id_, exp_id)

        return id_

    def gen_code(self, codegen: CodeGen):
        exp_rv = self.exp.rvalue(codegen)
        codegen.write(f"putw {exp_rv}")

    def type_check(self, defs: Definitions):
        self.exp.type_check(defs)

        if self.exp.type_ != Type.INT:
            raise TypeCheckingError(
                f"Argument to Putw should be of type {Type.INT} but was {self.exp.type_}."
            )
