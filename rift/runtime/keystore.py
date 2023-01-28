import base64
import json
import os
from hashlib import sha256
from os import path
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from rift.fift.types.builder import Builder
from rift.fift.types.bytes import Bytes
from rift.fift.types.cell import Cell
from rift.keys.key_pair import KeyPair
from rift.runtime.config import Config
from rift.types.payload import Payload


class KeyStore:
    _global_ks: "KeyStore" = None
    _key: Fernet
    secure: bool
    pair: KeyPair

    def __init__(self) -> None:
        pass

    @classmethod
    def initialize(cls):
        ks = cls._read_keystore()
        if ks is None:
            print("No keystore found!")
            print("Please select one of following options:")
            print("\t[1] Import your mnemonics")
            print("\t[2] Generate new mnemonics")
            print("\t[3] Import your 32-byte private key as a hex string")
            print("\t[4] Import your 32-byte private key as a base64 string")
            if Config.TEST:
                choice = 2
            else:
                choice = int(input(":"))
            if choice == 1:
                mnemonics = input(
                    "Please provide your mnemonics as a space separated string:",
                )
                kp = KeyPair(mnemonic=mnemonics)
            elif choice == 2:
                kp = KeyPair()
                print("Please save the following mnemonic for later imports!")
                print("!--- CAUTION: YOU WON'T BE ABLE TO GET IT LATER ---!")
                print("24 Secret Words:")
                print(" ".join(kp.mnem))
            elif choice == 3:
                pk = input(
                    "Please provide your 32-byte private key as a hex string:",
                )
                kp = KeyPair(priv_key=pk)
            elif choice == 4:
                pk = input(
                    "Please provide your 32-byte private key as a base64 string:",
                )
                kp = KeyPair(priv_key=pk, encoding="base64")
            else:
                raise RuntimeError("Invalid choice! Valid range [1-4]")
            if Config.TEST:
                secure = False
            else:
                secure = input(
                    "Would you like to secure keystore with custom password (we'll ask on every run)? [Y/n]: ",
                )
                secure = secure.lower() == "y"
            if secure:
                pass_ = input("Please input a memorable password: ")
            else:
                pass_ = None
            ks = KeyStore()
            ks._key = cls._fernet_key(pass_)
            ks.pair = kp
            ks.secure = secure
            if not Config.TEST:
                cls._write_keystore(ks)
                print("Configuration done successfully!")
        cls._global_ks = ks

    @classmethod
    def _read_keystore(cls):
        ks_f = path.join(Config.dirs.user_data_dir, "keys/.keystore")
        if path.exists(ks_f):
            with open(ks_f, "r") as f:
                data = json.loads(f.read())
            if data["sc"]:
                pass_ = input("Please provide your keystore password:")
            else:
                pass_ = None
            ks = KeyStore()
            ks._key = cls._fernet_key(pass_)
            pk = bytes.fromhex(data["pk"])
            pk = ks._key.decrypt(pk)
            ks.pair = KeyPair(priv_key=pk.hex())
            return ks
        return None

    @classmethod
    def _write_keystore(cls, ks: "KeyStore"):
        d = {
            "sc": ks.secure,
            "pk": ks._key.encrypt(bytes(ks.pair.priv_key)).hex(),
        }
        ks_f = path.join(Config.dirs.user_data_dir, "keys/.keystore")
        os.makedirs(path.dirname(ks_f), exist_ok=True)
        with open(ks_f, "w") as f:
            data = json.dumps(d, indent=4)
            f.write(data)

    @classmethod
    def _fernet_key(cls, password: str = None):
        if password is None:
            password = "rift-key-store!"
        password = password.encode("utf-8")
        salt = sha256(password).digest()[:16]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        return f

    @classmethod
    def sign(
        cls,
        data: Union["Bytes", "Cell", "Payload"],
        hash_bytes=False,
    ) -> "Bytes":
        if not cls._global_ks:
            cls.initialize()
        return cls._global_ks.pair.sign(data, hash_bytes)

    @classmethod
    def sign_pack(
        cls,
        data: Union["Bytes", "Cell", "Payload"],
        hash_bytes=False,
    ) -> "Cell":
        sig = cls.sign(data, hash_bytes=hash_bytes)
        b = Builder()
        b.call_("B,", sig)
        if isinstance(data, Bytes):
            b.call_("B,", data)
        elif isinstance(data, Payload):
            b = b.builder(data.as_builder())
        elif isinstance(data, Cell):
            b = b.slice(data.parse())
        return b.end()

    @classmethod
    def public_key(cls, bytes_=False) -> int:
        if not cls._global_ks:
            cls.initialize()
        if bytes_:
            return cls._global_ks.pair.pub_key
        return cls._global_ks.pair.pub_key.call("B>u@", 256)[0]
