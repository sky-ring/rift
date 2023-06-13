from enum import Enum
from functools import total_ordering
from typing import NamedTuple

from rift.ast.sentry.watchers.codes import ErrorCode


class SentryHalted(Exception):
    def __init__(self, result: "SentryResult" = None):
        if result is None:
            result = []
        self.warnings = result


@total_ordering
class SentryState(Enum):
    HALT = 0
    WARN = 1
    OK = 2

    def is_ok(self):
        return self == SentryState.OK

    def should_halt(self):
        return self == SentryState.HALT

    def __lt__(self, other):
        if isinstance(other, SentryState):
            return self.value < other.value
        return NotImplemented


class SentryEntry(NamedTuple):
    flag: SentryState
    file: str | None
    loc: tuple[int, int]
    code: int | ErrorCode
    msg: str

    def log(self, ret=True):
        r = f"{self.flag.name} | {self.file} {self.loc[0] + 1}:{self.loc[1] + 1} | {self.msg}"
        if ret:
            return r
        print(r)

    def inject_file(self, file):
        return SentryEntry(self.flag, file, self.loc, self.code, self.msg)


SentryResult = list[SentryEntry]
