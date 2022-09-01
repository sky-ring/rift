import ast
from typing import Any


class UnaryPatcher(ast.NodeTransformer):
    """Transforms the AST to handle unary neg as const."""

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        if isinstance(node.op, ast.USub) and isinstance(
            node.operand,
            ast.Constant,
        ):
            node.operand.value *= -1
            ast.fix_missing_locations(node.operand)
            return node.operand
        return node
