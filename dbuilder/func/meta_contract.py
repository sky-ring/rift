class ContractMeta(type):
    contracts = set()

    def __new__(mcs, name, bases, attrs):
        c = super(ContractMeta, mcs).__new__(mcs, name, bases, attrs)
        ContractMeta.contracts.add(c)
        return c
