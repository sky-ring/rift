import secrets

from rift.fift.fift import Fift
from rift.fift.types import Bytes, Cell
from rift.keys.mnemonic import (
    InvalidMnemonicsError,
    mnemonic_is_valid,
    mnemonic_new,
    mnemonic_to_wallet_key,
)
from rift.types.payload import Payload


class KeyPair:
    def __init__(
        self,
        priv_key: str = None,
        mnemonic: str | list[str] = None,
        encoding: str = "hex",
    ) -> None:
        if priv_key is not None:
            self.priv_key = Bytes(__value__=priv_key, encoding=encoding)
            if len(self.priv_key) != 32:
                raise RuntimeError("Invalid key provided, not 32-bytes")
            self.pub_key = self.priv_key.cmd("priv>pub", self.priv_key)[0]
        elif mnemonic is not None:
            if isinstance(mnemonic, str):
                mnemonic = mnemonic.split(" ")
            if not mnemonic_is_valid(mnemonic):
                raise InvalidMnemonicsError()
            pub, priv = mnemonic_to_wallet_key(mnemonic)
            self.priv_key = Bytes(__value__=priv[:32])
            self.pub_key = Bytes(__value__=pub)
        else:
            # Nothing provided? Let's generate
            mnemonics = mnemonic_new()
            if not mnemonic_is_valid(mnemonics):
                raise InvalidMnemonicsError()
            pub, priv = mnemonic_to_wallet_key(mnemonics)
            self.priv_key = Bytes(__value__=priv[:32])
            self.pub_key = Bytes(__value__=pub)
            self.mnem = mnemonics

    def sign(self, data: Bytes | Cell | Payload, hash_bytes=False) -> Bytes:
        if isinstance(data, Payload):
            data = data.as_cell()
        if isinstance(data, Cell):
            hash_ = data.hashB()
        elif isinstance(data, Bytes):
            if hash_bytes:
                hash_ = data.hashB()
            else:
                hash_ = data
        (signature,) = Fift.exec("ed25519_sign", hash_, self.priv_key)
        return signature
