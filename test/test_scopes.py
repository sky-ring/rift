from dbuilder.func.contract import Contract
from dbuilder.types import Slice

from .util import compile


class Scopes(Contract):
    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        x = in_msg
        while x.uint_(2) == 0:
            if x.uint(1) == 1:
                b = 4
                b = 2
                x = in_msg.addr_()
            else:
                b = 6
                b = 10
        b = 1
        b = 3


def test_compile():
    compile(Scopes)
