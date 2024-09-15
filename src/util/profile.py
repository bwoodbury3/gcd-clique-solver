"""
Recursive timing profiler
"""

from contextlib import contextmanager
from dataclasses import dataclass, field
import time


@dataclass
class ProfiledFunction:
    name: str
    """
    The name of this function
    """
    t: float
    """
    The time spent in this function
    """
    children: dict[str, "ProfiledFunction"] = field(default_factory=dict)
    """
    Recursive children of this function
    """


# Control
TIMER_ENABLED = False
ROOT_PROFILER = ProfiledFunction("ROOT", 0.0)
CUR_PROFILER = ROOT_PROFILER

# Text colors
GREEN = "\033[92m"
RESET = "\033[0m"


def enable():
    """
    Globally enable profiling.
    """
    global TIMER_ENABLED
    TIMER_ENABLED = True


def disable():
    """
    Globally disable profiling.
    """
    global TIMER_ENABLED
    TIMER_ENABLED = False


def is_enabled():
    """
    Whether profiling is enabled.
    """
    return TIMER_ENABLED


@contextmanager
def profile_context(name: str):
    """
    Profile a chunk of code as a context manager.

    Args:
        name: The name of the section of code to profile.
    """
    global CUR_PROFILER
    prev = CUR_PROFILER

    CUR_PROFILER = CUR_PROFILER.children.setdefault(name, ProfiledFunction(name, 0))

    t_start = time.monotonic()

    yield

    t_end = time.monotonic()
    CUR_PROFILER.t += t_end - t_start

    CUR_PROFILER = prev


def timer(name):
    """
    Timing profiler decorator.

    Args:
        name: The name of the function to profile.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            with profile_context(name):
                res = func(*args, **kwargs)
            return res

        return wrapper

    return decorator


def _print_profiler(profiler: ProfiledFunction, depth: int):
    """
    Recursively print a profiler
    """
    indent = depth * 2 * " "

    print(f"{indent}[{GREEN}{profiler.t:0.4f}s{RESET}] {profiler.name}")
    for _, profiler in profiler.children.items():
        _print_profiler(profiler, depth + 1)


def print_report():
    """
    Print the profiler report.
    """
    print("Algorithm profile:")
    for _, profiler in ROOT_PROFILER.children.items():
        _print_profiler(profiler, 0)
