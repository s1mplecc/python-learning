import pytest
from vector import Vector


class TestVector:
    def test_should_print_correctly(self):
        v1 = Vector()
        assert str(v1) == 'Vector(0)'

        v2 = Vector(1, 2)
        assert str(v2) == 'Vector(1, 2)'


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
