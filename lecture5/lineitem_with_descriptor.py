import pytest


class Quantity:
    def __init__(self, attribute):
        self.attribute = attribute

    def __set__(self, instance, value):
        if value >= 0:
            instance.__dict__[self.attribute] = value
        else:
            raise ValueError(f'{self.attribute} must >= 0')


class LineItem:
    price = Quantity('price')
    amount = Quantity('amount')

    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

    def total_price(self):
        return self.price * self.amount


class TestLineItem:
    def test_should_access_attribute_by_descriptor(self):
        item = LineItem(1.0, 5)
        assert item.price == 1.0
        assert item.amount == 5
        assert item.total_price() == 5.0
        assert 'amount' in item.__dict__ and 'price' in LineItem.__dict__
        assert 'amount' in LineItem.__dict__ and 'price' in LineItem.__dict__

    def test_should_raise_value_error_when_set_negative_value(self):
        item = LineItem(1.0, 5)
        with pytest.raises(ValueError) as e:
            item.price = -1
        with pytest.raises(ValueError) as e:
            item.amount = -1
