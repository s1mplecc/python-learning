import time
from enum import Enum


class TimeUnit(Enum):
    SECONDS = 's'
    MILL_SECONDS = 'ms'


def clock(unit=TimeUnit.SECONDS):
    def decorate(func):
        def clocked(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            arg_str = ', '.join(repr(arg) for arg in args)
            if unit == TimeUnit.SECONDS:
                print(f'running {func.__name__}({arg_str}): {end - start}s')
            else:
                print(f'running {func.__name__}({arg_str}): {(end - start) * 1000}ms')
            return result

        return clocked

    return decorate


@clock()
def sleep(secs):
    time.sleep(secs)


@clock(unit=TimeUnit.SECONDS)
def sleep_secs(secs):
    time.sleep(secs)


@clock(unit=TimeUnit.MILL_SECONDS)
def sleep_ms(ms):
    time.sleep(ms / 1000)


if __name__ == '__main__':
    sleep(0.1)
    sleep_secs(1)
    sleep_ms(100)
