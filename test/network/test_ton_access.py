from pytest import fixture

from rift.network.account import AccountState
from rift.network.ton_access import endpoint
from rift.network.v2_network import Network


def test_access_nodes():
    print(endpoint())


@fixture
def network() -> Network:
    return Network(testnet=False)


def test_account_empty(network: Network):
    acc = network.get_account(
        "EQBwJZXLSnXL797oPrpIJBB7lV4kBhKbp2aphjaQ70thlRX3",
    )
    assert acc.state == AccountState.EMPTY
    assert acc.balance == 0


def test_account_active(network: Network):
    acc = network.get_account(
        "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
    )
    assert acc.state == AccountState.ACTIVE
    assert acc.balance > 0


def test_account_uninit(network: Network):
    acc = network.get_account(
        "EQD__________________________________________0vo",
    )
    assert acc.state == AccountState.UNINIT
    assert acc.balance > 0
