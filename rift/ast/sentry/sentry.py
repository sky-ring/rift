import ast

from rift.ast.sentry.base_types import (
    SentryState,
    SentryResult,
)
from rift.ast.sentry.watchers.base_watcher import Watcher
from rift.ast.sentry.watchers.simple_restrictor import SimpleRestrictor

watchers: list[Watcher] = [
    SimpleRestrictor("match", ast.Match, breaks=True),
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
