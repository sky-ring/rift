import ast

from rift.ast.sentry.base_types import (
    SentryState,
    SentryResult,
)
from rift.ast.sentry.watchers.base_watcher import Watcher
from rift.ast.sentry.watchers.simple_restrictor import SimpleRestrictor

watchers: list[Watcher] = [
    SimpleRestrictor("match statement", ast.Match, breaks=False),
    SimpleRestrictor("delete statement", ast.Delete, breaks=False),
    SimpleRestrictor(
        "async ops",
        ast.AsyncFor,
        ast.AsyncWith,
        ast.Await,
        ast.AsyncFunctionDef,
        breaks=False,
    ),
    SimpleRestrictor(
        "with statements", ast.With, ast.AsyncWith, breaks=False
    ),
    SimpleRestrictor(
        "yield expressions", ast.Yield, ast.YieldFrom, breaks=False
    ),
    SimpleRestrictor("try statements", ast.Try, breaks=False),
    SimpleRestrictor("nonlocal statements", ast.Nonlocal, breaks=False),
    SimpleRestrictor("named expressions", ast.NamedExpr, breaks=False),
    SimpleRestrictor("lambda expressions", ast.Lambda, breaks=False),
    SimpleRestrictor("if expressions", ast.IfExp, breaks=False),
    SimpleRestrictor(
        "f-strings", ast.FormattedValue, ast.JoinedStr, breaks=False
    ),
    SimpleRestrictor("starred statements", ast.Starred, breaks=False),
    SimpleRestrictor("slicing statements", ast.Slice, breaks=False),
    SimpleRestrictor(
        "comprehensions",
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
        breaks=False,
    ),
]


def walker(node, file=None) -> SentryResult:
    cont_array = []
    results: SentryResult = []

    for watcher in watchers:
        if watcher.check(node):
            result, cont = watcher.watch(node)
            cont_array.append(int(cont))
            results += result

    if len(cont_array) == 0 or sum(cont_array) != 0:
        for child_node in ast.iter_child_nodes(node):
            results += walker(child_node)

    results = [r.inject_file(file) for r in results]
    return results


def sentry_analyze(tree, file=None) -> tuple[SentryState, SentryResult]:
    results = walker(tree, file=file)
    state = min(r.flag for r in results) if len(results) else SentryState.OK
    return state, results
