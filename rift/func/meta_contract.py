class ContractMeta(type):
    contracts = set()

    def __new__(mcs, name, bases, attrs):
        attrs["__refresh__"] = ContractMeta._refresh
        attrs["__restrain__"] = ContractMeta._restrain
        attrs["__refreshables__"] = {}
        attrs["__restrain_queue__"] = {}
        attrs["__fingerprint__"] = -1091
        if "Data" in attrs:
            if attrs["Data"].__magic__ == 0xBB10C0:
                d = attrs["Data"]()
                attrs["data"] = d
                attrs["__refreshables__"]["data"] = d
                attrs["__restrain_queue__"]["data"] = []
        c = super(ContractMeta, mcs).__new__(mcs, name, bases, attrs)
        if "__ignore__" not in attrs:
            ContractMeta.contracts.add(c)
        return c

    @staticmethod
    def _refresh(self, reset=False):
        for k, _v in self.__refreshables__.items():
            c_v = getattr(self, k)
            self.__restrain_queue__[k].append(c_v)
            setattr(self, k, c_v.copy(reset=reset))

    @staticmethod
    def _restrain(self):
        for k, _v in self.__refreshables__.items():
            n_v = self.__restrain_queue__[k].pop()
            setattr(self, k, n_v)

    @classmethod
    def defined_contracts(cls):
        contracts = filter(
            lambda x: x.__bases__ != (object,),
            cls.contracts,
        )
        return list(contracts)
