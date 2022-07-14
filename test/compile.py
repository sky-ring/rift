import unittest

from dbuilder import method, Cond, Engine
from dbuilder.types import Cell, Slice


class SimpleStorage:
    @method
    def double_the_num(self, val: int) -> int:
        return val + 2 + 3

    @method
    def rcv_internal(
        self,
        balance: int,
        msg_value: int,
        in_msg_full: Cell,
        in_msg_body: Slice,
    ) -> None:
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
            c.match(op == 0x2012)
            self.double_the_num(1)
            c.otherwise()
            self.double_the_num(4)


class CompileTestCase(unittest.TestCase):
    def test_simple_compile(self):
        compiled = Engine.compile(SimpleStorage)
        print(compiled.to_func())

    def test_patched_compile(self):
        t = Engine.patch(SimpleStorage, globals())
        compiled = Engine.compile(t)
        print(compiled.to_func())


if __name__ == "__main__":
    unittest.main()
