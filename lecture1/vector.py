from functools import reduce


class Vector(object):
    def __init__(self, *args):
        self.coordinate = args if args else (0,)  # using (0,) when only one item in tuple

    def __str__(self) -> str:
        s = reduce(lambda x, y: str(x) + ', ' + str(y), self.coordinate)
        return f'Vector({s})'

    def __add__(self, other):
        if len(self.coordinate) != len(other.coordinate):
            return None
        result = [i + other.coordinate[index] for index, i in enumerate(self.coordinate)]
        return Vector(*result)  # '*' deconstruct the result list

    def __eq__(self, other) -> bool:
        if len(self.coordinate) != len(other.coordinate):
            return False
        for index, i in enumerate(self.coordinate):
            if i != other.coordinate[index]:
                return False
        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
