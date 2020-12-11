import pytest
from vector import Vector


class TestVector:
    # todo
    def test_should_add_two_vectors(self):
        v1 = Vector(1, 2)
        v2 = Vector(1, 3)
        result = Vector(2, 5)

        assert result == v1 + v2


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
