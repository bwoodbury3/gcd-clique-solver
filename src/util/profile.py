"""
Profiling tools
"""

import time


def timer(func):
    """
    Timing profiler decorator.
    """

    def wrapper(*args, profile=False, **kwargs):
        t_start = time.monotonic()
        res = func(*args, **kwargs)
        t_end = time.monotonic()

        if profile:
            print(f"timer({func})={t_end - t_start:.02}")

        return res

    return wrapper
