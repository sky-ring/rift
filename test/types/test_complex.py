from rift import *
from rift.fift.tvm import TVM, TVMError
from test.util import compile


class Point(Payload):
    a: uint16
    b: uint16


class ComplexPayload(Payload):
    x: uint8
    y: uint4
    z1: Maybe[uint10]
    z2: Maybe[uint10]
    t: EitherRef[Point]
    t2: EitherRef[Point]


class ComplexTypeTest(Contract):
    @method()
    def custom_payload(self) -> Cell:
        p1 = Point(a=1, b=2)
        p = ComplexPayload(
            x=0,
            y=10,
            z1=20,
            z2=None,
            t=p1,
            t2=p1.as_ref(),
        )
        return p.as_cell()

    @method()
    def custom_payload_de(self, c: Cell) -> None:
        # Ensure Data is correctly costructed
        p = ComplexPayload(c.parse())
        assert p.t2.a == 1, 100
        assert p.x == 0, 101
        assert p.y == 10
        assert p.z1.bound == 20, 103
        assert ~ p.z2.has, 104
        assert p.t.a == 1, 105
        assert p.t.b == 2, 106
        assert p.t2.a == 1, 107
        assert p.t2.b == 2, 108


def obtain_custom_payload():
    c = compile(ComplexTypeTest)
    d = Cell()
    r = TVM.get_method(c.value, d.value, "custom_payload")
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
    out_cell, = r.stack
    return out_cell


def test_run_custom_payload():
    out_cell = obtain_custom_payload()
    payload = ComplexPayload(out_cell.parse())
    assert payload.t2.a == 1
    assert payload.x == 0
    assert payload.y == 10
    assert payload.z1 == 20
    assert payload.z2 is None
    assert payload.t.a == 1
    assert payload.t.b == 2
    assert payload.t2.a == 1
    assert payload.t2.b == 2


def test_run_custom_payload_fc():
    c = compile(ComplexTypeTest)
    d = Cell()
    out_cell = obtain_custom_payload()
    r = TVM.get_method(c.value, d.value, "custom_payload_de", out_cell)
    if isinstance(r, TVMError):
        print(r.exit_code)
        print(r.logs)
        raise AssertionError()
