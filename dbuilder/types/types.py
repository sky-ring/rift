from dbuilder.core import Entity


class Int(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "int"


class Slice(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "slice"


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
