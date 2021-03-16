import itertools
from array import array
from collections.abc import Iterable


class Vector:
    def __init__(self, components: Iterable):
        self._components = array('i', components)

    def __iter__(self):
        return iter(self._components)

    def __add__(self, other):
        pairs = itertools.zip_longest(self, other, fillvalue=0)
        return Vector(a + b for a, b in pairs)

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __len__(self):
        return len(self._components)
