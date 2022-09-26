from rift.func.contract import Contract
from rift.types import Slice

from .util import compile


class Assigns(Contract):
    def external_receive(self) -> None:
        x = self.body
        x = self.body.addr_()
        y, z = self.body.bits_refs_n()
        y = self.body.sint(1)
        y, t = self.body.bits_refs_n()
        theta, beta = t, y


def test_compile():
    compile(Assigns)
