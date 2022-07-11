import unittest

from dbuilder.annots import method
from dbuilder.ast.printer import Printer
from dbuilder.calls import CallStacks
from dbuilder.condition import Cond
from dbuilder.engine import Engine


class SimpleStorage:
    @method
    def double_the_num(self, val):
        return val + 2 + 3

    @method
    def rcv_internal(self, balance, msg_value, in_msg_full, in_msg_body):
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
        Engine.compile(SimpleStorage)
        v = CallStacks.current_contract
        p = Printer()
        v.print_func(p)
        print(p.out())

    def test_magic_compile(self):
        t = Engine.patch(SimpleStorage, globals())
        Engine.compile(t)
        v = CallStacks.current_contract
        p = Printer()
        v.print_func(p)
        x = open("test.func", "w")
        x.write(p.out())
        x.close()


if __name__ == '__main__':
    unittest.main()
