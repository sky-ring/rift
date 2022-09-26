from rift.func.contract import Contract
from rift.types import Slice
from rift.types.msg import InternalMessage

from .util import compile


class SimpleMsg(Contract):
    """Simple Msg Contract."""

    def internal_receive(self) -> None:
        self.message.load()


def test_compile():
    compile(SimpleMsg)
