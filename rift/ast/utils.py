from types import GenericAlias

DEBUG = False
type_map = {
    "Slice": "slice",
    "Int": "int",
    "Builder": "builder",
    "Cell": "cell",
}


def _type_name(type_):
    proxy = _type_name_p(type_)
    if proxy == "_" and isinstance(type_, str):
        proxy = type_map.get(type_, "_")
    if DEBUG:
        print(type_, proxy)
    return proxy


def _type_name_p(type_):
    if isinstance(type_, GenericAlias) and type_.__origin__ == tuple:
        types = map(_type_name, type_.__args__)
        names = ", ".join(types)
        n = "({names})".format(names=names)
        return n
    elif hasattr(type_, "type_name"):
        return type_.type_name()
    elif type_ is None:
        return "()"
    elif type_ == int:
        return "int"
    elif type_ == "var":
        return "var"
    return "_"
