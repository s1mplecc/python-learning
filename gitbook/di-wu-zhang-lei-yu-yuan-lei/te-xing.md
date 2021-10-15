# 特性

在 Java 中，为了控制属性的访问权限，一般会将属性设置为私有属性，并为可以公开的属性设置公有的 getter 和 setter 方法。这样做还有一个好处，可以在方法内添加对属性的验证，比如保证商品的数量不会是负数。如果想更进一步，可以按照领域驱动设计的理念，可以将属性设置为实体类 Entity，在类中对属性进行校验。这两种思想在 Python 中也都有对应的实现，前一种对应于特性，后一种对应于描述符。

特性经常用于把公开的属性变成使用读值方法和设置方法管理的属性，且在不影响客户端代码的前提下实施业务规则。使用 `get/set + 属性名` 的命名方式不符合 Python 一贯的简约作风，为此 Python 提供了特性，即 property。property 是一个类形式的函数装饰器，本质上它是一个**描述符类**（实现了描述符协议）。

```python
class property(object):
    def __init__(
        self,
        fget: Optional[Callable[[Any], Any]] = ...,
        fset: Optional[Callable[[Any, Any], None]] = ...,
        fdel: Optional[Callable[[Any], None]] = ...,
        doc: Optional[str] = ...,
    ) -> None: ...
    def getter(self, fget: Callable[[Any], Any]) -> property: ...
    def setter(self, fset: Callable[[Any, Any], None]) -> property: ...
    def deleter(self, fdel: Callable[[Any], None]) -> property: ...
    def __get__(self, obj: Any, type: Optional[type] = ...) -> Any: ...
    def __set__(self, obj: Any, value: Any) -> None: ...
    def __delete__(self, obj: Any) -> None: ...
    def fget(self) -> Any: ...
    def fset(self, value: Any) -> None: ...
    def fdel(self) -> None: ...
```

使用函数形式的装饰器会返回一个嵌套的高阶函数，类形式的装饰器也类似，使用 `@property` 装饰的方法会被包装成特性类。特性类具有 getter、setter 和 deleter 方法属性，这三个属性也都返回 property 对象。

因此，用 `@property` 装饰的读值方法，如下的 `amount(self)` 方法，相当于返回一个 `property(amount)` 特性对象，将读值方法作为初始化参数 fget 传入。而后可以使用 `@amount.setter` 装饰设值方法，此时设值方法 amount 返回的是特性对象，setter 是它的方法属性。相当于 `property(amount).setter(amount)`，第二个 amount 是设值方法，将设值方法作为 fset 参数传入 setter 方法。也因此，`@amount.setter` 必须要定义在被 `@property` 装饰的设置方法之后。如下所示：

```python
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
            raise ValueError('item amount must >= 0')
```

读值方法可以不与实例属性名一致，但要保证，读值方法名称、设值方法名称和 `@amount.setter` 装饰器中的名称三者保持一致，即都为 amount。这样，在访问属性时可以通过 `item.amount` 的形式对真正的实例属性 `self._amount` 进行读值和赋值。其实，初始化函数中的 `self.amount = amount` 语句就已经在使用特性的设置方法了。

```python
>>> item = LineItem(1.0, 5)
>>> item.__dict__
{'price': 1.0, '_amount': 5}
>>> item.total_price()
5.0
>>> item.amount = 3
>>> item.total_price()
3.0
>>> item.amount = -1
Traceback (most recent call last):
  ...
ValueError: item amount must >= 0
```

可以看到，真正被操作的实例属性 `_amount` 被保存在实例字典中。

任何对 `item.amount` 的读值和设值操作，都会经过由特性包装的读值和设值方法进行处理。由于在设值方法中对属性值做了非负验证，所以将其设置为负值会抛出 ValueError 异常。

需要注意的是，特性是类属性，被保存于类的 `__dict__` 字典中。在使用 `obj.attr` 这样的表达式时，不会从 obj 开始查询 attr 属性，而是从实例所属的类，即 `obj.__class__` 开始，仅当类中没有名为 attr 的特性时，才会去查询实例字典。也就是说，**特性的读值和设值方法要优先于实例字典**，只有直接存取 `__dict__` 属性才能跳过特性的处理逻辑。

```python
>>> LineItem.__dict__
mappingproxy({'__module__': 'attribute', 
              '__init__': <function LineItem.__init__ at 0x105459a60>, 
              'total_price': <function LineItem.total_price at 0x105459af0>, 
              'amount': <property object at 0x105487680>, 
              '__dict__': <attribute '__dict__' of 'LineItem' objects>, 
              '__weakref__': <attribute '__weakref__' of 'LineItem' objects>, 
              '__doc__': None})
>>> item = LineItem(1.0, 5)
>>> item.__dict__
{'price': 1.0, '_amount': 5}
>>> item.__dict__['_amount'] = -1
>>> item.amount
-1
```

这条规则不仅适用于特性，还适用于数据描述符，其实，特性也是数据描述符。或者换句话说，正是由于数据描述符的访问优先级要高于实例字典，特性的读值和设值方法访问才优先于实例字典。下面我们介绍描述符。
