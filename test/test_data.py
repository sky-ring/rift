from dbuilder.func.contract import Contract
from dbuilder.types import Cell, Slice
from dbuilder.types.either import Either
from dbuilder.types.int_aliases import uint32, uint256
from dbuilder.types.maybe import Maybe
from dbuilder.types.model import Model
from dbuilder.types.payload import Payload
from dbuilder.types.ref import Ref

from .util import compile


class SimpleData(Contract):
    """Simple Data Contract."""

    class Data(Model):
        class KeyPair(Payload):
            pub: uint32
            priv: uint32

        seq_no: uint32
        public_key: uint256
        ref: Ref[Cell]
        key: Ref[KeyPair]
        maybe_cell: Maybe[Ref[Cell]]
        maybe_key: Maybe[KeyPair]
        some_either: Either[KeyPair, Ref[KeyPair]]

    data: Data

    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        self.data.load()
        self.data.maybe_key.pub = 1
        pub_k = self.data.key.pub
        self.data.save()


def test_compile():
    compile(SimpleData)
