import time
from enum import Enum


class TimeUnit(Enum):
    SECONDS = 's'
    MILL_SECONDS = 'ms'


class _Logger:
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        print(f'[INFO]: the function {self._func.__name__}() is running...')
        return self._func(*args, **kwargs)


class Logger:
    def __init__(self, level='INFO'):
        self._level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f'[{self._level}]: the function {func.__name__}() is running...')
            return func(*args, **kwargs)

        return wrapper


class Clock:
    def __init__(self, unit=TimeUnit.SECONDS):
        self._unit = unit

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            arg_str = ', '.join(repr(arg) for arg in args)
            if self._unit == TimeUnit.SECONDS:
                print(f'running {func.__name__}({arg_str}): {end - start}s')
            else:
                print(f'running {func.__name__}({arg_str}): {(end - start) * 1000}ms')
            return result

        return wrapper


@Clock()
def sleep(secs):
    time.sleep(secs)


@Clock(unit=TimeUnit.SECONDS)
def sleep_secs(secs):
    time.sleep(secs)


@Clock(unit=TimeUnit.MILL_SECONDS)
def sleep_ms(ms):
    time.sleep(ms / 1000)


if __name__ == '__main__':
    sleep(0.1)
    sleep_secs(1)
    sleep_ms(100)
