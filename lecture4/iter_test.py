from collections.abc import Iterator, Iterable, Generator


class A:
    def __iter__(self): ...


class B:
    def __iter__(self): ...

    def __next__(self): ...


class C:
    def __iter__(self): ...

    def __next__(self): ...

    def send(self): ...

    def throw(self): ...

    def close(self): ...


class TestIter:
    def test_subclasshook_bind_virtual_subclass_with_magic_methods(self):
        assert issubclass(A, Iterable) and not issubclass(A, Iterator) and not issubclass(C, Generator)
        assert issubclass(B, Iterable) and issubclass(B, Iterator) and not issubclass(C, Generator)
        assert issubclass(C, Iterable) and issubclass(C, Iterator) and issubclass(C, Generator)
