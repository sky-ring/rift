import ast
from typing import Any


class IfPatcher(ast.NodeTransformer):
    _counter = 0
    """Transforms the AST to handle conditions."""

    def visit_If(self, node: ast.If) -> Any:
        # WHY?: This causes visitor to visit all children too,
        # otherwise we had to visit manually
        self.generic_visit(node)

        if_data = []
        current = node
        if_data.append((current.test, current.body))
        el_ = current.orelse
        if len(el_) != 0:
            if_data.append((None, el_))

        head = IfPatcher._counter
        IfPatcher._counter += 1

        with_item = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="helpers", ctx=ast.Load()),
                    attr="_cond",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
            optional_vars=ast.Name(id=f"c{head}", ctx=ast.Store()),
        )
        with_body = []
        for if_test, if_body in if_data:
            if if_test:
                expr = ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id=f"c{head}", ctx=ast.Load()),
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
                            value=ast.Name(id=f"c{head}", ctx=ast.Load()),
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
