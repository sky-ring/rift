from rift.func.contract import Contract
from rift.types import Slice

from .util import compile


class Assigns(Contract):
    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        x = in_msg
        x = in_msg.addr_()
        y, z = in_msg.bits_refs_n()
        y = in_msg.sint(1)
        y, t = in_msg.bits_refs_n()
        theta, beta = t, y


def test_compile():
    compile(Assigns)
