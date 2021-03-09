import pytest
from collections.abc import Sequence
from collections.abc import Iterator


class Foo:
    def __getitem__(self, pos):
        return range(3)[pos]

    def __len__(self):
        return 3

    def __contains__(self, item): ...

    def __reversed__(self): ...


class Bar:
    def __iter__(self):
        pass

    def __next__(self):
        pass


class TestDuckType:
    def test_should_(self):
        assert isinstance(Bar(), Iterator)
        assert not isinstance(Foo(), Sequence)


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
