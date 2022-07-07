# from dbuilder.invokable import Invokable
from dbuilder.calls import CallStacks


class Invokable:
    def __init__(self, name, entity):
        self.name = name
        self.entity = entity

    def __call__(self, *args, **kwargs):
        e = Entity({})
        CallStacks.add({
            "type": "METHOD_CALL",
            "operand": self.entity,
            "name": self.name,
            "args": args,
            "result": e,
        })
        return e


class Entity:
    N_ID = 0

    def __init__(self, data, name=None) -> None:
        super().__init__()
        self.data = data
        self.NAMED = False
        if name is not None:
            self.NAMED = True
            self.name = name
        Entity.N_ID += 1
        self.id = Entity.N_ID

    def __eq__(self, other):
        return Entity(
            {
                "type": "expr",
                "op": "==",
                "op1": self,
                "op2": other
            }
        )
        pass

    def __add__(self, other):
        e = Entity(
            {
                "type": "expr",
                "op": "+",
                "op1": self,
                "op2": other
            }
        )
        CallStacks.add({
            "type": "DEFINE_ENTITY",
            "entity": e,
            "value": {
                "type": "expr",
                "op": "+",
                "op1": self,
                "op2": other,
            }
        })
        return e

    def __radd__(self, other):
        e = Entity(
            {
                "type": "expr",
                "op": "+",
                "op1": other,
                "op2": self
            }
        )
        pass

    def __or__(self, other):
        return Entity(
            {
                "type": "expr",
                "op": "|",
                "op1": self,
                "op2": other
            }
        )
        pass

    def __ror__(self, other):
        return Entity(
            {
                "type": "expr",
                "op": "|",
                "op1": other,
                "op2": self
            }
        )
        pass

    def __invert__(self):
        return Entity(
            {
                "type": "expr",
                "op": "~",
                "op1": self
            }
        )
        pass

    def __getattr__(self, item):
        return Invokable(item, self)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.NAMED:
            return self.name
        return "e%d" % self.id

    def __assign__(self, v):
        print('called with %s' % v)