import pytest


class TestClass:
    def test_one(self):
        assert 'h' in 'this'

    # will not be test
    def two_test(self):
        assert 1 + 1 == 3


class TestClass2:
    def test_three(self):
        assert 1 + 1 == 2


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
