import ast
from copy import deepcopy
from typing import Any


class WhilePatcher(ast.NodeTransformer):
    """Transforms the AST to handle while loops."""

    def visit_While(self, node: ast.While) -> Any:
        return super().visit_While(node)
