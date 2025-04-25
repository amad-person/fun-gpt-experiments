import functools


def test_settings(n_times=10, verbose=False):
    def decorator_test_settings(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(n_times):
                func(verbose=verbose, *args, **kwargs)

        return wrapper

    return decorator_test_settings


def test_data(generator_func):
    def decorator_test_with(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = generator_func()
            if "verbose" in kwargs and kwargs.get("verbose"):
                print(f"Testing with: {data}")
            func(data)

        return wrapper

    return decorator_test_with
