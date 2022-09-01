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
        body = in_msg_body
        k = i
        while i == 0:
            a = in_msg_body.uint(8)
            if a == 0:
                v = a * 2
                if v & 5 == 0:
                    t = a * 43
                    while t | 1:
                        in_msg_body.ref_()
            elif a == 2:
                b = a * 4
            else:
                in_msg_body.coin()
        raise 0xFFFF


def test_compile():
    compile(PatchContract)
