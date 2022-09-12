from rift.ast.ref_table import ReferenceTable
from rift.ast.types import (
    AsmMethod,
    Contract,
    IfFlow,
    Method,
    Node,
    Statement,
    WhileLoop,
)


class CallStacks(object):
    """Class responsible for tracking the calls."""

    contracts = {}
    current_contract: Contract = None
    current_contract_name: str = None

    @classmethod
    def declare_contract(cls, name):
        cls.current_contract = Contract(name)
        cls.current_contract_name = name
        cls.contracts[name] = cls.current_contract

    @classmethod
    def get_contract(cls, name):
        return cls.contracts[name]

    @classmethod
    def declare_method(cls, name, args, annotations):
        m = Method(name, args, annotations)
        scope = f"{cls.current_contract_name}_{name}"
        ReferenceTable.init_scope(scope)
        cls.current_contract.add_method(m)

    @classmethod
    def declare_asm(cls, name, args, annotations, asm_annoations):
        m = AsmMethod(name, args, annotations, asm_annoations)
        cls.current_contract.add_method(m)

    @classmethod
    def add_raw_statement(cls, raw):
        cls.current_contract.add_statement(raw)

    @classmethod
    def add_statement(cls, type, *args):
        s = Statement(type, args)
        s._scope = ReferenceTable.current_scope
        cls.current_contract.add_statement(s)
        return s.node_id()

    @classmethod
    def return_(cls, entity):
        ReferenceTable.mark(entity)
        cls.add_statement(Statement.RETURN, entity)
        return entity

    @classmethod
    def end_method(cls, method):
        cls.current_contract.end_method(method)

    @classmethod
    def begin_if(cls, cond):
        ReferenceTable.mark(cond)
        nif = IfFlow()
        cls.current_contract.add_statement(nif)
        nif.iff(cond)
        return nif.node_id()

    @classmethod
    def else_if(cls, node_id, cond=None):
        ReferenceTable.mark(cond)
        nif: IfFlow = Node.find(node_id)
        if cond:
            nif.iff(cond)
        else:
            nif.else_()

    @classmethod
    def end_if(cls, node_id):
        nif: IfFlow = Node.find(node_id)
        cls.current_contract.current_method.end_statement(nif)

    @classmethod
    def begin_while(cls, cond):
        ReferenceTable.mark(cond)
        nif = WhileLoop(cond)
        cls.current_contract.add_statement(nif)
        return nif.node_id()

    @classmethod
    def end_while(cls, node_id):
        nif: WhileLoop = Node.find(node_id)
        cls.current_contract.current_method.end_statement(nif)

    @classmethod
    def assign(cls, name, value):
        return cls.add_statement(Statement.ASSIGN, name, value)

    @classmethod
    def multi_assign(cls, names, values):
        return cls.add_statement(Statement.M_ASSIGN, names, values)

    @classmethod
    def expression(cls, expr):
        return cls.add_statement(Statement.EXPR, expr)

    @classmethod
    def call_(cls, name, *args, operand=None):
        ReferenceTable.mark(*args)
        if operand:
            cls.add_statement(
                Statement.METHOD_CALL,
                name,
                operand,
                *args,
            )
        else:
            cls.add_statement(Statement.FUNC_CALL, name, *args)
