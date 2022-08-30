import ast
from copy import deepcopy
from typing import Any


class RaisePatcher(ast.NodeTransformer):
    """Transforms the AST to handle raise exprs."""

    def visit_Raise(self, node: ast.Raise) -> Any:
        return super().visit_Raise(node)
