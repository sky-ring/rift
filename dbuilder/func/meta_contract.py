class ContractMeta(type):
    contracts = set()

    def __new__(mcs, name, bases, attrs):
        attrs["__refresh__"] = ContractMeta._refresh
        attrs["__restrain__"] = ContractMeta._restrain
        attrs["__refreshables__"] = {}
        if "Data" in attrs:
            if attrs["Data"].__magic__ == 0xBB10C0:
                d = attrs["Data"]()
                attrs["data"] = d
                attrs["__refreshables__"]["data"] = d
        c = super(ContractMeta, mcs).__new__(mcs, name, bases, attrs)
        if "__ignore__" not in attrs:
            ContractMeta.contracts.add(c)
        return c

    @staticmethod
    def _refresh(self, reset=False):
        for k, v in self.__refreshables__.items():
            setattr(self, k, v.copy(reset=reset))

    @staticmethod
    def _restrain(self):
        for k, v in self.__refreshables__.items():
            setattr(self, k, v)
