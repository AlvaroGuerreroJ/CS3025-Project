import graphviz
import sys

from c_yacc import parser


def main():
    text = sys.stdin.read()
    r = parser.parse(text, tracking=True)

    dot = graphviz.Digraph(comment="AST")
    cur_id = 1

    def draw_node(node):
        nonlocal cur_id

        node_id = cur_id
        cur_id += 1

        if type(node) == tuple:
            dot.node(str(node_id), graphviz.escape(node[0]))
            for n in node[1:]:
                n_id = draw_node(n)
                dot.edge(str(node_id), str(n_id))

            return node_id
        else:
            dot.node(str(node_id), graphviz.escape(str(node)))
            return node_id

    draw_node(r)

    dot.render(directory="pngs/", view=True)


if __name__ == "__main__":
    main()
