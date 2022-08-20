from dbuilder.core.loop import while_
from dbuilder.library.std import std
from dbuilder.types.types import Slice


class Payload:
    data: Slice

    def __init__(self, data_slice: Slice):
        self.data = data_slice
        self.annotations = self.__annotations__
        self.f_name = type(self).__name__.lower()
        # Local Copy
        self.cp = self.data.__assign__(f"{self.f_name}_cp")

    def load(self):
        for k, v in self.annotations.items():
            name = f"{self.f_name}_{k}"
            n = v.__deserialize__(self.data, name=name, inplace=True)
            setattr(self, k, n)

    def __assign__(self, name):
        self.f_name = name

    def iter_refs(self):
        return while_(self.data.slice_refs())

    def ref(self):
        return self.data.load_ref_()

    def hash(self, after=None):
        if after is None:
            return std.slice_hash(self.cp)
        for k, v in self.annotations.items():
            v.__deserialize__(self.cp, inplace=True)
            if k == after:
                break
        return std.slice_hash(self.cp)
