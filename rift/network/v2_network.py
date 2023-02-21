import json
from urllib.parse import urlencode

import requests

from rift.network.account import Account, AccountState
from rift.network.inetwork import INetwork
from rift.network.ton_access import endpoint as get_endpoint


class Network(INetwork):
    def __init__(self, endpoint=None, testnet=False):
        if endpoint is None:
            endpoint = get_endpoint(testnet=testnet)
        if endpoint.endswith("/"):
            endpoint = endpoint[:-1]
        self.endpoint = endpoint

    def execute(self, method, query=None, **kwargs):
        if query is None:
            query = {}
        query = {**query, **kwargs}
        params = urlencode(query)
        full_url = f"{self.endpoint}/{method}?{params}"
        r = requests.get(full_url)
        if r.status_code != 200:
            # TODO: Better Exception maybe??
            raise Exception("Error in v2 retreive")
        d = json.loads(r.content)
        if not d["ok"]:
            # TODO: use "error" and "code" fields
            raise Exception("Error in v2 result")
        return d["result"]

    def send_boc(self, boc: bytes):
        pass

    def get_account(self, addr: str) -> Account:
        result = self.execute("getAddressInformation", address=addr)
        account = Account(addr=addr)
        match result["state"], balance := int(result["balance"]):
            case "active", _:
                account.state = AccountState.ACTIVE
                account.balance = balance
                account.code = result["code"]
                account.data = result["data"]
            case "uninitialized", 0:
                account.state = AccountState.EMPTY
                account.balance = balance
            case "uninitialized", _:
                account.state = AccountState.UNINIT
                account.balance = balance
        return account
