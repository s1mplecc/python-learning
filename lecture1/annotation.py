from typing import List, ClassVar, Dict

primes: List[int] = []


def foo(a: 'int > 0', b: 5 + 6, c: list) -> max(2, 9):
    return max(2, 9)


def signal(flag: bool) -> str:
    color: str  # Note: no initial value!
    if flag:
        color = 'green'
    else:
        color = 'red'
    return color


class Starship:
    captain: str = 'Picard'  # instance variable
    stats: ClassVar[Dict[str, int]] = {}  # class variable


if __name__ == '__main__':
    for method in dir(signal.__code__):
        if 'co_' in method:
            s = repr(signal.__code__.__getattribute__(method))
            print(repr(method), ':', s)
