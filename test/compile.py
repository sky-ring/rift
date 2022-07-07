import unittest

from dbuilder.annots import method
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
            r.some_shit()
            c.match(op == 0x2012)
            print("b")
            c.otherwise()
            print("x")


class CompileTestCase(unittest.TestCase):
    def test_simple_compile(self):
        Engine.compile(SimpleStorage)
        print(CallStacks.get_stack())
        print(CallStacks.func())

    def test_magic_compile(self):
        t = Engine.patch(SimpleStorage, globals())
        print(t == SimpleStorage)
        Engine.compile(t)
        print(CallStacks.get_stack())
        print(CallStacks.func())


if __name__ == '__main__':
    unittest.main()
