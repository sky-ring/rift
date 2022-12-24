from rift.fift.types.factory import Factory


def create_entry(item):
    if isinstance(item, int):
        item = Factory.acquire("int")(value=item)
    if isinstance(item, str):
        item = Factory.acquire("string")(__value__=item)
    if hasattr(item, "__stack_entry__"):
        return item.__stack_entry__()
    raise NotImplementedError(f"Type {type(item)} isn't supported!")
