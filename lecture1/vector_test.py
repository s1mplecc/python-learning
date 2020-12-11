import pytest
from vector import Vector


class TestVector:
    def test_should_print_correctly(self):
        v1 = Vector()
        assert str(v1) == 'Vector(0)'

        v2 = Vector(1, 2)
        assert str(v2) == 'Vector(1, 2)'

        v3 = Vector(*(1, 2, 3))
        assert str(v3) == 'Vector(1, 2, 3)'

    def test_should_compare_two_vectors_with_operator(self):
        v1 = Vector(1, 2)
        v2 = Vector(1, 2)
        v3 = Vector(2, 3)

        assert v1 is not v2
        assert v1 == v2
        assert v1 != v3

    def test_should_add_two_vectors_with_add_operator(self):
        v1 = Vector(1, 2)
        v2 = Vector(1, 3)
        expected = Vector(2, 5)

        assert v1 + v2 == expected


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
