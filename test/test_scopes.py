from rift.func.contract import Contract
from rift.types import Slice

from .util import compile


class Scopes(Contract):
    def external_receive(self) -> None:
        x = self.body
        while x.uint_(2) == 0:
            if x.uint(1) == 1:
                b = 4
                b = 2
                x = x.addr_()
            else:
                b = 6
                b = 10
        b = 1
        b = 3


def test_compile():
    compile(Scopes)
