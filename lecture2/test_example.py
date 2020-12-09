import pytest


class TestClass:
    def test_one(self):
        assert 'h' in 'this'

    def test_two(self):
        x = {'check': 's'}
        assert hasattr(x, 'check')


class TestClass2:
    def test_three(self):
        assert 1 + 1 == 3


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
