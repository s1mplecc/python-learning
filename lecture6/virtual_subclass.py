import random
from abc import ABC, abstractmethod
from collections.abc import Sized


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        """Random draw an item."""

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Drawable:
            return 'draw' in dir(C)
        return NotImplemented


@Drawable.register
class Poker:
    def __init__(self):
        self.suits = ('Spade', 'Heart', 'Diamond', 'Club')
        self.numbers = (*range(2, 11), 'J', 'Q', 'K', 'A')

    def draw(self):
        suit = self.suits[random.randint(0, 3)]
        number = self.numbers[random.randint(0, 12)]
        return suit, number


class Capsule:
    def draw(self):
        ...


class TestVirtualSubclass:
    def test_should_bind_to_virtual_subclass_by_register(self):
        assert issubclass(Poker, Drawable)
        assert isinstance(Poker(), Drawable)

    def test_should_bind_to_virtual_subclass_by_subclasshook_method(self):
        assert issubclass(Capsule, Drawable)
        assert isinstance(Capsule(), Drawable)
