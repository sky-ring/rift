from enum import Enum
from typing import NamedTuple


class SentryHalted(Exception):
    pass


class SentryState(Enum):
    OK = 0
    WARN = 1
    HALT = 2

    def is_ok(self):
        return self == SentryState.OK

    def should_halt(self):
        return self == SentryState.HALT


class SentryEntry(NamedTuple):
    flag: SentryState
    file: str
    loc: tuple[int, int]
    code: int
    msg: str

    def log(self):
        r = f"{self.flag.name} | {self.file} {self.loc[0]}:{self.loc[1]} | {self.msg}"
        print(r)


SentryResult = list[SentryEntry]


def sentry_analyze(ast, lazy=False) -> tuple[SentryState, SentryResult]:
    return SentryState.OK, []
