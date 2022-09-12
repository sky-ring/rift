from rift.ast.types import Expr
from rift.core import Entity
from rift.core.factory import Factory
from rift.core.utils import init_abstract_type
from rift.types.bases.builder_base import _BuilderBase
from rift.types.bases.cell_base import _CellBase
from rift.types.bases.cont_base import _ContBase
from rift.types.bases.dict_base import _DictBase
from rift.types.bases.idict_base import _IDictBase
from rift.types.bases.int_base import _IntBase
from rift.types.bases.pfxdict_base import _PfxDictBase
from rift.types.bases.slice_base import _SliceBase
from rift.types.bases.string_base import _StringBase
from rift.types.bases.udict_base import _UDictBase


class Int(_IntBase):
    def __init__(self, value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        if "data" not in kwargs:
            self.data = Expr.const(value)

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> "Int":
        return cls(0, *args, **kwargs)

    @classmethod
    def type_name(cls) -> str:
        return "int"


class HexInt(_IntBase):
    def __init__(self, value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        if "data" not in kwargs:
            self.data = Expr.const(value)

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> "Int":
        return cls(0, *args, **kwargs)

    def _repr_(self):
        return hex(self.value)

    @classmethod
    def type_name(cls) -> str:
        return "int"


class Slice(_SliceBase):
    @classmethod
    def type_name(cls) -> str:
        return "slice"

    def __rshift__(self, other):
        return other.__deserialize__(self)


class Cont(_ContBase):
    @classmethod
    def type_name(cls) -> str:
        return "cont"


class String(_StringBase):
    @classmethod
    def type_name(cls) -> str:
        return "string"


class Cell(_CellBase):
    @classmethod
    def type_name(cls) -> str:
        return "cell"


class Dict(_DictBase):
    @classmethod
    def type_name(cls) -> str:
        return "cell"


class UDict(_UDictBase):
    pass


class IDict(_IDictBase):
    pass


class PfxDict(_PfxDictBase, Cell):
    @classmethod
    def type_name(cls) -> str:
        return "cell"


class Builder(_BuilderBase):
    @classmethod
    def type_name(cls) -> str:
        return "builder"


class Tensor(Entity, tuple):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args)

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        data = kwargs.pop("data", None)
        self.type_ = kwargs.pop("type_", None)
        super().__init__(data=data, name=name)

    def __iter__(self):
        if not self.type_:
            return super().__iter__()
        if hasattr(self, "__unpackable") and self.__unpackable:
            for _, tp in zip(range(self._unpack_len), self.type_.__args__):
                yield init_abstract_type(tp)


class Tuple(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "tuple"


Factory.register("Tensor", Tensor)
Factory.register("Tuple", Tuple)
Factory.register("Builder", Builder)
Factory.register("Dict", Dict)
Factory.register("UDict", UDict)
Factory.register("IDict", IDict)
Factory.register("PfxDict", PfxDict)
Factory.register("Slice", Slice)
Factory.register("Cell", Cell)
Factory.register("String", String)
Factory.register("Cont", Cont)
Factory.register("Int", Int)
Factory.register("HexInt", HexInt)
