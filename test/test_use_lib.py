from rift.func.contract import Contract
from rift.library.std import std
from rift.types import Cell, Slice

from .util import compile


class Contract2(Contract):
    def internal_receive(self) -> None:
        signature = self.body.load_bits_(512)
        cs = self.body
        msg_seqno = cs.load_uint_(32)
        valid_until = cs.load_uint_(32)
        self.throw_if(35, valid_until <= std.now())
        std.skip_bits_(cs, 1)
        x = 10
        y = 15
        x = x + 1
        min, max = std.minmax(y, x)


def test_compile():
    compile(Contract2)
