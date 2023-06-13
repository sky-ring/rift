from typing import TYPE_CHECKING, Union

from rift.fift.types.dict import Dict

if TYPE_CHECKING:
    from rift.fift.types.slice import Slice
    from rift.fift.types.builder import Builder
    from rift.fift.types.int import Int


class GDict(Dict):
    def __init__(self, __value__=None, __g_id__=None):
        super().__init__(__value__=__value__)
        self.__g_id__ = __g_id__

    def set(
        self,
        n_bits: "Int",
        x: "Int",
        value: Union["Slice", "Builder"],
        exists_ok=True,
    ):
        from rift.fift.types.slice import Slice

        g = self.generic_identifier()
        cmd = f"{g}dict!" if isinstance(value, Slice) else f"b>{g}dict!"
        if not exists_ok:
            cmd += "+"
        new_d, ok = self.cmd(cmd, value, x, self, n_bits)
        new_d = GDict(__value__=new_d.value, __g_id__=g)
        return new_d, ok

    def set_(
        self,
        n_bits: "Int",
        x: "Int",
        value: Union["Slice", "Builder"],
        exists_ok=True,
    ):
        new_d, ok = self.set(n_bits, x, value, exists_ok)
        if not ok:
            raise RuntimeError()
        self.value = new_d.value

    def get(self, n_bits: "Int", x: "Int"):
        g = self.generic_identifier()
        stack_out = self.cmd(f"{g}dict@", x, self, n_bits)
        if len(stack_out) == 1:
            return None
        else:
            return stack_out[0]

    def remove(self, n_bits: "Int", x: "Int"):
        g = self.generic_identifier()
        new_d, ok = self.cmd(f"{g}dict-", x, self, n_bits)
        new_d = GDict(__value__=new_d.value, __g_id__=g)
        return new_d, ok

    def remove_(self, n_bits: "Int", x: "Int"):
        new_d, ok = self.remove(n_bits, x)
        if not ok:
            raise RuntimeError()
        self.value = new_d.value

    def pop(self, n_bits: "Int", x: "Int"):
        g = self.generic_identifier()
        stack_out = self.cmd(f"{g}dict-", x, self, n_bits)
        if len(stack_out) == 3:
            new_d, v, ok = stack_out
        else:
            new_d, ok = stack_out
            v = None
        new_d = GDict(__value__=new_d.value, __g_id__=g)
        return new_d, v, ok

    def pop_(self, n_bits: "Int", x: "Int"):
        new_d, v, ok = self.pop(n_bits, x)
        if not ok:
            raise RuntimeError()
        self.value = new_d.value
        return v

    def __setitem__(self, key, value):
        k, n, *left = key
        if len(left) != 0:
            exist_nok_flag = left[0]
        else:
            exist_nok_flag = False
        self.set_(n, k, value, exists_ok=not exist_nok_flag)

    def __getitem__(self, item):
        k, n = item
        return self.get(n, k)

    def __delitem__(self, key):
        k, n = key
        self.remove_(n, k)

    def generic_identifier(self):
        return self.__g_id__
