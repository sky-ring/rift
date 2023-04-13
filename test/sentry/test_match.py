from rift import *

from test.util import compile


class DisallowMatch(Contract):
    def external_receive(self) -> None:
        match self.data:
            case True:
                pass


def test_compile():
    compile(DisallowMatch)
