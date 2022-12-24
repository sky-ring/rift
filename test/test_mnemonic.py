from rift.keys.key_pair import KeyPair
from rift.types import Cell


def test_mnemonic():
    mnemonic = [
        "romance",
        "edge",
        "twin",
        "avoid",
        "next",
        "opinion",
        "blur",
        "wish",
        "order",
        "number",
        "dad",
        "fog",
        "sock",
        "patient",
        "scissors",
        "gaze",
        "kite",
        "immune",
        "number",
        "bring",
        "truth",
        "rival",
        "tower",
        "resist",
    ]
    kp = KeyPair(mnemonic=mnemonic)
    x = kp.sign(Cell())
    print(len(x))
