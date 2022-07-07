from dbuilder.entity import Entity


class Invokable:
    def __init__(self, name, entity):
        self.name = name
        self.entity = entity

    def __call__(self, *args, **kwargs):
        print("calling", self.name, "on", self.entity)
        return Entity({})
