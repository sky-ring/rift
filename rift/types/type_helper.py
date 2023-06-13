def safe_type(t):
    if hasattr(t, "__type__"):
        try:
            return t.__type__()
        except:
            return None
    return None


def type_matches(base, incoming):
    """
    This function checks whether incoming data type can match the base type or not.
    """
    if base.__type_id__() == incoming.__type_id__():
        return True
    i_ids = set(map(safe_type, incoming.__mro__))
    i_ids.remove(None)
    b_ids = set(map(safe_type, base.__mro__))
    b_ids.remove(None)
    # print("This is an unexpected case!")
    return False
