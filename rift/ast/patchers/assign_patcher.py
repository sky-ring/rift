import ast
from copy import deepcopy
from typing import Any


class AssignPatcher(ast.NodeTransformer):
    """Transforms the AST to capture assginments."""

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
            l_expr = ast.Call(
                func=ast.Name(id="hasattr", ctx=ast.Load()),
                args=[
                    ast.Name(id="__tmp__", ctx=ast.Load()),
                    ast.Constant(value="__prep_unpack__", kind=None),
                ],
                keywords=[],
            )
            r_expr = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="__tmp__", ctx=ast.Load()),
                    attr="__prep_unpack__",
                    ctx=ast.Load(),
                ),
                args=[ast.Constant(value=len(vars), kind=None)],
                keywords=[],
            )

            p_expr = ast.Expr(
                value=ast.BoolOp(op=ast.And(), values=[l_expr, r_expr]),
            )
            a_expr = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="helpers", ctx=ast.Load()),
                        attr="_m_assign",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Name(id="__tmp__", ctx=ast.Load()),
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
            target = node.targets[0]
            if hasattr(target, "id"):
                tg = target.id
                # Let's not patch some specific vars
                if tg.startswith("__") and tg.endswith("__"):
                    return node
            else:
                tg = None
            nodes = [node]
            if isinstance(node.value, ast.Constant):
                if isinstance(node.value.value, int) and type(
                    node.value.value,
                ) != type(False):
                    node.value = ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="helpers", ctx=ast.Load()),
                            attr="factory_",
                            ctx=ast.Load(),
                        ),
                        args=[ast.Constant("int"), node.value],
                        keywords=[],
                    )
            nt = deepcopy(target)
            nt.ctx = ast.Load()
            if isinstance(target, ast.Attribute):
                rem_expr = ast.Call(
                    func=ast.Attribute(
                        value=nt,
                        attr="__rem_name__",
                        ctx=ast.Load(),
                    ),
                    args=[],
                    keywords=[],
                )
                r_expr = ast.Assign(
                    targets=[ast.Name(id="__rem__", ctx=ast.Store())],
                    value=rem_expr,
                )
            elif isinstance(target, ast.Name):
                r_expr = ast.Assign(
                    targets=[ast.Name(id="__rem__", ctx=ast.Store())],
                    value=ast.Constant(value=target.id, kind=None),
                )
            nodes.insert(0, r_expr)
            c_expr = ast.Call(
                func=ast.Attribute(
                    value=nt,
                    attr="__assign__",
                    ctx=ast.Load(),
                ),
                args=[ast.Name(id="__rem__", ctx=ast.Load())],
                keywords=[],
            )
            if isinstance(node.value, ast.Name):
                a_expr = ast.Assign(
                    targets=[target],
                    value=c_expr,
                )
            else:
                a_expr = ast.Expr(
                    value=c_expr,
                )
            nodes.append(a_expr)
        for g_node in nodes:
            ast.fix_missing_locations(g_node)
        return nodes
