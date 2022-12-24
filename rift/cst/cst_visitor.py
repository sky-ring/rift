"""
CST Visitor.

This dude helps us review the source code
"""
import libcst as cst

from rift.cst.import_visitor import (
    GeneralImportVisitor,
    RelativeImportVisitor,
)


def relative_imports(source) -> RelativeImportVisitor:
    tree = cst.parse_module(source)
    visitor = RelativeImportVisitor()
    tree.visit(visitor)
    return visitor


def target_imports(source: str, target: str) -> GeneralImportVisitor:
    tree = cst.parse_module(source)
    visitor = GeneralImportVisitor(target)
    tree.visit(visitor)
    return visitor
