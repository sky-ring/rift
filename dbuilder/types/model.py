from dbuilder.core.entity import Entity
from dbuilder.library.std import std
from dbuilder.types.msg import StateInit


class Model:
    __magic__ = 0xBB10C0
    _pointer: int
    _skipped_ones: dict[str, Entity]

    def __init__(self):
        self.annotations = self.__annotations__
        self._items = list(self.annotations.keys())
        self._lazy = True
        self._skipped_ones = {}
        self._pointer = 0

    def __getattr__(self, item):
        # This gets called whenever item doesn't exist in data model
        # So we'll check whether it's really from fields or not
        # Purpose => Lazy Loading
        # if not self._lazy or item not in self._items:
        #     # Q: Is this a good idea?
        #     return getattr(self.__data__, item)
        if item in self._skipped_ones:
            n = self._skipped_ones[item]
            name = f"data_{item}"
            return n.__assign__(name)

        if item not in self.annotations:
            raise AttributeError()

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
                # self.__predefine__(name=name, lazy=True, target=t)
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
