import sys


def main():
    code = []
    for l in sys.stdin:
        code.append(l.strip("\n"))

    labels = dict()
    for i, cl in enumerate(code):
        if cl[0] == ":":
            labels[cl] = i

    states = [dict()]
    stack = []
    return_pointers = []
    next_instruction = 0

    def eval_operand(operand):
        if operand[0].isdigit():
            return int(operand)
        elif operand == "true":
            return True
        elif operand == "false":
            return False
        else:
            return states[-1][operand]

    def eval_exp(exp):
        op1 = eval_operand(exp[0])
        if len(exp) == 1:
            return op1
        op2 = eval_operand(exp[2])

        if exp[1] == "+":
            return op1 + op2
        elif exp[1] == "-":
            return op1 - op2
        elif exp[1] == "*":
            return op1 * op2
        elif exp[1] == "<":
            return op1 < op2
        elif exp[1] == ">":
            return op1 > op2
        elif exp[1] == "==":
            return op1 == op2
        else:
            raise RuntimeError("Not implemented")

    def eval_line(line):
        nonlocal next_instruction

        p = line.split()
        if p[0][0] == ":":
            pass
        elif p[0] == "goto":
            next_instruction = labels[p[1]]
            return
        elif p[0] == "puts":
            print(states[-1][p[1]])
        elif p[0] == "putw":
            print(states[-1][p[1]])
        elif p[0] == "ifFalse":
            if states[-1][p[1]] is False:
                next_instruction = labels[p[3]]
                return
        elif p[0] == "return":
            if len(p) == 1:
                next_instruction = return_pointers.pop()
                states.pop()
                return
            else:
                stack.append(eval_exp(p[1:]))
                next_instruction = return_pointers.pop()
                states.pop()
                return
        elif p[0] == "push":
            stack.append(eval_operand(p[1]))
        elif p[0] == "pop":
            states[-1][p[1]] = stack.pop()
        elif p[0] == "fcall":
            ns = states[-1].copy()
            states.append(ns)

            return_pointers.append(next_instruction + 1)

            next_instruction = labels[p[1]]
        elif p[1] == "=":
            states[-1][p[0]] = eval_exp(p[2:])
        else:
            raise RuntimeError("Not implemented")

        next_instruction += 1

    while next_instruction < len(code):
        line = code[next_instruction]
        print(f"Evaluating: {line}")
        eval_line(line)

    main_label = None
    for l in labels:
        if l.endswith("main"):
            main_label = l

    if main_label is None:
        print("Main not found")
        return

    next_instruction = labels[main_label]
    while next_instruction < len(code):
        # import pprint
        # pprint.pprint(states)
        # pprint.pprint(stack)
        line = code[next_instruction]
        print(f"Evaluating: {line}")
        eval_line(line)

    print("Done!")


if __name__ == "__main__":
    main()
