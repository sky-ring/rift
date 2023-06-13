from ast import AST
from typing import Callable

from rift.ast.sentry.base_types import SentryEntry, SentryState
from rift.ast.sentry.watchers.base_watcher import Watcher
from rift.ast.sentry.watchers.codes import ErrorCode


class SimpleRestrictor(Watcher):
    def __init__(
        self,
        name,
        *args: type | Callable[[AST], bool],
        breaks=False,
        code=ErrorCode.RestrictUnknown,
    ):
        self.name = name
        self.breaks = breaks
        self.supports_ = list(args)
        self.code = code

    def watch(self, node: AST):
        is_plural = len(self.supports_) > 1
        verb = "are" if is_plural else "is"
        return [
            SentryEntry(
                SentryState.HALT,
                None,
                (node.lineno, node.col_offset),
                self.code,
                f"{self.name} {verb} not supported!",
            ),
        ], not self.breaks

    def supports(self):
        return self.supports_
