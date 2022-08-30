from dbuilder.ast.types import (
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
    _instance = None
    current_contract: Contract = None

    def __init__(self):
        if CallStacks._instance is not None:
            raise RuntimeError("This class is a singleton!")
        else:
            CallStacks._instance = self

    @staticmethod
    def get_instance() -> "CallStacks":
        if CallStacks._instance is None:
            CallStacks()
        return CallStacks._instance

    @staticmethod
    def declare_contract(name):
        CallStacks.current_contract = Contract(name)
        CallStacks.contracts[name] = CallStacks.current_contract

    @staticmethod
    def get_contract(name):
        return CallStacks.contracts[name]

    @staticmethod
    def declare_method(name, args, annotations):
        m = Method(name, args, annotations)
        CallStacks.current_contract.add_method(m)

    @staticmethod
    def declare_asm(name, args, annotations, asm_annoations):
        m = AsmMethod(name, args, annotations, asm_annoations)
        CallStacks.current_contract.add_method(m)

    @staticmethod
    def add_raw_statement(raw):
        CallStacks.current_contract.add_statement(raw)

    @staticmethod
    def add_statement(type, *args):
        s = Statement(type, args)
        CallStacks.current_contract.add_statement(s)
        return s.node_id()

    @staticmethod
    def return_(entity):
        CallStacks.add_statement(Statement.RETURN, entity)
        return entity

    @staticmethod
    def end_method(method):
        CallStacks.current_contract.end_method(method)

    @staticmethod
    def begin_if(cond):
        nif = IfFlow()
        nif.iff(cond)
        CallStacks.current_contract.add_statement(nif)
        return nif.node_id()

    @staticmethod
    def else_if(node_id, cond=None):
        nif: IfFlow = Node.find(node_id)
        if cond:
            nif.iff(cond)
        else:
            nif.else_()

    @staticmethod
    def end_if(node_id):
        nif: IfFlow = Node.find(node_id)
        CallStacks.current_contract.current_method.end_statement(nif)

    @staticmethod
    def begin_while(cond):
        nif = WhileLoop(cond)
        CallStacks.current_contract.add_statement(nif)
        return nif.node_id()

    @staticmethod
    def end_while(node_id):
        nif: WhileLoop = Node.find(node_id)
        CallStacks.current_contract.current_method.end_statement(nif)

    @staticmethod
    def call_(name, *args, operand=None):
        if operand:
            CallStacks.add_statement(
                Statement.METHOD_CALL,
                name,
                operand,
                *args,
            )
        else:
            CallStacks.add_statement(Statement.FUNC_CALL, name, *args)
