from rift.func.contract import Contract
from rift.types import Cell, Slice
from rift.types.addr import MsgAddress
from rift.types.coin import Coin
from rift.types.int_aliases import uint32, uint64
from rift.types.payload import Payload
from rift.types.ref import Ref

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

    def internal_receive(self) -> None:
        msg = self.body % BurnNotification
        q_id = msg.query_id
        amount = msg.op
        j = msg.x


def test_compile():
    compile(UnorderedLazyPayloads)
