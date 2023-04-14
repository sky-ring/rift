from rift import *
from rift.ast.sentry.base_types import SentryHalted
from rift.ast.sentry.watchers.codes import ErrorCode

from test.util import compile


class DisallowUnsupportedSyntax(Contract):
    class Data(Model):
        a: uint32

    async def async_f(self):
        async with 11 as f:
            pass
        pass

    def self_yield(self):
        yield self

    def external_receive(self) -> None:
        try:
            x = self.data.a
        except Exception:
            pass
        list_comp = [Entity() for i in range(10)]
        dict_comp = {i: Entity() for i in range(10)}
        set_comp = {Entity() for i in range(10)}
        gen_comp = (Entity() for i in range(10))
        del self.data
        with 10 as f:

            def theta():
                nonlocal gen_comp

        if (a := 10) == 11:
            print(a)
            pass

        f_str = f"a: {a:.3f}"
        a, *b = list_comp
        theta = list_comp[1:3]
        lx = 0 if a % 2 == 0 else 1
        tl = lambda xx: xx * 2

        match self.data:
            case True:
                pass


def test_compile():
    try:
        compile(DisallowUnsupportedSyntax)
        raise RuntimeError("Shouldn't have compiled")
    except SentryHalted as halt:
        assert len(halt.warnings) == 18
        codes = {e.code.value for e in halt.warnings}
        expected = {
            c
            for c in range(
                ErrorCode.NoAsync.value, ErrorCode.NoComprehension.value + 1
            )
        }
        assert codes == expected
