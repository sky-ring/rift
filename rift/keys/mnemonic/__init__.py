"""
Mnemonic implementation.

Notice: We borrow this code from https://github.com/tonfactory/tonsdk
It's not included as dependency because we won't use the other parts and it would make the codebase less flexible for future changes
"""

from rift.keys.mnemonic.exceptions import InvalidMnemonicsError
from rift.keys.mnemonic.keystore import (
    generate_keystore_key,
    generate_new_keystore,
)
from rift.keys.mnemonic.mnemonic import (
    mnemonic_is_valid,
    mnemonic_new,
    mnemonic_to_wallet_key,
)

__all__ = [
    "mnemonic_new",
    "mnemonic_to_wallet_key",
    "mnemonic_is_valid",
    "generate_new_keystore",
    "generate_keystore_key",
    "InvalidMnemonicsError",
]
