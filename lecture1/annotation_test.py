import pytest
from annotation import foo


class TestAnnotation:
    def test_foo_annotations(self):
        assert foo(1, 2, [1]) == 9
        assert repr(foo.__annotations__) == '''{'a': 'int > 0', 'b': 11, 'c': <class 'list'>, 'return': 9}'''


if __name__ == '__main__':
    pytest.main(['-p', 'no:cacheprovider'])
