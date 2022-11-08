import hashlib
import hmac

from nacl.bindings import crypto_sign_seed_keypair

from rift.keys.mnemonic.bip39 import english
from rift.keys.mnemonic.settings import PBKDF_ITERATIONS
from rift.keys.mnemonic.utils import get_secure_random_number, is_basic_seed


def mnemonic_is_valid(mnemo_words: list[str]) -> bool:
    return len(mnemo_words) == 24 and is_basic_seed(
        mnemonic_to_entropy(mnemo_words),
    )


def mnemonic_to_entropy(mnemo_words: list[str], password: str | None = None):
    # TODO: implement password
    sign = hmac.new(
        (" ".join(mnemo_words)).encode("utf-8"),
        bytes(0),
        hashlib.sha512,
    ).digest()
    return sign


def mnemonic_to_seed(
    mnemo_words: list[str],
    seed: str,
    password: str | None = None,
):
    entropy = mnemonic_to_entropy(mnemo_words, password)
    return hashlib.pbkdf2_hmac("sha512", entropy, seed, PBKDF_ITERATIONS)


def mnemonic_to_private_key(
    mnemo_words: list[str],
    password: str | None = None,
) -> tuple[bytes, bytes]:
    """
    :rtype: (bytes(public_key), bytes(secret_key))
    """
    seed = mnemonic_to_seed(
        mnemo_words,
        "TON default seed".encode("utf-8"),
        password,
    )
    return crypto_sign_seed_keypair(seed[:32])


def mnemonic_to_wallet_key(
    mnemo_words: list[str],
    password: str | None = None,
) -> tuple[bytes, bytes]:
    """
    :rtype: (bytes(public_key), bytes(secret_key))
    """
    _, priv_k = mnemonic_to_private_key(mnemo_words, password)
    return crypto_sign_seed_keypair(priv_k[:32])


def mnemonic_new(
    words_count: int = 24,
    password: str | None = None,
) -> list[str]:
    while True:
        mnemo_arr = []

        for _ in range(words_count):
            idx = get_secure_random_number(0, len(english))
            mnemo_arr.append(english[idx])

        if not is_basic_seed(mnemonic_to_entropy(mnemo_arr)):
            continue

        break

    return mnemo_arr
