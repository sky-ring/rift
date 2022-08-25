from dbuilder.core.condition import Cond
from dbuilder.core.loop import while_
from dbuilder.library.std import std
from dbuilder.types.types import Builder, Entity, Slice


class Payload:
    __magic__ = 0xA935E5
    __tag__ = "_"
    __data__: Slice

    def __init__(self, data_slice: Slice = None, name=None):
        # TODO: Handle the inheritance of the annotatins
        self.annotations = self.__annotations__
        if name is None:
            self.f_name = type(self).__name__.lower()
        else:
            self.f_name = name
        if data_slice:
            self.data_init(data_slice)

    def data_init(self, data_slice: Slice):
        self.__data__ = data_slice
        if not self.__data__.NAMED:
            self.__data__.__assign__(f"{self.f_name}_orig")
        self.cp = self.__data__.__assign__(f"{self.f_name}_cp")

    def load(self, proc_tag=True, master=True):
        if master:
            self.__predefine__(name=self.f_name)
        tag_len, tag = self.tag_data()
        if (not proc_tag) or tag_len == 0:
            self.load_body()
            return
        read_tag = self.__data__.int(tag_len)
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

    def iter_refs(self):
        return while_(self.__data__.slice_refs())

    def ref(self):
        return self.__data__.load_ref_()

    def hash(self, after=None):
        if after is None:
            return std.slice_hash(self.cp)
        for k, v in self.annotations.items():
            v.__deserialize__(self.cp, inplace=True)
            if k == after:
                break
        return std.slice_hash(self.cp)

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

    def as_cell(self):
        b = self.as_builder()
        return b.end()

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
        **kwargs,
    ):
        p: "Payload" = cls(from_, name=name)
        tag = True
        if "tag" in kwargs:
            tag = kwargs["tag"]
        p.load(proc_tag=tag, master=False)
        return p

    @classmethod
    def __predefine__(cls, name: str = None):
        if name is None:
            return
        for k, v in cls.__annotations__.items():
            v_name = f"{name}_{k}"
            v.__predefine__(name=v_name)

    def __getattr__(self, item):
        return getattr(self.__data__, item)

    @classmethod
    def type_name(cls) -> str:
        return "-"
