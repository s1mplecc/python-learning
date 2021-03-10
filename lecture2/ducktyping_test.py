from collections.abc import Sequence
from collections.abc import Iterator


class SeqDuck:
    def __getitem__(self, pos):
        return range(3)[pos]

    def __len__(self):
        return 3


class IterDuck:
    def __iter__(self):
        return self

    def __next__(self):
        return 1


class TestDuckType:
    def test_should_treat_iter_duck_typing_as_iterator(self):
        assert isinstance(IterDuck(), Iterator)
        assert not isinstance(SeqDuck(), Sequence)

    def test_should_seq_duck_typing_support_iter_with_getitem_method(self):
        seq = SeqDuck()
        assert 2 in seq
        for i in seq:
            assert seq[i] == i
