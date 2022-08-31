from dbuilder.func.contract import Contract
from dbuilder.types import Slice

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


def test_compile():
    compile(Assigns)
