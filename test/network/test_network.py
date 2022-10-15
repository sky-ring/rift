from pytest import fixture

from rift.network.account import AccountState
from rift.network.network import Network


@fixture
def network() -> Network:
    return Network(testnet=False)


def test_account_active(network: Network):
    with network:
        acc = network.get_account(
            "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
        )
        assert acc.state == AccountState.ACTIVE
        assert acc.balance > 0


def test_account_empty(network: Network):
    with network:
        acc = network.get_account(
            "EQBwJZXLSnXL797oPrpIJBB7lV4kBhKbp2aphjaQ70thlRX3",
        )
        assert acc.state == AccountState.EMPTY
        assert acc.balance == -1


def test_account_uninit(network: Network):
    with network:
        acc = network.get_account(
            "EQD__________________________________________0vo",
        )
        assert acc.state == AccountState.UNINIT
        assert acc.balance > 0


def test_deploy_account(network: Network):
    # We send a deploy message to active wallet,
    #  so we except it to reject the message
    # This way we can both validate send_boc works,
    #  and prevent any fees
    with network:
        boc = """B5EE9C724102030100010F0002DF88013CE88E9B96BDD5F256C4258B1461E37AB81E9A11EBFD2316FC8350DF9885F74A1191405F6754084AD36AA2C1B68106D2656CF957F270F7AF127BD78B6EB197BBE87890D5AC33548FE31583534DF60D8E493B840263053B2E20F82E683815E3F4A1600000001FFFFFFFE000000010010200DEFF0020DD2082014C97BA218201339CBAB19F71B0ED44D0D31FD31F31D70BFFE304E0A4F2608308D71820D31FD31FD31FF82313BBF263ED44D0D31FD31FD3FFD15132BAF2A15144BAF2A204F901541055F910F2A3F8009320D74A96D307D402FB00E8D101A4C8CB1FCB1FCBFFC9ED540050000000000000000070A2BA5BA31A4CE1905029D0CA07A193B69F3FF9259084561A9A2BFC209DAF47596784C8"""
        bb = bytes.fromhex(boc)
        res = network.send_boc(bb)
        assert not res["ok"]
        print(res["data"])
