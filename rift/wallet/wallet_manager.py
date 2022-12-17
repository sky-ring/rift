import json
import time
from os import path

from rift.fift.types.cell import Cell
from rift.network.network import Network
from rift.runtime.config import Config
from rift.types.msg import MessageFlag, MessageMode
from rift.wallet.wallet_base import WalletBase
from rift.wallet.wallet_v3_r2 import WalletV3R2


class WalletManager:
    wallets = {
        "v3r2": WalletV3R2,
    }

    @classmethod
    def send_message(
        cls,
        network: Network,
        message: Cell,
        valid_until: int = -1,
        mode: int = MessageFlag.FLAG_IGNORE_ACTION_ERR
        + MessageMode.CARRY_REM_VALUE,
    ) -> bool:
        wallet = cls.acquire_wallet(network)
        ok, account = wallet.connect()
        if not ok:
            print("Selected wallet address:", account.addr)
            if account.state == account.state.EMPTY:
                print(
                    "The wallet account is empty! Please send some TONs and proceed to deploying it.",
                )
                return
            elif account.state == account.state.UNINIT:
                print("Account is uninitialized, proceeding to deploy it ...")
                r = wallet.deploy_wallet()
                print(r)
                print("Waiting 15 seconds to be sure wallet is deployed!")
                time.sleep(15)
        return wallet.send_message(
            message,
            valid_until=valid_until,
            mode=mode,
        )

    @classmethod
    def acquire_wallet(cls, network: Network) -> WalletBase:
        w_f = path.join(Config.dirs.user_data_dir, ".wallet")
        if path.exists(w_f):
            with open(w_f, "r") as f:
                data: dict = json.loads(f.read())
        else:
            data = {}
        rev = data.get("revision", "v3r2")
        subwallet = data.get("subwallet", 2)
        wallet_cls = cls.wallets.get(rev, None)
        if wallet_cls is None:
            raise RuntimeError()
        wallet = wallet_cls(network, subwallet=subwallet)
        return wallet
