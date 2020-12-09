from functools import reduce


class Vector(object):
    def __init__(self, *args):
        self._coordinate = args if args else (0,)  # using (0,) when only one item in tuple

    def __str__(self) -> str:
        s = reduce(lambda x, y: str(x) + ', ' + str(y), self._coordinate)
        return f'Vector({s})'
