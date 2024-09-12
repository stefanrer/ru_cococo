import time


def timeit(timed_function):
    """
    Decorator for measuring function's running time.
    """
    def measure_time(*args, **kw):
        start_time = time.time()
        result = timed_function(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
              % (timed_function.__qualname__, time.time() - start_time))
        return result

    return measure_time
