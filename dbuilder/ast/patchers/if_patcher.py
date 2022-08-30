import ast
from copy import deepcopy
from typing import Any


class IfPatcher(ast.NodeTransformer):
    """Transforms the AST to handle conditions."""

    def visit_If(self, node: ast.If) -> Any:
        # Let's Process the F***ing If
        # TODO: handle with names
        if_data = []
        current = node
        while current is not None:
            if_data.append((current.test, current.body))
            el_ = current.orelse
            if len(el_) == 0:
                current = None
                break
            top = el_[0]
            if isinstance(top, ast.If):
                current = top
            else:
                if_data.append((None, el_))
                current = None
        with_item = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="self", ctx=ast.Load()),
                    attr="_cond",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
            optional_vars=ast.Name(id="c", ctx=ast.Store()),
        )
        with_body = []
        for if_test, if_body in if_data:
            if if_test:
                expr = ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="c", ctx=ast.Load()),
                            attr="match",
                            ctx=ast.Load(),
                        ),
                        args=[if_test],
                        keywords=[],
                    ),
                )
            else:
                expr = ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="c", ctx=ast.Load()),
                            attr="otherwise",
                            ctx=ast.Load(),
                        ),
                        args=[],
                        keywords=[],
                    ),
                )
            with_body.append(expr)
            with_body.extend(if_body)
        with_ = ast.With(items=[with_item], body=with_body)
        ast.fix_missing_locations(with_)
        return with_
