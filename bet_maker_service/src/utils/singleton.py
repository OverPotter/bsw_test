from functools import wraps


def singleton(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not wrapped.__result:
            wrapped.__result = func(*args, **kwargs)
        return wrapped.__result

    wrapped.__result = None
    return wrapped
