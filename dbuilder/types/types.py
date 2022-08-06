from dbuilder.ast.types import Expr
from dbuilder.core import Entity
from dbuilder.core.factory import Factory
from dbuilder.core.invokable import TypedInvokable, typed_invokable


class Int(Entity):
    def __init__(self, value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        self.data = Expr.const(value)

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> "Int":
        return cls(0, *args, **kwargs)

    @classmethod
    def type_name(cls) -> str:
        return "int"

    def _repr_(self):
        return str(self.value)


class Slice(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "slice"

    @typed_invokable(name="load_coins_", return_=Int)
    def coin(self) -> int:
        pass

    def uint(self, bits: int) -> int:
        return TypedInvokable("load_uint_", self, return_=int)(bits)


class Cont(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "cont"


class String(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "string"


class Cell(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "cell"


class Dict(Cell):
    @classmethod
    def type_name(cls) -> str:
        return "cell"


class Builder(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "builder"


class Tensor(Entity, tuple):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args)

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        data = kwargs.pop("data", None)
        super().__init__(data=data, name=name)


class Tuple(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "tuple"


Factory.register("Tensor", Tensor)
Factory.register("Tuple", Tuple)
Factory.register("Builder", Builder)
Factory.register("Dict", Dict)
Factory.register("Slice", Slice)
Factory.register("Cell", Cell)
Factory.register("String", String)
Factory.register("Cont", Cont)
Factory.register("Int", Int)
