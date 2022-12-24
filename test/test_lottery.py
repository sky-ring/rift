from rift import *
from rift.core.annots import asm
from rift.fift.tvm import TVM, TVMError

from .util import compile


class LoterryHacker(Contract):
    @impure
    @asm()
    def custom_seed(self, seed: int) -> None:
        return "SETRAND"

    @method()
    def break_the_lottery(self) -> int:
        start_lt = 32253735000005
        discovered = 0
        i = 0
        while discovered != 1:
            i = i + 1
            self.custom_seed(start_lt + i)
            new_rand = std.rand(10000)
            if new_rand == 7777:
                discovered = 1
        return start_lt + i


def test_compile():
    compile(LoterryHacker)


def test_run():
    c = compile(LoterryHacker)
    d = Cell()
    r = TVM.get_method(c.value, d.value, "break_the_lottery")
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    print("Gas cost in TONs: ", r.gas / (10**6))
    (lottery_seed,) = r.stack
    assert lottery_seed == 32253735006889
