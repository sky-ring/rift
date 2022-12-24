import pytest

from rift.fift.types import Builder


@pytest.fixture
def builder():
    return Builder()


def test_init(builder: Builder):
    # Empty Builder
    assert builder.value == "te6ccgEBAQEAAgAAAA=="


def test_int(builder: Builder):
    b = builder.uint(1, 100).sint(-2, 2)
    assert b.bits_n() == 102
    assert b.refs_n() == 0
    s = b.end().parse()
    assert s.uint_(100) == 1
    assert s.sint_(2) == -2


def test_coins(builder: Builder):
    b = builder.coins(12422000123)
    b.cmd("85 .")
    s = b.end().parse()
    assert s.coin_() == 12422000123
