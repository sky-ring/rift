import ast
from typing import Any


class BreakPatcher(ast.NodeTransformer):
    """Transforms the AST to handle raise exprs."""

    def visit_Break(self, node: ast.Break) -> Any:
        u_node = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="helpers", ctx=ast.Load()),
                    attr="_break",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
        )
        ast.fix_missing_locations(u_node)
        return u_node
