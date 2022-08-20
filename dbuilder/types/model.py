from dbuilder.library.std import std


class Model:
    __magic__ = 0xBB10C0

    def __init__(self):
        self.annotations = self.__annotations__
        self.items = list(self.annotations.keys())

    def load(self):
        data = std.get_data().parse()
        data.__assign__("data")
        for k, v in self.annotations.items():
            name = f"data_{k}"
            n = v.__deserialize__(data, name=name, inplace=True)
            setattr(self, k, n)

    def save(self):
        builder = std.begin_cell()
        for k, v in self.annotations.items():
            c_v = getattr(self, k)
            builder = v.__serialize__(builder, c_v)
        cell = builder.end()
        cell.set_data()

    def get(self, key):
        data = std.get_data().parse()
        data.__assign__("data")
        for k, v in self.annotations.items():
            target = k == key
            res = v.__deserialize__(data, inplace=not target)
            if target:
                break
        return res
