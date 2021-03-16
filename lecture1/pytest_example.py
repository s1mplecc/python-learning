import pytest


class TestClass:
    def test_1(self):
        assert 'h' in 'this'

    # will not be tested
    def second_test(self):
        assert 1 + 1 == 3


class TestClass2:
    def test_3(self):
        assert 1 + 1 == 2


class NotTestClass:
    # will not be tested
    def test_4(self):
        assert 1 + 1 == 2


# will be tested
def test_5():
    assert 1 + 1 == 2


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
