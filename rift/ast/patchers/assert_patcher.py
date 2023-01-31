import ast
from copy import deepcopy
from typing import Any


class AssertPatcher(ast.NodeTransformer):
    """Transforms the AST to handle assertions."""

    def visit_Assert(self, node: ast.Assert) -> Any:
        if node.msg is None:
            node.msg = ast.Constant(999)
        u_node = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="helpers", ctx=ast.Load()),
                    attr="throw_unless",
                    ctx=ast.Load(),
                ),
                args=[node.msg, node.test],
                keywords=[],
            ),
        )
        ast.fix_missing_locations(u_node)
        return u_node
