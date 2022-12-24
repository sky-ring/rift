def cls_hierarchy(cls):
    h = [cls]
    bases = cls.__bases__
    if bases == (object,):
        return h
    for b in bases:
        h += cls_hierarchy(b)
    return h


def cls_attrs(cls):
    h = cls_hierarchy(cls)
    d = {}
    for c in h:
        d = {**d, **c.__dict__}
    return d
