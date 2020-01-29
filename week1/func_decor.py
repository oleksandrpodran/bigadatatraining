def smart_logger(method):
    def inner(*args):
        print('Function ', method.__name__)
        print(args)
        result = method(*args)
        return result
    return inner

@smart_logger
def func(*args):
    return 3 + len(args)

func(1,2,3,4)
