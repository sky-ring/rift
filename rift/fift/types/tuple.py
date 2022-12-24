from rift.fift.types._fift_base import _FiftBaseType
from rift.fift.types.factory import Factory
from rift.fift.types.util import create_entry
from rift.util import type_id


class Tuple(_FiftBaseType):
    __type_id__ = type_id("Tuple")

    def __init__(self, __factory__: bool = False):
        if not __factory__:
            # NOTE: Although we can implement all behavior here just
            # by leveraging python's list, We stick to fift's tuple
            # primitives. Because currently we think it may run
            # additional checks, and this approach would be more
            # compatible. May change in future.
            t: Tuple = self.cmd("0 tuple")[0]
            self.value = t.value

    def __load_data__(self, value: list, *args, **kwargs):
        self.value = [
            Factory.load(item["type"], item.get("value", None))
            for item in value
        ]

    def __stack_entry__(self):
        return {
            "type": self.__type__(),
            "value": [create_entry(item) for item in self.value],
        }

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise RuntimeError("non int key")
        return self.cmd("[]", self, key)[0]

    def append(self, *items):
        for item in items:
            t: Tuple = self.cmd(",", self, item)[0]
            self.value = t.value

    @classmethod
    def __type__(cls) -> str:
        return "tuple"


Factory.register(Tuple.__type__(), Tuple)
