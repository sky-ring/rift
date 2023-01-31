from rift.library.std import std
from rift.types.int_aliases import uint256
from rift.types.payload import Payload
from rift.types.slice import Slice, slice


class SignedPayload(Payload):
    """
    This kind of payload assumes 512-bit signature at start of the data.

    [signature, signed-data]
    """

    def __init__(
        self, data_slice: Slice = None, name=None, lazy=True, **kwargs
    ):
        self.__annotations__ = {
            "__sig": slice[512],
            **self.__annotations__,
        }
        super().__init__(data_slice, name, lazy, **kwargs)
        self.__sig = getattr(self, "__sig")
        self.hash_ = self.__data__.hash().__assign__("_hash_x")

    def verify_signature(self, pub_key: uint256):
        return std.check_signature(
            self.hash_,
            self.__sig,
            pub_key,
        )
