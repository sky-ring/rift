from dbuilder.func.contract import Contract
from dbuilder.types import Cell, Slice

from .util import compile


class Contract1(Contract):
    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        super(Contract1, self).internal_receive(
            balance,
            msg_value,
            in_msg_full,
            in_msg_body,
        )
        b = in_msg_body.uint(10)
        c = in_msg_body.coin()


def test_compile():
    compile(Contract1)
