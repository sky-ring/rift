from test.util import compile

from rift import *
from rift.fift.tvm import TVM, TVMError


class CustomPayload(Payload):
    x: uint8
    y: uint4


class MaybeTypeTest(Contract):
    @method()
    def custom_payload(self) -> Cell:
        # Ensure Message Info is correctly costructed
        p = CustomPayload(x=1, y=2)
        return p.as_cell()


def test_compile():
    compile(MaybeTypeTest)


def test_run_custom_payload():
    c = compile(MaybeTypeTest)
    d = Cell()
    r = TVM.get_method(c.value, d.value, "custom_payload")
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    print(r)
