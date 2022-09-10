class Subscriptable(type):
    def __getitem__(cls, item):
        return cls.__build_type__(item)


class CachingSubscriptable(type):
    _build_cache = {}

    def __getitem__(cls, item):
        if cls not in cls._build_cache:
            cls._build_cache[cls] = {}
        bc = cls._build_cache[cls]
        if item in bc:
            return bc[item]
        v = cls.__build_type__(item)
        bc[item] = v
        return v
