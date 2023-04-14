import ast

from rift.ast.sentry.base_types import (
    SentryState,
    SentryResult,
)
from rift.ast.sentry.watchers.base_watcher import Watcher
from rift.ast.sentry.watchers.codes import ErrorCode
from rift.ast.sentry.watchers.simple_restrictor import SimpleRestrictor

watchers: list[Watcher] = [
    SimpleRestrictor(
        "match statement", ast.Match, breaks=False, code=ErrorCode.NoMatch
    ),
    SimpleRestrictor(
        "delete statement", ast.Delete, breaks=False, code=ErrorCode.NoDelete
    ),
    SimpleRestrictor(
        "async ops",
        ast.AsyncFor,
        ast.AsyncWith,
        ast.Await,
        ast.AsyncFunctionDef,
        breaks=False,
        code=ErrorCode.NoAsync,
    ),
    SimpleRestrictor(
        "with statements", ast.With, breaks=False, code=ErrorCode.NoWith
    ),
    SimpleRestrictor(
        "yield expressions",
        ast.Yield,
        ast.YieldFrom,
        breaks=False,
        code=ErrorCode.NoYield,
    ),
    SimpleRestrictor(
        "try statements", ast.Try, breaks=False, code=ErrorCode.NoTry
    ),
    SimpleRestrictor(
        "nonlocal statements",
        ast.Nonlocal,
        breaks=False,
        code=ErrorCode.NoNonLocal,
    ),
    SimpleRestrictor(
        "named expressions",
        ast.NamedExpr,
        breaks=False,
        code=ErrorCode.NoNamedExpr,
    ),
    SimpleRestrictor(
        "lambda expressions",
        ast.Lambda,
        breaks=False,
        code=ErrorCode.NoLambda,
    ),
    SimpleRestrictor(
        "if expressions", ast.IfExp, breaks=False, code=ErrorCode.NoIfExpr
    ),
    SimpleRestrictor(
        "f-strings",
        ast.FormattedValue,
        ast.JoinedStr,
        breaks=True,
        code=ErrorCode.NoFStr,
    ),
    SimpleRestrictor(
        "starred statements",
        ast.Starred,
        breaks=False,
        code=ErrorCode.NoStarredStatement,
    ),
    SimpleRestrictor(
        "slicing statements",
        ast.Slice,
        breaks=False,
        code=ErrorCode.NoSlicing,
    ),
    SimpleRestrictor(
        "comprehensions",
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
        breaks=False,
        code=ErrorCode.NoComprehension,
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
