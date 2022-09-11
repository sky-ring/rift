"""
CST Transformer.

This dude patches the details that AST bypasses
"""
import libcst as cst

from rift.cst.int_visitor import HexTransformer


def patch(source):
    tree = cst.parse_module(source)
    transformers = [
        HexTransformer(),
    ]
    for t in transformers:
        tree = tree.visit(t)
    return tree.code
