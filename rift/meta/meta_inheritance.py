"""
Meta Class Conflict Fixer.

Thanks to:
https://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
"""
import inspect


def skip_redundant(iterable, skip_set=None):
    """Redundant items are repeated items or items in the original skip set."""
    if skip_set is None:
        skip_set = set()
    for item in iterable:
        if item not in skip_set:
            skip_set.add(item)
            yield item


def remove_redundant(meta_classes):
    skip_set = {type}
    for meta in meta_classes:  # determines the meta classes to be skipped
        skip_set.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(meta_classes, skip_set))


memoized_meta_classes_map = {}


def _get_non_conflicting_metaclass(bases, left_metas, right_metas):
    # make tuple of needed meta classes in specified priority order
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)

    # return existing conflict-solving meta, if any
    if needed_metas in memoized_meta_classes_map:
        return memoized_meta_classes_map[needed_metas]
    # nope: compute, memoize and return needed conflict-solving meta
    elif not needed_metas:  # wee, a trivial case, happy us
        meta = type
    elif len(needed_metas) == 1:  # another trivial case
        meta = needed_metas[0]
    # check for recursion, can happen i.e. for Zope ExtensionClasses
    elif needed_metas == bases:
        raise TypeError("Incompatible root meta types", needed_metas)
    else:  # gotta work ...
        meta_name = "_" + "".join([m.__name__ for m in needed_metas])
        meta = mix_metas()(meta_name, needed_metas, {})
    memoized_meta_classes_map[needed_metas] = meta
    return meta


def mix_metas(left_metas=(), right_metas=()):
    def make_class(name, bases, attrs):
        metaclass = _get_non_conflicting_metaclass(
            bases,
            left_metas,
            right_metas,
        )
        return metaclass(name, bases, attrs)

    return make_class
