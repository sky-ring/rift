import pytest

from rift.fift.types.builder import Builder
from rift.fift.types.dict_impl import IDict, UDict


@pytest.fixture
def udict_():
    return IDict()


@pytest.fixture
def idict_():
    return UDict()


def b_and_s():
    b = Builder()
    b = b.uint(1, 10)
    s = b.end().parse()
    return b, s


def test_rw_value_u(udict_: UDict):
    b, s = b_and_s()
    slice_hash = s.hash()
    udict_[0, 1] = s
    v = udict_[0, 1]
    assert v is not None
    assert v.hash() == slice_hash


def test_rw_value_ub(udict_: UDict):
    b, s = b_and_s()
    slice_hash = s.hash()
    udict_[0, 1] = b
    v = udict_[0, 1]
    assert v is not None
    assert v.hash() == slice_hash


def test_rw_value_i(idict_: IDict):
    b, s = b_and_s()
    slice_hash = s.hash()
    idict_[0, 1] = s
    v = idict_[0, 1]
    assert v is not None
    assert v.hash() == slice_hash


def test_rw_value_ib(idict_: IDict):
    b, s = b_and_s()
    slice_hash = s.hash()
    idict_[0, 1] = b
    v = idict_[0, 1]
    assert v is not None
    assert v.hash() == slice_hash


def test_del_value(idict_: IDict):
    b, s = b_and_s()
    idict_[0, 1] = b
    del idict_[0, 1]
    v = idict_[0, 1]
    assert v is None
