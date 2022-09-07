import ast
from copy import deepcopy
from typing import Any


class ReturnPatcher(ast.NodeTransformer):
    """Transforms the AST to handle returns."""

    def visit_Return(self, node: ast.Return) -> Any:
        v = node.value
        if v is None:
            v = ast.Constant(None)
        u_node = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="helpers", ctx=ast.Load()),
                    attr="ret_",
                    ctx=ast.Load(),
                ),
                args=[v],
                keywords=[],
            ),
        )
        ast.fix_missing_locations(u_node)
        return u_node
