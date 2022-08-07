from dbuilder.library.std import std
from dbuilder.types.sized_int import SizedIntType


class Model:
    __magic__ = 0xBB10C0

    def __init__(self):
        self.annotations = self.__annotations__
        self.items = list(self.annotations.keys())

    def load(self):
        data = std.get_data().parse()
        data.__assign__("data")
        for k, v in self.annotations.items():
            if issubclass(v, SizedIntType):
                name = f"data_{k}"
                if v.__signed__:
                    v = data.int_(v.__bits__)
                else:
                    v = data.uint_(v.__bits__)
                v.__assign__(name)
                setattr(self, k, v)

    def save(self):
        builder = std.begin_cell()
        for k, v in self.annotations.items():
            if issubclass(v, SizedIntType):
                c_v = getattr(self, k)
                builder = builder.store_uint(c_v, v.__bits__)
        cell = builder.end_cell()
        std.set_data(cell)

    def get(self, key):
        data = std.get_data().parse()
        data.__assign__("data")
        for k, v in self.annotations.items():
            if issubclass(v, SizedIntType):
                b = v.__bits__
                if v.__signed__:
                    if k == key:
                        res = data.int(b)
                        break
                    res = data.int_(v.__bits__)
                else:
                    if k == key:
                        res = data.uint(b)
                        break
                    res = data.uint_(v.__bits__)
        return res
