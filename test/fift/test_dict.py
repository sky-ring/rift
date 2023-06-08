import pytest

from rift.fift.types.builder import Builder
from rift.fift.types.dict import Dict


@pytest.fixture
def dict_():
    return Dict()


# def test_init(d: Dict):
#     # Empty Builder
#     assert builder.value == "te6ccgEBAQEAAgAAAA=="


def test_rw_value(dict_: Dict):
    b = Builder()
    b = b.uint(1, 10)
    s = b.end().parse()
    slice_hash = s.hash()
    dict_, ok = dict_.idict_set(1, 0, s)
    assert ok == -1
    v = dict_.idict_get(1, 0)
    assert v is not None
    assert v.hash() == slice_hash
