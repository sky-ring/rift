class Factory:
    engines = {}

    @classmethod
    def register(cls, name: str, creator):
        cls.engines[name] = creator

    @classmethod
    def build(cls, name: str, *args, **kwargs):
        return cls.engines[name](*args, **kwargs)
