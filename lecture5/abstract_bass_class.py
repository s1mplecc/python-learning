import abc
import pytest


class Sequence(abc.ABC):
    def __init__(self, iterable=None):
        if iterable:
            self._items = list(iterable)
        else:
            self._items = []

    @abc.abstractmethod
    def pop(self):
        """Remove and return item. Raises IndexError if sequence is empty."""

    @abc.abstractmethod
    def push(self, item):
        """Add item"""

    def inspect(self):
        return self._items


class Stack(Sequence):
    def pop(self):
        if not len(self._items):
            raise IndexError('Stack is empty.')
        return self._items.pop()

    def push(self, item):
        self._items.append(item)


class Queue(Sequence):
    def pop(self):
        if not len(self._items):
            raise IndexError('Queue is empty.')
        return self._items.pop(0)

    def push(self, item):
        self._items.append(item)


class TestAbstractBaseClass:
    def test_should_raise_typeerror_when_instantiate_abstract_class(self):
        with pytest.raises(TypeError) as e:
            seq = Sequence()
