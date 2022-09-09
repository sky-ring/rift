from dbuilder.func.contract import Contract
from dbuilder.library.std import std
from dbuilder.types import Cell, Slice
from dbuilder.types.addr import MsgAddress
from dbuilder.types.coin import Coin
from dbuilder.types.int_aliases import uint32, uint64
from dbuilder.types.payload import Payload
from dbuilder.types.ref import Ref
from dbuilder.types.slice import slice

from .util import compile


class BurnNotification(Payload):
    op: uint32
    query_id: uint64
    amount: Coin
    owner: MsgAddress
    response: MsgAddress
    x: Ref[Cell]


class UnorderedLazyPayloads(Contract):
    """UnorderedLazyPayloads Contract."""

    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        msg = BurnNotification(in_msg_body)
        q_id = msg.query_id
        amount = msg.op
        j = msg.x


def test_compile():
    compile(UnorderedLazyPayloads)
