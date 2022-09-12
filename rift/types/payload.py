from rift.ast.ref_table import ReferenceTable
from rift.core.condition import Cond
from rift.core.loop import while_
from rift.library.std import std
from rift.types.types import Builder, Cell, Entity, Int, Slice
from rift.types.utils import Subscriptable


class Payload(metaclass=Subscriptable):
    __magic__ = 0xA935E5
    __tag__ = "_"
    __data__: Slice
    _pointer: int
    _skipped_ones: dict[str, Entity]

    def __init__(
        self,
        data_slice: Slice = None,
        name=None,
        lazy=True,
        **kwargs,
    ):
        # TODO: Handle the inheritance of the annotatins
        self.annotations = self.__annotations__
        self._items = list(self.annotations.keys())
        self._lazy = lazy
        self._pointer = 0
        self._skipped_ones = {}
        self.__data__ = None
        if name is None:
            self.f_name = type(self).__name__.lower()
        else:
            self.f_name = name
        if data_slice:
            self.data_init(data_slice)
        if self.__data__ is None:
            # TODO: Fix [Probably replace it with special NoneEntity]
            # This snippet was used to ease building
            # But it causes problem with lazy access (for set)
            # for k in self.annotations:
            #     setattr(self, k, None)
            for k in kwargs:
                if k in self.annotations:
                    setattr(self, k, kwargs[k])

    def __setattr__(self, __name: str, __value) -> None:
        if isinstance(__value, int) and not __name.startswith("_"):
            __value = Int(__value)
        super().__setattr__(__name, __value)

    def __getattr__(self, item):
        # This gets called whenever item doesn't exist in payload
        # So we'll check whether it's really from fields or not
        # Purpose => Lazy Loading
        if item in self._skipped_ones:
            n = self._skipped_ones[item]
            name = f"{self.f_name}_{item}"
            return n.__assign__(name)

        if self.__data__ is None:
            name = f"{self.f_name}_{item}"
            return Entity(name=name)
        if not self._lazy or item not in self._items:
            # Q: Is this a good idea?
            return getattr(self.__data__, item)
        if self._pointer == 0:
            tag_len, _ = self.tag_data()
            if tag_len != 0:
                self.__data__.uint_(tag_len)
        # Strategy => Skip if not present
        targets = self._items[self._pointer :]
        for t in targets:
            self._pointer += 1
            v = self.annotations[t]
            is_ = t == item
            name = None
            if is_:
                name = f"{self.f_name}_{t}"
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

    def data_init(self, data_slice: Slice):
        self.__data__ = data_slice
        if not self.__data__.NAMED:
            self.__data__.__assign__(f"{self.f_name}_orig")
        self.__origin__ = self.__data__.__assign__(f"{self.f_name}_cp")
        ReferenceTable.eliminatable(f"{self.f_name}_cp")

    def load(self, proc_tag=True, master=True):
        if master:
            self.__predefine__(name=self.f_name)
        tag_len, tag = self.tag_data()
        if (not proc_tag) or tag_len == 0:
            self.load_body()
            return
        read_tag = self.__data__.uint(tag_len)
        with Cond() as c:
            c.match(read_tag == tag)
            self.skip_tag(self.__data__)
            self.load_body()

    def load_body(self):
        for k, v in self.annotations.items():
            name = f"{self.f_name}_{k}"
            n = v.__deserialize__(self.__data__, name=name, inplace=True)
            setattr(self, k, n)

    def __assign__(self, name):
        self.f_name = name

    def __rshift__(self, other):
        return other.__deserialize__(self.__data__)

    def refs(self):
        return self.__data__.slice_refs()

    def iter_refs(self):
        return while_(self.__data__.slice_refs())

    def ref(self):
        return self.__data__.load_ref_()

    def hash(self, after=None):
        if after is None:
            return std.slice_hash(self.__origin__)
        for k, v in self.annotations.items():
            v.__deserialize__(self.__origin__, inplace=True)
            if k == after:
                break
        return std.slice_hash(self.__origin__)

    def as_builder(self):
        builder = std.begin_cell()
        return self.to_builder(builder)

    @classmethod
    def write_tag(cls, builder):
        tag_len, tag = cls.tag_data()
        if tag_len > 0:
            builder = builder.uint(tag, tag_len)
        return builder

    @classmethod
    def tag_data(cls):
        _tag_len = 0
        tag = -1
        if cls.__tag__.startswith("#"):
            # hex
            t = cls.__tag__.replace("#", "")
            _tag_len = len(t) * 4
            tag = int(t, 16)
        elif cls.__tag__.startswith("$"):
            # bin
            t = cls.__tag__.replace("$", "")
            _tag_len = len(t)
            tag = int(t, 2)
        elif cls.__tag__.startswith("|"):
            # this is the auto tag
            # would be better if we'd calculate
            # automatically
            t = cls.__tag__.replace("|", "")
            _tag_len = 32
            tag = int(t, 16)
        return _tag_len, tag

    @classmethod
    def skip_tag(cls, from_):
        tag_len, _ = cls.tag_data()
        from_.skip_bits_(tag_len)

    def to_builder(self, builder):
        builder = self.write_tag(builder)
        for k, v in self.annotations.items():
            c_v = getattr(self, k)
            builder = v.__serialize__(builder, c_v)
        return builder

    def origin_slice(self):
        return self.__origin__

    def rest(self):
        return self.__data__

    def as_cell(self) -> "Cell":
        b = self.as_builder()
        return b.end()

    def as_ref(self):
        from rift.types.ref import Ref

        type_ = Ref[type(self)]
        return type_(self.as_cell())

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        p: "Payload" = value
        b = p.to_builder(to)
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
        lazy: bool = True,
        **kwargs,
    ):
        p: "Payload" = cls(from_, name=name)
        tag = True
        if "tag" in kwargs:
            tag = kwargs["tag"]
        if not lazy:
            p.load(proc_tag=tag, master=False)
        return p

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
        lazy: bool = True,
        **kwargs,
    ):
        if name is None:
            return
        if lazy and "target" in kwargs:
            tg = kwargs["target"]
            targets = {tg: cls.__annotations__[tg]}
        else:
            targets = cls.__annotations__

        for k, v in targets.items():
            v_name = f"{name}_{k}"
            v.__predefine__(name=v_name, lazy=lazy, **kwargs)

    @classmethod
    def type_name(cls) -> str:
        return "-"
