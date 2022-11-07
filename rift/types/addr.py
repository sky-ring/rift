from rift.core import Entity
from rift.library import std
from rift.runtime.config import Config
from rift.types.bases import Builder, Cell, Int, Slice, String
from rift.types.int_aliases import int8, integer, uint2, uint256
from rift.types.maybe import Maybe
from rift.types.payload import Payload


class MsgAddress(Slice):
    class Std(Payload):
        __tag__ = "$10"
        anycast: Maybe[Cell]
        workchain: int8
        address: uint256

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if isinstance(value, Int) or isinstance(value, integer):
            b = type(value).__serialize__(to, value)
        else:
            b = to.slice(value)
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
        # TODO: HANDLE INPLACE STUFF
        v = from_.addr_()
        if name is not None:
            v.__assign__(name)
        return v

    @classmethod
    def std(cls, workchain: int, addr: uint256) -> Slice:
        return (
            cls.Std(
                anycast=None,
                workchain=workchain,
                address=addr,
            )
            .as_cell()
            .parse()
        )

    @classmethod
    def human_readable(cls, addr: Slice, flags=0) -> str:
        # We assume this is an standard one
        # TODO: Copy stuff
        s = Slice(__value__=addr.value)
        s.uint_(3)
        wc = s.uint_(8)
        hash_ = s.uint_(256)
        hr: String
        (hr,) = s.cmd("smca>$", wc, hash_, flags)
        return hr.value

    @classmethod
    def empty(cls) -> Slice:
        if Config.mode.is_fift():
            b = Builder()
        else:
            b = std.begin_cell()
        b = b.uint(0, 2)
        return b.end().parse()
