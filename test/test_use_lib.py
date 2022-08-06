from dbuilder.func.contract import Contract
from dbuilder.library.std import std
from dbuilder.types import Cell, Slice

from .util import compile


class Contract2(Contract):
    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        super(Contract2, self).internal_receive(
            balance,
            msg_value,
            in_msg_full,
            in_msg_body,
        )
        signature = in_msg_body.load_bits_(512)
        cs = in_msg_body
        msg_seqno = cs.load_uint_(32)
        valid_until = cs.load_uint_(32)
        self.throw_if(35, valid_until <= std.now())
        o = std.load_uint_(cs, 10)
        x = 10
        y = 15
        min, max = std.minmax(y, x)


def test_compile():
    compile(Contract2)
