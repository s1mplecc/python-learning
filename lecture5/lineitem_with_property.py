import pytest


class LineItem:
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

    def total_price(self):
        return self.price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value >= 0:
            self._amount = value
        else:
            raise ValueError('amount must >= 0')


class TestLineItem:
    def test_should_access_attribute_with_property(self):
        item = LineItem(1.0, 5)
        assert item.amount == 5
        assert item.total_price() == 5.0
        assert '_amount' in item.__dict__
        assert 'amount' in LineItem.__dict__

    def test_should_raise_value_error_when_set_negative_value(self):
        with pytest.raises(ValueError) as e:
            LineItem(1.0, -1)
        item = LineItem(1.0, 5)
        with pytest.raises(ValueError) as e:
            item.amount = -1

    def test_should_set_negative_amount_directly_by_instance_dict(self):
        item = LineItem(1.0, 5)
        item.__dict__['_amount'] = -1
        assert item.amount == -1
