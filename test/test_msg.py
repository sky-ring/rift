from dbuilder.func.contract import Contract
from dbuilder.types import Slice
from dbuilder.types.msg import InternalMessage

from .util import compile


class SimpleMsg(Contract):
    """Simple Msg Contract."""

    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        payload = InternalMessage(in_msg)
        payload.load()


def test_compile():
    compile(SimpleMsg)
