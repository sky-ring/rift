from rift import *

from .util import compile


class Loop(Contract):
    @method()
    def traverse_the_loop(self) -> int:
        i = 0
        while 1:
            i = i + 1
            if i == 7777:
                break
        return i


def test_compile():
    try:
        compile(Loop)
        # Should not compile as FunC doesn't support break
        raise AssertionError()
    except Exception:
        # Failed as expected
        pass
