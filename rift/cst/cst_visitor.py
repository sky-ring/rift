"""
CST Visitor.

This dude helps us review the source code
"""
import libcst as cst

from rift.cst.cst_env import cst_use_native
from rift.cst.import_visitor import (
    GeneralImportVisitor,
    RelativeImportVisitor,
    ModuleImportVisitor,
)


def relative_imports(source) -> RelativeImportVisitor:
    cst_use_native()
    tree = cst.parse_module(source)
    visitor = RelativeImportVisitor()
    tree.visit(visitor)
    return visitor


def target_imports(source: str, target: str | None) -> GeneralImportVisitor:
    cst_use_native()
    tree = cst.parse_module(source)
    wrapper = cst.metadata.MetadataWrapper(tree)
    visitor = GeneralImportVisitor(target)
    wrapper.visit(visitor)
    return visitor


def module_imports(source: str) -> ModuleImportVisitor:
    cst_use_native()
    tree = cst.parse_module(source)
    wrapper = cst.metadata.MetadataWrapper(tree)
    visitor = ModuleImportVisitor()
    wrapper.visit(visitor)
    return visitor
