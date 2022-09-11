"""
CST Visitor.

This dude helps us review the source code
"""
import libcst as cst

from rift.cst.import_visitor import RelativeImportVisitor


def relative_imports(source) -> RelativeImportVisitor:
    tree = cst.parse_module(source)
    visitor = RelativeImportVisitor()
    tree.visit(visitor)
    return visitor
