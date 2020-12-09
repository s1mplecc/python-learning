from functools import reduce


class Vector(object):
    def __init__(self, *args):
        self._coordinate = args if args else 0

    def __str__(self) -> str:
        s = reduce(lambda x, y: str(x) + ', ' + str(y), self._coordinate)
        return f'Vector({s})'


if __name__ == '__main__':
    v = Vector(1)
    v = Vector(1)
    v2 = Vector(1, 2)
    print(v2)
    print(v)
