from dbuilder import method, method_id
from dbuilder.core.loop import while_
from dbuilder.func.contract import Contract
from dbuilder.library.std import Stdlib
from dbuilder.types import Slice
from dbuilder.types.model import Model
from dbuilder.types.sized_int import SizedInt

from .util import compile


class SimpleWallet(Contract):
    class Data(Model):
        seq_no: SizedInt(32)
        public_key: SizedInt(256)

    data: Data

    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        super(SimpleWallet, self).external_receive(
            in_msg,
        )
        self.data.load()
        signature = in_msg.load_bits_(512)
        cs = in_msg
        msg_seqno = cs.load_uint_(32)
        valid_until = cs.load_uint_(32)
        self.throw_if(35, valid_until <= self.now())
        self.throw_unless(33, msg_seqno == self.data.seq_no)
        self.throw_unless(
            34,
            self.check_signature(
                self.slice_hash(in_msg),
                signature,
                self.data.public_key,
            ),
        )
        self.accept_message()
        cs.touch_()
        with while_(cs.slice_refs()):
            mode = cs.load_uint_(8)
            self.send_raw_message(cs.load_ref_(), mode)
        cs.end_parse()
        self.data.seq_no = self.data.seq_no + 1
        self.data.save()

    @method_id
    @method()
    def seqno(self) -> int:
        return self.get_data().begin_parse().preload_uint(32)

    @method_id
    @method()
    def get_public_key(self) -> int:
        cs = self.get_data().begin_parse()
        cs.load_uint_(32)
        return cs.preload_uint(256)


def test_compile():
    compile(SimpleWallet)
