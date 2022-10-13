from rift import *
from rift.runtime.config import *


class ExternalBody(Payload):
    seq_no: uint32
    valid_until: uint32


def test_payload_deserialize():
    Config.mode = Mode.FIFT
    s = Builder().uint(1, 32).sint(-1, 32).end().parse()
    e = ExternalBody(s)
    assert e.seq_no == 1
    assert e.valid_until == 4294967295


def test_payload_serialize():
    e = ExternalBody(seq_no=1, valid_until=4294967295)
    c = e.as_cell().parse()
    assert c.uint_(32) == 1
    assert c.sint_(32) == -1


class ComplexPayload(Payload):
    color: Either[uint32, uint64]
    bg: Maybe[int24]


def test_complex_deserialize():
    s = Builder().uint(0, 1).uint(1, 32).uint(1, 1).sint(-1, 24).end().parse()
    e = ComplexPayload(s)
    assert e.color == 1
    assert e.bg == -1
    s = Builder().uint(1, 1).uint(2, 64).uint(0, 1).end().parse()
    e = ComplexPayload(s)
    assert e.color == 2
    assert e.bg is None
