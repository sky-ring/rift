from rift import *
from rift.fift.tvm import TVM, TVMError, TVMResult
from rift.runtime.config import Config, Mode

from .util import compile


class SimpleMethod(Contract):
    """
    Simple Contract with a method
    """

    @method()
    def multiply_by_two(self, x: int) -> int:
        return x * 2

    def external_receive(self) -> None:
        pass


def test_compile():
    compile(SimpleMethod)


def test_method():
    cell = compile(SimpleMethod)
    Config.mode = Mode.FIFT
    d = Cell()
    r = TVM.get_method(cell.value, d.value, "multiply_by_two", 10)
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    (rs,) = r.stack
    assert rs == 20
