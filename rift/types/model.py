from rift.core.entity import Entity
from rift.library.std import std
from rift.types.msg import StateInit


class Model:
    __magic__ = 0xBB10C0
    _pointer: int
    _skipped_ones: dict[str, Entity]

    def __init__(self, **kwargs):
        self.annotations = self.__annotations__
        self._items = list(self.annotations.keys())
        self._lazy = True
        self._skipped_ones = {}
        self._pointer = 0
        if len(kwargs) != 0:
            self._build = True
            for k in self.annotations:
                setattr(self, k, None)
            for k in kwargs:
                if k in self.annotations:
                    setattr(self, k, kwargs[k])

    def __getattr__(self, item):
        # This gets called whenever item doesn't exist in data model
        # So we'll check whether it's really from fields or not
        # Purpose => Lazy Loading

        if item not in self.annotations:
            raise AttributeError()

        if item in self._skipped_ones:
            n = self._skipped_ones[item]
            name = f"data_{item}"
            return n.__assign__(name)

        if self._pointer == 0:
            self.__data__ = std.get_data().parse()
            self.__data__.__assign__("data")

        # Strategy => Skip if not present
        targets = self._items[self._pointer :]
        for t in targets:
            self._pointer += 1
            v = self.annotations[t]
            is_ = t == item
            name = None
            if is_:
                name = f"data_{t}"
            n = v.__deserialize__(
                self.__data__,
                name=name,
                inplace=True,
                lazy=True,
            )
            if is_:
                setattr(self, t, n)
                return n
            else:
                self._skipped_ones[t] = n

    def load(self):
        data = std.get_data().parse()
        data.__assign__("data")
        for k, v in self.annotations.items():
            name = f"data_{k}"
            n = v.__deserialize__(data, name=name, inplace=True)
            setattr(self, k, n)

    def as_cell(self):
        builder = std.begin_cell()
        for k, v in self.annotations.items():
            c_v = getattr(self, k)
            builder = v.__serialize__(builder, c_v)
        cell = builder.end()
        return cell

    def save(self):
        cell = self.as_cell()
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

    def copy(self, reset=False):
        cp = type(self)()
        if not reset:
            cp.__dict__ = {**self.__dict__}
        return cp
