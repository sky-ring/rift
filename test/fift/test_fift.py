from rift.fift.fift import Fift


def check_end2end(code: str):
    f = Fift()
    s1 = f.eval(code)
    s2 = f.eval("", s1)
    for i1, i2 in zip(s1, s2):
        assert i1.__type__() == i2.__type__()
        assert i1.value == i2.value


def test_int():
    check_end2end("1")


def test_string():
    check_end2end('"Some Test String"')


def test_builder():
    check_end2end("<b 1 1 u,")


def test_cell():
    check_end2end("<b 1 1 u, b>")


def test_slice():
    check_end2end("<b 1 1 u, b> <s")


def test_bytes():
    check_end2end("<b 1 1 u, b> 2 boc+>B")


def test_fift_load():
    check_end2end("B{1234}")
