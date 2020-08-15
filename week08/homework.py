'''
list: container, mutable
tuple: container, immutable
str: flatten, immutable
dict: container, mutable
collections.deque: container, mutable
'''

import time
from typing import Callable, Iterable


def self_map(func: Callable, iterable: Iterable):
    kclazz = iterable.__class__
    container = kclazz()
    for item in iterable:
        container += kclazz([func(item)])
    return container


def timer(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(inner)
        end_time = time.time()
        duration = end_time - start_time
        print(duration)
        return result
    return inner


@timer
def run_func(*args, **kwargs):
    time.sleep(1)


if __name__ == "__main__":
    print(self_map(lambda x: x + 1, [1, 2, 3, 4, 5]))
    print(self_map(lambda x: x + 1, (1, 2, 3, 4, 5)))
    run_func()
