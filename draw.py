import sys

import a_code
from c_yacc import parser


def main():
    text = sys.stdin.read()
    r = parser.parse(text, tracking=True)

    dot = a_code.draw(r)
    dot.render(directory="pngs/", view=True)

    r.type_check(a_code.Definitions())

    cg = a_code.CodeGen()
    r.gen_code(cg)
    print(cg.out.getvalue())


if __name__ == "__main__":
    main()
