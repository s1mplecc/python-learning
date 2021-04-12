def poker_order(item):
    seq = {str(i): i for i in range(2, 11)}
    seq.setdefault('J', 11)
    seq.setdefault('Q', 12)
    seq.setdefault('K', 13)
    seq.setdefault('A', 1)
    return seq.get(item)


class PokerOrder:
    def __init__(self):
        self._seq = {str(i): i for i in range(2, 11)}
        self._seq.setdefault('J', 11)
        self._seq.setdefault('Q', 12)
        self._seq.setdefault('K', 13)
        self._seq.setdefault('A', 1)

    def __call__(self, item):
        return self._seq.get(item)

    def show(self):
        print(self._seq)


class TestPokerSort:
    def test_should_sort_poker_with_key_function(self):
        result = sorted(['K', '3', 'A', '7', 'J'], key=poker_order)
        answer = ['A', '3', '7', 'J', 'K']
        assert answer == result

    def test_should_sort_poker_with_key_callable_class(self):
        pokerorder = PokerOrder()
        result = sorted(['K', '3', 'A', '7', 'J'], key=pokerorder)
        answer = ['A', '3', '7', 'J', 'K']

        assert pokerorder('A') == 1
        assert pokerorder('3') == 3
        assert pokerorder('K') == 13
        assert callable(pokerorder)
        assert answer == result
