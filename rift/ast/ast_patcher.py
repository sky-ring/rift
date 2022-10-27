"""
AST Transformer.

Patches the contract AST to capture the assignments, wrap the returns
Wouldn't be possible without:
https://gist.github.com/RyanKung/4830d6c8474e6bcefa4edd13f122b4df
"""

import ast

from rift.ast.patchers import (
    AssertPatcher,
    AssignPatcher,
    BreakPatcher,
    IfPatcher,
    RaisePatcher,
    ReturnPatcher,
    UnaryPatcher,
    WhilePatcher,
)


def patch(node):
    transformers = [
        UnaryPatcher(),
        AssertPatcher(),
        AssignPatcher(),
        BreakPatcher(),
        IfPatcher(),
        RaisePatcher(),
        ReturnPatcher(),
        WhilePatcher(),
    ]
    for t in transformers:
        new_node = t.visit(node)
        ast.fix_missing_locations(new_node)
    return new_node
