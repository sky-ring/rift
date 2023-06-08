from test.util import compile

from rift import *
from rift.ast.sentry.base_types import SentryHalted


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
