import itertools
from functools import reduce


class Vector(object):
    def __init__(self, *args):
        self.coordinate = args if args else (0,)  # using (0,) when only one item in tuple

    def __str__(self) -> str:
        s = reduce(lambda x, y: str(x) + ', ' + str(y), self.coordinate)
        return f'Vector({s})'

    # todo
    def __iter__(self):
        return iter(self.coordinate)

    # todo
    def __add__(self, other):
        pairs = itertools.zip_longest(self, other, fillvalue=0)
        in_pairs = (a + b for a, b in pairs)
        print(in_pairs)
        return Vector(in_pairs)

    def __eq__(self, other) -> bool:
        if len(self.coordinate) != len(other.coordinate):
            return False
        for index, i in enumerate(self.coordinate):
            if i != other.coordinate[index]:
                return False
        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
