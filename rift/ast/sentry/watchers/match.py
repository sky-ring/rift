from ast import AST, Match

from rift.ast.sentry.base_types import SentryEntry, SentryState
from rift.ast.sentry.watchers.base_watcher import Watcher
from rift.ast.sentry.watchers.codes import ErrorCode


class MatchWatcher(Watcher):
    def watch(self, node: AST):
        return [
            SentryEntry(
                SentryState.HALT,
                None,
                (node.lineno, node.col_offset),
                ErrorCode.UnSupportedFlow,
                "match is not supported!",
            ),
        ], False

    def supports(self):
        return [
            Match,
        ]
