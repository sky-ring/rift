from dbuilder.core.loop import while_
from dbuilder.library.std import std
from dbuilder.types.sized_int import SizedIntType
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
            if issubclass(v, SizedIntType):
                name = f"{self.f_name}_{k}"
                if v.__signed__:
                    v = self.data.int_(v.__bits__)
                else:
                    v = self.data.uint_(v.__bits__)
                v.__assign__(name)
                setattr(self, k, v)

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
            if issubclass(v, SizedIntType):
                if v.__signed__:
                    self.cp.int_(v.__bits__)
                else:
                    self.cp.uint_(v.__bits__)
            if k == after:
                break
        return std.slice_hash(self.cp)
