"""
AST Transformer.

Patches the contract AST to capture the assignments, wrap the returns
Wouldn't be possible without:
https://gist.github.com/RyanKung/4830d6c8474e6bcefa4edd13f122b4df
"""

import ast
from typing import Any


class Transformer(ast.NodeTransformer):
    """Transforms the AST to capture assginments."""

    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Return(self, node: ast.Return) -> Any:
        v = node.value
        if v is None:
            v = ast.Constant(None)
        u_node = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="self", ctx=ast.Load()),
                    attr="ret_",
                    ctx=ast.Load(),
                ),
                args=[v],
                keywords=[],
            ),
        )
        ast.fix_missing_locations(u_node)
        return u_node
        pass

    def visit_Assign(self, node):
        tg = node.targets[0]
        if isinstance(tg, ast.Tuple):
            node.targets = [
                ast.Name(
                    id="__tmp__",
                    ctx=ast.Store(),
                ),
            ]
            vars = [v.id for v in tg.dims]
            e_expr = ast.Assign(
                targets=[
                    ast.Tuple(
                        elts=[
                            ast.Name(
                                id=v,
                                ctx=ast.Store(),
                            )
                            for v in vars
                        ],
                        ctx=ast.Store(),
                    ),
                ],
                value=ast.Name(
                    id="__tmp__",
                    ctx=ast.Load(),
                ),
            )
            p_expr = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="__tmp__", ctx=ast.Load()),
                        attr="__prep_unpack__",
                        ctx=ast.Load(),
                    ),
                    args=[ast.Constant(value=len(vars), kind=None)],
                    keywords=[],
                ),
            )
            a_expr = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="__tmp__", ctx=ast.Load()),
                        attr="__massign__",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.List(
                            elts=[
                                ast.Constant(value=str(v), kind=None)
                                for v in vars
                            ],
                            ctx=ast.Load(),
                        ),
                        ast.List(
                            elts=[
                                ast.Name(id=str(v), ctx=ast.Load())
                                for v in vars
                            ],
                            ctx=ast.Load(),
                        ),
                    ],
                    keywords=[],
                ),
            )
            nodes = [node, p_expr, e_expr, a_expr]
        else:
            target = node.targets[0].id
            nodes = [node]
            a_expr = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id=target, ctx=ast.Load()),
                        attr="__assign__",
                        ctx=ast.Load(),
                    ),
                    args=[ast.Constant(value=str(target), kind=None)],
                    keywords=[],
                ),
            )
            nodes.append(a_expr)
        for g_node in nodes:
            ast.fix_missing_locations(g_node)
        return nodes


def patch(node):
    trans = Transformer()
    new_node = trans.visit(node)
    ast.fix_missing_locations(new_node)
    return new_node
