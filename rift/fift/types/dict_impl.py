from rift.fift.types.gdict import GDict
from rift.fift.types.factory import Factory


class UDict(GDict):
    def generic_identifier(self):
        return "u"


class IDict(GDict):
    def generic_identifier(self):
        return "i"


Factory.register(IDict.__type__(), IDict)
Factory.register(UDict.__type__(), UDict)
