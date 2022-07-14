from dbuilder.ast import Node, Expr, Statement
from dbuilder.func import CallStacks


class Invokable:
    def __init__(self, name, entity):
        self.name = name
        self.entity = entity

    def __call__(self, *args, **kwargs):
        e = Entity(
            Expr.call_expr(self.entity, self.name, *args)
        )
        setattr(e, "__expr", CallStacks.add_statement(Statement.EXPR, e.data))
        e.has_expr = True
        return e


class Entity(Node):
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
        self.assigned = False
        self.has_expr = False

    def __eq__(self, other):
        return Entity(
            Expr.binary_op("==", self, other)
        )

    def __add__(self, other):
        return Entity(
            Expr.binary_op("+", self, other)
        )

    def __radd__(self, other):
        return Entity(
            Expr.binary_op("+", other, self)
        )

    def __or__(self, other):
        return Entity(
            Expr.binary_op("|", self, other)
        )

    def __ror__(self, other):
        return Entity(
            Expr.binary_op("|", other, self)
        )

    def __invert__(self):
        return Entity(
            Expr.unary_op("~", self)
        )

    def __getattr__(self, item):
        return Invokable(item, self)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.NAMED:
            return self.name
        return repr(self.data)

    def __assign__(self, v):
        if self.has_expr:
            _x = getattr(self, "__expr")
            s: Statement = Node.find(_x)
            s.args = (v, s.args[0])
            s.type = Statement.ASSIGN
        else:
            CallStacks.add_statement(Statement.ASSIGN, v, self.data)
        self.NAMED = True
        self.name = v