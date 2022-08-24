from dbuilder.func.contract import Contract
from dbuilder.library.std import std
from dbuilder.types import Slice, Cell
from dbuilder.types.maybe import Maybe
from dbuilder.types.model import Model
from dbuilder.types.payload import Payload
from dbuilder.types.ref import Ref
from dbuilder.types.either import Either
from dbuilder.types.sized_int import SizedInt

from .util import compile


class SimpleData(Contract):
    """
    Simple Data Contract.
    """

    class Data(Model):
        class KeyPair(Payload):
            pub: SizedInt(32)
            priv: SizedInt(32)
        seq_no: SizedInt(32)
        public_key: SizedInt(256)
        ref: Ref(Cell)
        key: Ref(KeyPair)

    data: Data

    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        self.data.load()
        pub_k = self.data.key.pub
        self.data.save()


def test_compile():
    compile(SimpleData)
