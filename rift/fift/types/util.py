from rift.fift.types.factory import Factory


def create_entry(item):
    if isinstance(item, int):
        item = Factory.acquire("int")(value=item)
    if hasattr(item, "__stack_entry__"):
        return item.__stack_entry__()
    raise NotImplementedError()
