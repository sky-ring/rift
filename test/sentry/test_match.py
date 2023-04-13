from rift import *
from rift.ast.sentry.base_types import SentryHalted

from test.util import compile


class DisallowMatch(Contract):
    def external_receive(self) -> None:
        match self.data:
            case True:
                pass


def test_compile():
    try:
        compile(DisallowMatch)
        raise RuntimeError("Shouldn't have c")
    except SentryHalted:
        pass
