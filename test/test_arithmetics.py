from rift.func.contract import Contract
from rift.types import Slice

from .util import compile


class Arithmetics(Contract):
    def external_receive(self) -> None:
        some_const = -2
        v = self.body.load_uint_(8)
        _ = v + 2
        _ = v / 2
        _ = v - 2
        _ = v * 2
        _ = 2 + v
        _ = 2 / v
        _ = 2 - v
        _ = 2 * v
        _ = ~v
        _ = -v
        _ = v <= 2
        _ = v < 2
        _ = v > 2
        _ = v >= 2
        _ = v == 2
        _ = v != 2
        _ = v | 2
        _ = v & 2
        _ = 2 | v
        _ = 2 & v


def test_compile():
    compile(Arithmetics)
