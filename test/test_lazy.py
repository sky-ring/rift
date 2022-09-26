from rift.func.contract import Contract
from rift.types import Cell, Slice
from rift.types.msg import InternalMessage

from .util import compile


class LazyPayloads(Contract):
    """LazyPayloads Contract."""

    def internal_receive(self) -> None:
        sender = self.message.info.src
        fwd_fee = self.message.info.fwd_fee


def test_compile():
    compile(LazyPayloads)
