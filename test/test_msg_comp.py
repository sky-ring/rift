from rift.fift.tvm import TVM, TVMError
from rift.fift.types.builder import Builder
from rift.func.contract import Contract
from rift.runtime.config import FiftMode, FunCMode
from rift.types import Cell, Slice
from rift.types.addr import MsgAddress
from rift.types.int_aliases import uint4
from rift.types.msg import InternalMessage

from .util import compile


class SimpleMsg(Contract):
    """Simple Msg Contract."""

    def internal_receive(self) -> None:
        # self.message.load()
        x = self.body >> uint4
        assert x == 10, 45


def test_compile():
    compile(SimpleMsg)


def test_run():
    c = compile(SimpleMsg)
    with FiftMode:
        body = Builder()
        body = body.uint(10, 4)
        body = body.end()
        msg = InternalMessage.build(
            dest=MsgAddress.std(0, 0),
            body=body,
        ).as_cell()
    d = Cell()
    r = TVM.get_method(c.value, d.value, 0, 0, 0, msg, body.parse())
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    print(r)
    pass
