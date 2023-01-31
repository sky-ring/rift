from rift.func.contract import Contract
from rift.types import Cell, Slice

from .util import compile


class PatchContract(Contract):
    def internal_receive(self) -> None:
        i = 0
        body = self.body
        k = i
        while i == 0:
            a = body.uint(8)
            if a == 0:
                v = a * 2
                if v & 5 == 0:
                    t = a * 43
                    while t | 1:
                        body.ref_()
            elif a == 2:
                b = a * 4
            else:
                body.coin_()
            i = 1
        raise 0xFFFF


def test_compile():
    compile(PatchContract)
