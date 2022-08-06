from dbuilder.library.std import Stdlib

from .util import compile


def test_compile():
    compile(Stdlib)
