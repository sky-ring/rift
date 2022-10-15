from rift.fift.utils import calc_method_id


def test_method_id():
    x = calc_method_id("seqno")
    assert x == 85143
    x = calc_method_id("get_public_key")
    assert x == 78748
