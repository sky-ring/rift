class ContractMeta(type):
    contracts = set()

    def __new__(mcs, name, bases, attrs):
        if "Data" in attrs:
            if attrs["Data"].__magic__ == 0xBB10C0:
                attrs["data"] = attrs["Data"]()
        c = super(ContractMeta, mcs).__new__(mcs, name, bases, attrs)
        ContractMeta.contracts.add(c)
        return c
