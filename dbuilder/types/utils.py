class Subscriptable(type):
    def __getitem__(cls, item):
        return cls.__build_type__(item)


class CachingSubscriptable(type):
    _build_cache = {}

    def __getitem__(cls, item):
        if item in cls._build_cache:
            return cls._build_cache[item]
        v = cls.__build_type__(item)
        cls._build_cache[item] = v
        return v
