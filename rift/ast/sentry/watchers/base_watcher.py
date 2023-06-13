from abc import ABC, abstractmethod
from ast import AST
from typing import Callable

from rift.ast.sentry.base_types import SentryResult


class Watcher(ABC):
    @abstractmethod
    def watch(self, node) -> tuple[SentryResult, bool]:
        pass

    @abstractmethod
    def supports(self) -> list[type | Callable[[AST], bool]]:
        pass

    def check(self, node: AST) -> bool:
        supports = self.supports()
        if type(node) in supports:
            return True

        for c in filter(lambda x: not isinstance(x, type), supports):
            if c(node):
                return True

        return False
