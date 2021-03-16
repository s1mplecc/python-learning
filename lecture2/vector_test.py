from vector import Vector


class TestVector:
    def test_should_add_two_vectors_with_override_add_operator(self):
        v1 = Vector([1, 2])
        v2 = Vector((1, 3))
        result = Vector([2, 5])

        assert result == v1 + v2
