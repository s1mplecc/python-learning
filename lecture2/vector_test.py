from vector import Vector


class TestVector:
    def test_should_compare_two_vectors_with_override_compare_operators(self):
        v1 = Vector([1, 2])
        v2 = Vector((1, 2))
        v3 = Vector([2, 3])
        v4 = Vector([2, 3, 4])

        assert v1 == v2
        assert v3 != v2
        assert v4 != v3
        assert (1, 2) == v2
        assert v2 == [1, 2]

    def test_should_add_two_same_dimension_vectors_with_override_add_operator(self):
        v1 = Vector([1, 2])
        v2 = Vector((1, 3))
        result = Vector([2, 5])

        assert result == v1 + v2

    def test_should_add_two_different_dimension_vectors_with_override_add_operator(self):
        v1 = Vector([1, 2])
        v2 = Vector((1, 1, 1))
        result = Vector([2, 3, 1])

        assert result == v1 + v2

    def test_should_add_vector_and_iterable_with_override_add_operator(self):
        v1 = Vector([1, 2])

        assert v1 + (1, 1) == (2, 3)
        assert v1 + [1, 1, 1] == (2, 3, 1)

    def test_should_add_iterable_and_vector_with_override_radd_method(self):
        v1 = Vector([1, 2])

        assert (1, 1) + v1 == (2, 3)
        assert [1, 1, 1] + v1 == (2, 3, 1)
