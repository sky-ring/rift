import ast
from typing import Any


class RaisePatcher(ast.NodeTransformer):
    """Transforms the AST to handle raise exprs."""

    def visit_Raise(self, node: ast.Raise) -> Any:
        u_node = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="helpers", ctx=ast.Load()),
                    attr="_throw",
                    ctx=ast.Load(),
                ),
                args=[node.exc],
                keywords=[],
            ),
        )
        ast.fix_missing_locations(u_node)
        return u_node
