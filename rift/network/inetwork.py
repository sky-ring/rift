from abc import ABC, abstractmethod


class INetwork(ABC):
    @abstractmethod
    def send_boc(self):
        pass

    @abstractmethod
    def get_account(self):
        pass
