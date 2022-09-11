from os import path
from pathlib import Path

bases = {"bare": "bare.py"}


def load_contract(name: str) -> str:
    p = Path(__file__)
    f = path.join(p.parent.absolute(), bases[name])
    fd = open(f, "r")
    v = fd.read()
    fd.close()
    return v


def write_contract(name: str, dst: str):
    c = load_contract(name)
    fd = open(dst, "w")
    fd.write(c)
    fd.close()
