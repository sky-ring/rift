from dbuilder import method, method_id
from dbuilder.core.loop import while_
from dbuilder.func.contract import Contract
from dbuilder.library.std import Stdlib
from dbuilder.types import Slice

from .util import compile


class SimpleWallet(Contract):
    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        super(SimpleWallet, self).external_receive(
            in_msg,
        )
        signature = in_msg.load_bits_(512)
        cs = in_msg
        msg_seqno = cs.load_uint_(32)
        valid_until = cs.load_uint_(32)
        self.throw_if(35, valid_until <= self.now())
        ds = self.get_data().begin_parse()
        stored_seqno = ds.load_uint_(32)
        public_key = ds.load_uint_(256)
        ds.end_parse()
        self.throw_unless(33, msg_seqno == stored_seqno)
        self.throw_unless(
            34,
            self.check_signature(
                self.slice_hash(in_msg),
                signature,
                public_key,
            ),
        )
        self.accept_message()
        cs.touch_()
        with while_(cs.slice_refs()):
            mode = cs.load_uint_(8)
            self.send_raw_message(cs.load_ref_(), mode)
        cs.end_parse()
        self.set_data(
            self.begin_cell()
            .store_uint(stored_seqno + 1, 32)
            .store_uint(public_key, 256)
            .end_cell(),
        )

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
