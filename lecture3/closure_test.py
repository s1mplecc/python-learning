from closure import make_average
import pytest


class TestClosure:
    def test_should_compute_average_with_higher_order_function(self):
        # >>> avg = make_average()
        # >>> avg(1)
        # 1.0
        # >>> avg(2)
        # 1.5
        # >>> avg(3)
        # 2.0

        avg = make_average()

        avg1 = avg(1)
        assert avg1 == 1
        avg2 = avg(2)
        assert avg2 == 1.5
        avg3 = avg(3)
        assert avg3 == 2

    def test_should_find_bind_free_variables_in_closure_function(self):
        # >>> avg.__code__.co_freevars
        # ('series',)
        # >>> avg.__closure__
        # (<cell at 0x104301400: list object at 0x1041a9580>,)
        # >>> avg.__closure__[0].cell_contents
        # [1, 2, 3]

        avg = make_average()
        assert 'series' in avg.__code__.co_freevars

        avg(1)
        avg(2)
        assert avg.__closure__[0].cell_contents == [1, 2]


if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
