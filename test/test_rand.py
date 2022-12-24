from rift import *
from rift.core.annots import asm
from rift.fift.tvm import TVM, TVMError

from .util import compile


class RandomGenerator(Contract):
    @impure
    @asm()
    def custom_seed(self, seed: int) -> None:
        return "SETRAND"

    @method_id()
    @method()
    def rand_no(self) -> int:
        self.custom_seed(10000000000000001545)
        return std.rand(10000)


def test_compile():
    compile(RandomGenerator)


def test_run():
    c = compile(RandomGenerator)
    d = Cell()
    r = TVM.get_method(c.value, d.value, "rand_no")
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    (rand_no,) = r.stack
    assert rand_no == 7777
