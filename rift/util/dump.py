# from abc import ABC, abstractmethod


class Dump:
    def dump(self, msg, **kwargs):
        p = " ".join(f"{k}:{v}" for k, v in kwargs.items())
        print(msg, p)
