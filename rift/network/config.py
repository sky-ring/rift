import json
import os
from pathlib import Path

import requests

from rift.runtime.config import Config


class ConfigManager:
    @classmethod
    def acquire_config(cls, network="main", invalidate=True):
        config_url = {
            "main": "https://ton.org/global-config.json",
            "test": "https://ton.org/testnet-global.config.json",
        }[network]
        config_name = f"configs/{network}-config.json"
        ap = os.path.join(Config.dirs.user_data_dir, config_name)
        Path(ap).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(ap) or invalidate:
            # TODO: Wouldn't it be a good idea to invalidate
            # cache between some intervals automatically?!
            d = requests.get(config_url, timeout=5).content
            with open(ap, "wb") as f:
                f.write(d)
        with open(ap) as f:
            content = f.read()
        _config = json.loads(content)
        return _config
