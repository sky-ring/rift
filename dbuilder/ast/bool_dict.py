from collections.abc import MutableMapping


class BoolDict(MutableMapping):
    def __init__(self, default_=False, *args, **kwargs):
        self.store = {}
        self.default = default_
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def has(self, item):
        return item in self.store

    def __getitem__(self, key):
        if key not in self.store:
            return self.default
        return self.store[self._keytransform(key)]

    def __setitem__(self, key, value):
        self.store[self._keytransform(key)] = value

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def _keytransform(self, key):
        return key
