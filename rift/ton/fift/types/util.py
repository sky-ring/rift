def create_entry(item):
    if hasattr(item, "__stack_entry__"):
        return item.__stack_entry__()
    raise NotImplementedError()
