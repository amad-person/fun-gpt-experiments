import functools


def test_settings(n_times=10, verbose=False):
    def decorator_test_settings(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(n_times):
                func(verbose=verbose, *args, **kwargs)

        return wrapper

    return decorator_test_settings


def test_data(*decorator_args, **decorator_kwargs):
    def decorator_test_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data_list = [generator.generate() for generator in decorator_args]
            if "verbose" in kwargs and kwargs.get("verbose"):
                print(f"Testing with: {data_list}")
            func(*data_list)

        return wrapper

    return decorator_test_data
