from rift.ast import CallStacks
from rift.ast.types import Expr, Node, Statement
from rift.core.factory import Factory
from rift.core.invokable import Invokable
from rift.core.mark import mark


class Entity(Node):
    __magic__ = 0x050794
    N_ID = 0

    def __init__(self, data=None, name=None) -> None:
        super().__init__()
        if data is None:
            data = {}
        self.data = data
        self.NAMED = False
        if name is not None:
            self.NAMED = True
            self.name = name
        Entity.N_ID += 1
        self.id = Entity.N_ID
        self.assigned = False
        self.has_expr = False
        self.__used__ = False

    def _binary(self, op, other, r=False):
        mark(self, other)
        e = Entity(
            Expr.binary_op(
                op,
                other if r else self,
                self if r else other,
                type(self),
            ),
        )
        return e

    def _unary(self, op):
        mark(self)
        e = Entity(Expr.unary_op(op, self, type(self)))
        return e

    def __eq__(self, other):
        return self._binary("==", other)

    def __neg__(self):
        return self._unary("-")

    def __ne__(self, other):
        return self._binary("!=", other)

    def __le__(self, other):
        return self._binary("<=", other)

    def __lt__(self, other):
        return self._binary("<", other)

    def __gt__(self, other):
        return self._binary(">", other)

    def __ge__(self, other):
        return self._binary(">=", other)

    def __add__(self, other):
        return self._binary("+", other)

    def __radd__(self, other):
        return self._binary("+", other, r=True)

    def __sub__(self, other):
        return self._binary("-", other)

    def __rsub__(self, other):
        return self._binary("-", other, r=True)

    def __truediv__(self, other):
        return self._binary("/", other)

    def __rtruediv__(self, other):
        return self._binary("/", other, r=True)

    def __mul__(self, other):
        return self._binary("*", other)

    def __rmul__(self, other):
        return self._binary("*", other, r=True)

    def __or__(self, other):
        return self._binary("|", other)

    def __ror__(self, other):
        return self._binary("|", other, r=True)

    def __and__(self, other):
        return self._binary("&", other)

    def __rand__(self, other):
        return self._binary("&", other, r=True)

    def __iadd__(self, other):
        x = self._binary("+", other)
        if self.NAMED:
            x.__assign__(self.name)
        return x

    def __isub__(self, other):
        x = self._binary("-", other)
        if self.NAMED:
            x.__assign__(self.name)
        return x

    def __imul__(self, other):
        x = self._binary("*", other)
        if self.NAMED:
            x.__assign__(self.name)
        return x

    def __idiv__(self, other):
        x = self._binary("/", other)
        if self.NAMED:
            x.__assign__(self.name)
        return x

    def __invert__(self):
        return self._unary("~")

    def __getattr__(self, item):
        mark(self)
        return Invokable(item, self)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.NAMED:
            return self.name
        return self._repr_()

    def _repr_(self):
        return repr(self.data)

    def __assign__(self, v):
        if self.NAMED:
            t = type(self)
            CallStacks.assign(v, Expr.variable(self.name, type_=t))
            return t.abstract_init(name=v)
        if self.has_expr:
            _x = getattr(self, "__expr")
            s: Statement = Node.find(_x)
            s.args = (v, s.args[0])
            s.type = Statement.ASSIGN
            s.refresh()
        else:
            # TODO: Most likely this never occurs (cleanup)
            CallStacks.assign(v, self.data)
        self.NAMED = True
        self.name = v
        return self

    def __massign__(self, vs, xs):
        if self.has_expr:
            _x = getattr(self, "__expr")
            s: Statement = Node.find(_x)
            if s.type == s.EXPR:
                s.args = (vs, s.args[0])
                s.type = Statement.M_ASSIGN
                s.refresh()
            else:
                CallStacks.multi_assign(vs, self.data)
        for x, v in zip(xs, vs):
            x.NAMED = True
            x.name = v

    def __prep_unpack__(self, l_):
        self._unpack_len = l_

    def __iter__(self):
        if hasattr(self, "__unpackable") and self.__unpackable:
            for _ in range(self._unpack_len):
                yield Entity()

    def __rem_name__(self):
        if self.NAMED:
            return self.name
        return None

    @classmethod
    def type_name(cls) -> str:
        return "var"

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> "Entity":
        return cls(*args, **kwargs)


Factory.register("Entity", Entity)
