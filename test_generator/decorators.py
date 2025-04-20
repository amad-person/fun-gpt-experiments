import functools


def decorator_with_arguments(decorator_func):
    @functools.wraps(decorator_func)
    def decorator_maker(*args, **kwargs):
        def decorator(func):
            return decorator_func(func, *args, **kwargs)

        return decorator

    return decorator_maker


@decorator_with_arguments
def test_with(func, generator_func, n_times=10):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(n_times):
            test_data = generator_func()
            func(test_data)

    return wrapper
