from rift.func.contract import Contract
from rift.types import Cell, Slice
from rift.types.coin import Coin
from rift.types.int_aliases import uint64
from rift.types.payload import Payload

from .util import compile


class BurnBody(Payload):
    query_id: uint64
    amount: Coin


class BuildPayload(Contract):
    """Build Payload Contract."""

    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        body = BurnBody()
        body.query_id = 1
        body.amount = 2
        b = body.as_cell()


def test_compile():
    compile(BuildPayload)
