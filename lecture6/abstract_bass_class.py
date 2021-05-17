from abc import ABC, abstractmethod
import pytest


class Container(ABC):
    def __init__(self, iterable=None):
        if iterable:
            self._items = list(iterable)
        else:
            self._items = []

    @abstractmethod
    def pop(self):
        """Remove and return item. Raises IndexError if container is empty."""

    @abstractmethod
    def push(self, item):
        """Add item."""

    def inspect(self):
        return self._items


class Stack(Container):
    def pop(self):
        if not len(self._items):
            raise IndexError('Stack is empty.')
        return self._items.pop()

    def push(self, item):
        self._items.append(item)


class Queue(Container):
    def pop(self):
        if not len(self._items):
            raise IndexError('Queue is empty.')
        return self._items.pop(0)

    def push(self, item):
        self._items.append(item)


class TestAbstractBaseClass:
    def test_should_raise_typeerror_when_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            seq = Container()

    def test_should_raise_indexerror_when_pop_empty_container(self):
        with pytest.raises(IndexError):
            stack = Stack()
            stack.pop()
        with pytest.raises(IndexError):
            queue = Queue()
            queue.pop()

    def test_should_stack_first_in_last_out(self):
        stack = Stack([1, 2])
        stack.push(3)
        stack.push(4)
        assert stack.pop() == 4
        assert stack.inspect() == [1, 2, 3]

    def test_should_queue_first_in_first_out(self):
        queue = Queue([1, 2])
        queue.push(3)
        queue.push(4)
        assert queue.pop() == 1
        assert queue.inspect() == [2, 3, 4]
