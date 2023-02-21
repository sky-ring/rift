from pytest import fixture

from rift.fift.tvm import TVM, TVMResult
from rift.network.v2_network import Network


@fixture
def network() -> Network:
    return Network(testnet=False)


def test_tvm(network: Network):
    a = network.get_account(
        "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
    )
    r = TVM.get_method(a.code, a.data, "get_public_key")
    assert isinstance(r, TVMResult)
    (pub_key,) = r.stack
    assert (
        pub_key
        == 51920439607500563943260473395437779465153568561322824062990259298408252367615
    )
