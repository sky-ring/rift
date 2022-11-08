from rift.core.annots import asm, impure
from rift.fift.tvm import TVM, TVMError
from rift.fift.types.builder import Builder
from rift.func.contract import Contract
from rift.runtime.config import FiftMode
from rift.types import Cell, Slice
from rift.types.addr import MsgAddress
from rift.types.int_aliases import uint4
from rift.types.msg import InternalMessage
from rift.types.ref import Ref

from .util import compile


class SimpleMsgConstruct(Contract):
    """Simple Msg Contract."""

    @impure
    @asm()
    def dump_stack(self) -> None:
        return "DUMPSTK"

    @impure
    @asm()
    def dump(self, a: int) -> None:
        return "DUMP"

    @asm()
    def equal_slices(self, a: Slice, b: Slice) -> int:
        return "SDEQ"

    def internal_receive(self) -> None:
        # Ensure Message Info is correctly costructed
        assert self.message.info.ihr_disabled, 1
        assert self.message.info.bounce, 2
        assert ~self.message.info.bounced, 3
        assert self.message.info.src.is_equal(MsgAddress.empty()), 4
        assert self.message.info.dest.is_equal(MsgAddress.std(0, 0)), 5
        assert ~self.message.info.value.amount, 6
        assert self.message.info.value.other.dict_empty_check(), 7
        assert ~self.message.info.ihr_fee, 8
        assert ~self.message.info.fwd_fee, 9
        assert ~self.message.info.created_lt, 10
        assert ~self.message.info.created_at, 11
        # Ensure Init is absent
        assert ~self.message.init.is_present(), 12
        # Ensure Body isn't ref , and parse it
        assert ~self.message.body.is_ref(), 13
        x2 = self.message.body.bound >> uint4
        x = self.body >> uint4
        assert x == 10, 14
        assert x == x2, 15

    def external_receive(self) -> None:
        # Ensure Message Info is correctly costructed
        assert self.message.info.src.is_equal(MsgAddress.empty()), 1
        # assert self.message.info.dest.is_equal(MsgAddress.std(0, 0)), 2
        assert ~self.message.info.import_fee, 3
        # Ensure Init is present
        assert self.message.init.is_present(), 4
        assert self.message.init.data.is_present(), 5
        assert self.message.init.code.is_present(), 6
        x2 = self.message.body.bound >> uint4
        x = self.body >> uint4
        assert x == 10, 14
        assert x == x2, 15


def test_compile():
    compile(SimpleMsgConstruct)


def test_run_internal():
    c = compile(SimpleMsgConstruct)
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


def test_run_external():
    c = compile(SimpleMsgConstruct)
    with FiftMode:
        body = Builder()
        body = body.uint(10, 4)
        body = body.end()
        body_ref = Ref[Cell](body)
        d = Cell()
        msg, address = SimpleMsgConstruct.deploy(
            d,
            body=body,
            amount=0,
            independent=True,
            ref_state=False,
        )
    d = Cell()
    r = TVM.get_method(c.value, d.value, -1, 0, 0, msg, body.parse())
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    print(r)
    pass
