import functools
import time

from django.db import connection, reset_queries


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries: int = len(connection.queries)

        start: float = time.perf_counter()
        result = func(*args, **kwargs)
        end: float = time.perf_counter()

        end_queries: int = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.5f}s")
        return result

    return inner_func
