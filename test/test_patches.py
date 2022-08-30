from dbuilder.func.contract import Contract
from dbuilder.types import Cell, Slice

from .util import compile


class PatchContract(Contract):
    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        i = 0
        while i == 0:
            a = in_msg_body.int(8)
            if a == 0:
                v = a * 2
            elif a == 2:
                b = a * 4
            else:
                in_msg_body.coin()


def test_compile():
    compile(PatchContract)
