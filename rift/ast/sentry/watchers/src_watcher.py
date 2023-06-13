from abc import ABC, abstractmethod

from rift.ast.sentry.base_types import SentryResult


class SrcWatcher(ABC):
    @abstractmethod
    def watch(self, src: str) -> tuple[SentryResult, bool]:
        pass
