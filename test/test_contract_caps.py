from dbuilder import Cond, method
from dbuilder.func.contract import Contract
from dbuilder.types import Cell, Slice

from .util import compile


class SimpleStorage(Contract):
    @method()
    def copy_num(self, val: int) -> tuple[int, int]:
        return val, val

    @method()
    def double_the_num(self, val: int) -> int:
        return val + 2 + 3

    def internal_receive(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
        super(SimpleStorage, self).internal_receive(
            balance,
            msg_value,
            in_msg_full,
            in_msg_body,
        )
        cs = in_msg_full.begin_parse()
        cs.skip_bits_(4)
        sender = cs.load_msg_addr_()
        op = in_msg_body.load_uint_(32)
        with Cond() as c:
            c.match(op == 0x2013)
            r = self.double_the_num(op)
            r.recalc()
            with Cond() as c2:
                c2.match(sender == 1)
                sender.destroy()
                self.ret_()
            c.match(op == 0x2012)
            self.double_the_num(1)
            y1, y2 = self.copy_num(2)
            t = self.copy_num(9)
            x1, x2 = t
            u1, u2, u3 = x1.untyped_func(4, 4, "str", x2)
            c.otherwise()
            self.double_the_num(4)
        return


def test_compile():
    compile(SimpleStorage)
