from dbuilder.func.contract import Contract
from dbuilder.types import Cell, Slice
from dbuilder.types.msg import InternalMessage

from .util import compile


class LazyPayloads(Contract):
    """LazyPayloads Contract."""

    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        msg = InternalMessage(in_msg_full.parse())
        sender = msg.info.src
        fwd_fee = msg.info.fwd_fee


def test_compile():
    compile(LazyPayloads)
