class Factory:
    types = {}

    @classmethod
    def register(cls, name: str, creator_cls):
        cls.types[name] = creator_cls

    @classmethod
    def load(cls, name: str, *args, **kwargs):
        b = cls.types[name]()
        b.__load_data__(*args, **kwargs)
        return b
