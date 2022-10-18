from rift import Cond, method
from rift.func.contract import Contract
from rift.types import Cell, Slice

from .util import compile


class SimpleStorage(Contract):
    @method()
    def recalc(self, a: int) -> int:
        return a

    @method()
    def untyped_func(
        self, theta: int, a: int, b: int, c: int,
    ) -> tuple[int, int, int]:
        return c * theta, a * theta, b * theta

    @method()
    def copy_num(self, val: int) -> tuple[int, int]:
        return val, val

    @method()
    def double_the_num(self, val: int) -> int:
        return val + 2 + 3

    def internal_receive(self) -> None:
        cs = self.message
        cs.skip_bits_(4)
        sender = cs.load_msg_addr_()
        op = self.body.load_uint_(32)
        with Cond() as c:
            c.match(op == 0x2013)
            r = self.double_the_num(op)
            r.recalc()
            with Cond() as c2:
                c2.match(r == 1)
                self.ret_()
            c.match(op == 0x2012)
            self.double_the_num(1)
            y1, y2 = self.copy_num(2)
            t = self.copy_num(9)
            x1, x2 = t
            u1, u2, u3 = self.untyped_func(x1, 4, 4, x2)
            u1, u2, u3 = x1.untyped_func(4, 4, x2)
            c.otherwise()
            self.double_the_num(4)
        return


def test_compile():
    compile(SimpleStorage)
