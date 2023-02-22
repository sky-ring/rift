import json
import os
from hashlib import sha256

from rift.network.config import ConfigManager
from rift.network.util import sample_without_replacement
from rift.runtime.config import Config


class Servers:
    def __init__(self, network="main", path=None) -> None:
        self._network = network
        self._path = path
        self._load_data()
        self._reconfigure()

    def _load_data(self):
        if self._path is None:
            self._path = os.path.join(
                Config.dirs.user_data_dir,
                f"{self._network}-servers.json",
            )
        self.config = ConfigManager.acquire_config(self._network)
        if os.path.exists(self._path):
            with open(self._path, "r") as f:
                self.data = json.loads(f.read())
        else:
            self.data = {
                "config_hash": "",
                "servers": {},
            }

    def _reconfigure(self):
        # TODO: pop-out removed servers
        d = json.dumps(self.config, sort_keys=True)
        hash_ = sha256(d.encode("utf-8")).hexdigest()
        prev_hash = self.data["config_hash"]
        if prev_hash == hash_:
            return
        self.data["config_hash"] = hash_
        servers = self.data["servers"]
        for i, server in enumerate(self.config["liteservers"]):
            id_ = server["id"]["key"]
            if id_ in servers:
                servers[id_]["ls_index"] = i
            else:
                servers[id_] = {
                    "ls_index": i,
                    "weight": 1,
                }
        self._persist()

    def _persist(self):
        d = json.dumps(self.data, sort_keys=True)
        with open(self._path, "w") as f:
            f.write(d)

    def select(self, exclude_list=None) -> int:
        servers: dict = self.data["servers"]
        if exclude_list is not None:
            servers = dict(
                filter(
                    lambda x: x[1]["ls_index"] not in exclude_list,
                    servers.items(),
                ),
            )
        weights = [s["weight"] for s in servers.values()]
        srv = sample_without_replacement(
            list(servers.keys()),
            weights=weights,
        )
        return servers[srv]["ls_index"]

    def reward(self, ls_index):
        self.adjust(ls_index, success=True)

    def punish(self, ls_index):
        self.adjust(ls_index, success=False)

    def adjust(self, ls_index, success=False):
        servers: dict = self.data["servers"]
        server_id = None
        for s_id, s in servers.items():
            if s["ls_index"] == ls_index:
                server_id = s_id
                break
        if server_id is None:
            raise RuntimeError("Invalid ls_index provided!")
        w = servers[server_id]["weight"]
        if success:
            w += 1
        else:
            w *= 0.7
        servers[server_id]["weight"] = w
        self._persist()
