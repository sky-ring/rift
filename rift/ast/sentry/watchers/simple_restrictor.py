from typing import Callable

from rift.ast.sentry.watchers.base_watcher import Watcher
from rift.ast.sentry.watchers.codes import ErrorCode
from rift.ast.sentry.base_types import SentryEntry, SentryState
from ast import AST


class SimpleRestrictor(Watcher):
    def __init__(
        self, name, *args: type | Callable[[AST], bool], breaks=False
    ):
        self.name = name
        self.breaks = breaks
        self.supports_ = list(args)

    def watch(self, node: AST):
        return [
            SentryEntry(
                SentryState.HALT,
                None,
                (node.lineno, node.col_offset),
                ErrorCode.UnSupportedFlow,
                f"{self.name} is not supported!",
            ),
        ], not self.breaks

    def supports(self):
        return self.supports_
