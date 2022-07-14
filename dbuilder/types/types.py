from dbuilder import Entity


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


class Tuple(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "tuple"
