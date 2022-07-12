"""
AST Transformer
Patches the contract AST to capture the assignments
Wouldn't be possible without: https://gist.github.com/RyanKung/4830d6c8474e6bcefa4edd13f122b4df
"""

import ast

origin_import = __import__
AST = {}


class Transformer(ast.NodeTransformer):
    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Assign(self, node):
        targets = [t.id for t in node.targets]
        nodes = [node]
        for t in targets:
            vx = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id=t, ctx=ast.Load()),
                        attr='__assign__',
                        ctx=ast.Load(),
                    ),
                    args=[ast.Constant(value=str(t), kind=None)],
                    keywords=[],
                ),
            )
            nodes.append(vx)
        for vx in nodes:
            ast.fix_missing_locations(vx)
        return nodes


def patch(node):
    trans = Transformer()
    new_node = trans.visit(node)
    ast.fix_missing_locations(new_node)
    return new_node
