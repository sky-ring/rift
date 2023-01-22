import asyncio
from pathlib import Path

from rift_tonlib import (
    ExternalMessageNotAccepted,
    LiteServerTimeout,
    TonlibClient,
    TonlibNoResponse,
)
from rift_tonlib.client import os

from rift.logging import log_info, log_panic, log_warn
from rift.network.account import Account
from rift.network.config import ConfigManager
from rift.network.servers import Servers
from rift.runtime.config import Config


class Network:
    def __init__(self, testnet=False, max_tries=5) -> None:
        self._network = "main" if not testnet else "test"
        self._max_tries = max_tries
        self._current = -1

        self._acquire_config()
        self._setup_ev()
        self.servers = Servers(network=self._network)
        self._try_connect()

    def _setup_ev(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def _acquire_config(self, invalidate=True):
        self._config = ConfigManager.acquire_config(self._network, invalidate)
        return self._config

    def _try_connect(self):
        tries = 0
        exclude_list = [self._current]
        while True:
            s = self.servers.select(exclude_list=exclude_list)
            log_info(
                "Network",
                "Selected server {server}, connecting ...",
                server=(s, "yellow"),
            )
            ok = self._connect_and_commit(s)
            if ok:
                log_info(
                    "Network",
                    "Successfully connected to server {server}!",
                    server=(s, "yellow"),
                )
                break
            else:
                log_warn(
                    "Network",
                    "Failure in connecting to server {server}!",
                    server=(s, "red"),
                )
                exclude_list.append(s)
            tries += 1
            if tries == self._max_tries:
                log_panic("Network", "Maximum connection retries reached!")

    def _try_do(self, cmd):
        tries = 0
        while True:
            try:
                future = cmd()
                r = self.loop.run_until_complete(future)
                return r
            except (TonlibNoResponse, LiteServerTimeout):
                log_warn(
                    "Network",
                    "Attempting server change due to timeout ...",
                )
                self.servers.punish(self._current)
                self._try_connect()
            tries += 1
            if tries == self._max_tries:
                log_panic("Network", "Maximum connection retries reached!")

    def _connect_and_commit(self, i, timeout=5):
        try:
            self._connect(i, timeout=timeout)
            self.servers.reward(i)
            self._current = i
            return True
        except Exception as e:
            raise e
            self.servers.punish(i)
            return False

    def _connect(self, i, timeout=5):
        keystore_dir = os.path.join(Config.dirs.user_data_dir, "keystore")
        Path(keystore_dir).mkdir(parents=True, exist_ok=True)
        self.client = TonlibClient(
            ls_index=i,
            config=self._config,
            keystore=keystore_dir,
            loop=self.loop,
            tonlib_timeout=timeout,
        )
        self.loop.run_until_complete(self.client.init())

    def get_account(self, address):
        data = self._try_do(
            lambda: self.client.raw_get_account_state(address),
        )
        return Account(raw_data=data, addr=address)

    def send_boc(self, boc: bytes):
        try:
            data = self._try_do(lambda: self.client.raw_send_message(boc))
            return {
                "ok": True,
                "data": data,
            }
        except ExternalMessageNotAccepted as e:
            return {
                "ok": False,
                "data": e.result,
            }

    def close(self):
        self.loop.run_until_complete(self.client.close())

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
