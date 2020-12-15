from closure import make_average
import pytest


class TestClosure:
    def test_should_compute_average_with_higher_order_function(self):
        avg = make_average()

        avg1 = avg(1)
        assert avg1 == 1
        avg2 = avg(2)
        assert avg2 == 1.5
        avg3 = avg(3)
        assert avg3 == 2


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
