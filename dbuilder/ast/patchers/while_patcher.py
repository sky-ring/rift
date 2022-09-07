import ast
from typing import Any


class WhilePatcher(ast.NodeTransformer):
    """Transforms the AST to handle while loops."""

    def visit_While(self, node: ast.While) -> Any:
        self.generic_visit(node)

        with_item = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="helpers", ctx=ast.Load()),
                    attr="_while",
                    ctx=ast.Load(),
                ),
                args=[node.test],
                keywords=[],
            ),
        )
        with_ = ast.With(items=[with_item], body=node.body)
        ast.fix_missing_locations(with_)
        return with_
