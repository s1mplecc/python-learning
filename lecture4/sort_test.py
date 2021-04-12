import pytest


def sort(iterable, *, key=None, reverse=False):
    if key is not None and not callable(key):
        raise TypeError(f'{type(key)} object is not callable')

    _l = list(iterable)
    for i in range(len(_l)):
        for j in range(i):
            if key is None:
                if _l[j] > _l[i]:
                    _l[j], _l[i] = _l[i], _l[j]
            else:
                if key(_l[j]) > key(_l[i]):
                    _l[j], _l[i] = _l[i], _l[j]
    if reverse:
        _l.reverse()
    return _l


class TestFunction:
    def test_should_sort_number_sequence(self):
        _l = [1, 5, 3, 2, 7, 4]
        result = [1, 2, 3, 4, 5, 7]
        assert sort(_l) == result

    def test_should_sort_sequence_with_key_function(self):
        _l = ['a', 'aab', 'ab', 'aabb']
        result = ['a', 'ab', 'aab', 'aabb']
        assert sort(_l, key=len) == result

    def test_should_sort_sequence_with_key_function_and_reverse(self):
        _l = ['a', 'aab', 'ab', 'aabb']
        result = ['aabb', 'aab', 'ab', 'a']
        assert sort(_l, key=len, reverse=True) == result

    def test_should_raise_error_when_key_function_is_not_callable(self):
        _l = [1, 5, 3, 2, 7, 4]
        with pytest.raises(TypeError) as e:
            sort(_l, key=1)
