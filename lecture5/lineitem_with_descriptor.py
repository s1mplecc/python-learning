class Quantity:
    def __init__(self, attribute):
        self.attribute = attribute

    def __set__(self, instance, value):
        if value >= 0:
            instance.__dict__[self.attribute] = value
        else:
            raise ValueError('item amount must >= 0')


class LineItem:
    price = Quantity('price')
    amount = Quantity('amount')

    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

    def total_price(self):
        return self.price * self.amount


if __name__ == '__main__':
    item = LineItem(1.0, 5)
    print(item.amount)
