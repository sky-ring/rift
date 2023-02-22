import base64 as b64
from urllib.parse import urlencode

import requests

from rift.network.account import Account, AccountState
from rift.network.error import NetworkError
from rift.network.inetwork import INetwork
from rift.network.ton_access import endpoint as get_endpoint


class Network(INetwork):
    def __init__(self, endpoint=None, testnet=False):
        if endpoint is None:
            endpoint = get_endpoint(testnet=testnet)
        if endpoint.endswith("/"):
            endpoint = endpoint[:-1]
        self.endpoint = endpoint

    def execute_get(self, method: str, query=None, **kwargs):
        if query is None:
            query = {}
        query = {**query, **kwargs}
        params = urlencode(query)
        full_url = f"{self.endpoint}/{method}?{params}"
        r = requests.get(full_url)
        d = r.json()
        if r.status_code != 200:
            raise NetworkError(d["code"], d["error"])
        return d["result"]

    def execute_post(self, method: str, body: dict):
        if body is None:
            body = {}
        full_url = f"{self.endpoint}/{method}"
        r = requests.post(full_url, json=body)
        d = r.json()
        if r.status_code != 200:
            raise NetworkError(d["code"], d["error"])
        return d["result"]

    def send_boc(self, boc: bytes):
        data = b64.b64encode(boc).decode("utf-8")
        r = self.execute_post("sendBoc", {"boc": data})
        return r

    def get_account(self, addr: str) -> Account:
        result = self.execute_get("getAddressInformation", address=addr)
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
