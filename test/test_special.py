from rift import *
from rift.runtime.config import FunCMode


def test_special_methods():
    FunCMode.activate()
    i = Int(0)
    j = Int(2)
    assert str(i == j) == "0 == 2"
