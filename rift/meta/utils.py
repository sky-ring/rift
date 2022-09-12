def caller_locals(back=1):
    """Returns the local variables in the caller's frame."""
    import inspect

    frame = inspect.currentframe()
    try:
        t_frame = frame
        while back != 0:
            t_frame = t_frame.f_back
            back -= 1
        return t_frame.f_locals
    finally:
        del frame
