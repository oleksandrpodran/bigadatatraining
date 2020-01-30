def smart_logger(method):
    def inner(*args, **kwargs):
        print('you called ', method.__name__, args, kwargs)
        result = method(*args, **kwargs)
        print('it returned ', result)
        return result
    return inner

@smart_logger
def func(*args):
    return 3 + len(args)

func(1,2,3,4)

