from rift.func.contract import Contract
from rift.types import Cell, Slice

from .util import compile


class Contract1(Contract):
    def internal_receive(self) -> None:
        b = self.body.uint(10)
        c = self.body.coin()


def test_compile():
    compile(Contract1)
