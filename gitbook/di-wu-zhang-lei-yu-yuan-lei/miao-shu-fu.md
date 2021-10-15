# 描述符

描述符是 Python 的独有特征，不仅在应用层，内置库和标准库中也有使用。除了特性之外，使用描述符的还有方法、classmethod 和 staticmethod 装饰器，以及 functools 模块中的诸多类。理解描述符是精通 Python 的关键，本章的话题就是描述符。

**描述符是实现了特定协议的类**，这个协议包括 `__get__`、`__set__` 和 `__delete__` 方法。特性类 property 实现了完整的描述符协议。通常，可以只实现部分协议。其实，我们在真实代码中见到的大多数描述符只实现了 `__get__` 和 `__set__` 方法，还有很多只实现了其中的一个。

#### 定制描述符实现属性验证

**描述符是对多个属性运用相同存取逻辑的一种方式**。假设我们想为之前定义的 LineItem 类中的 price 和 amount 属性都设置非负验证，一种方式是为它们都编写读值和设值方法，但这会造成代码重复。为了避免这个问题，Python 提出了一种面向对象的解决方式，那就是定制描述符类。

在下面的代码中，定义了一个名为 Quantity 的描述符类，用于管理 LineItem 的属性。我们将 LineItem 类称为托管类，被管理的属性称为托管属性。Quantity 类的实例属性 attribute 指代托管属性的名称，由初始化方法传入。通过在托管类中声明类属性的形式，如 `price = Quantity('price')` 将描述符实例绑定给 price 属性。

```python
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
```

描述符类中定义了 `__set__` 方法，当尝试为托管属性赋值时，会调用这个方法并对值做验证。

```python
>>> item = LineItem(1.0, 5)
>>> item.__dict__
{'price': 1.0, 'amount': 5}
>>> item.amount
5
>>> item.amount = -1
Traceback (most recent call last):
  ...
ValueError: amount must >= 0
>>> item.price = -1
Traceback (most recent call last):
  ...
ValueError: price must >= 0                            
```

**`__set__` 方法的签名**：`def __set__(self, instance, value) -> None: ...`。第一个参数 self 是**描述符实例**，即 `LineItem.price` 或 `LineItem.amount`；第二个参数 instance 是**托管类实例**，即 LineItem 实例；第三个参数 value 是要设置的值。在为属性赋值时，必须直接操作托管实例的 `__dict__`，如果使用内置的 setattr 函数，将会重复调用 `__set__` 导致无限递归。

由于读值方法不需要特殊的逻辑，所以这个描述符类没有定义 `__get__` 方法。一般情况下，如果没有 `__get__` 方法，为了给用户提供内省和其他元编程技术支持，通过托管类访问属性会返回描述符实例。通过实例访问则会去实例字典中查询对应属性。

```python
def __get__(self, instance, owner):
    if instance is None:
        return self
    else:
        return instance.__dict__[self.attribute]
```

**`__get__` 方法的签名**：`def __get__(self, instance, owner) -> Any: ...`。与 `__set__` 方法相同，`__get__` 方法的第一个参数代表描述符实例，第二个参数代表托管类实例。而第三个参数 owner 是**托管类的引用**，当通过托管类访问属性时会被使用，返回类字典中的描述符实例，可以理解为 `instance.__class__`。

此时通过托管类访问属性会得到描述符实例，通过实例访问属性会得到托管属性的值。

```python
>>> LineItem.amount
<lineitem_with_descriptor.Quantity object at 0x108c52760>
>>> item = LineItem(1.0, 5)
>>> item.amount
5
>>> LineItem.__dict__
mappingproxy({'__module__': 'lineitem_with_descriptor', 
              'price': <lineitem_with_descriptor.Quantity object at 0x10abd1910>, 
              'amount': <lineitem_with_descriptor.Quantity object at 0x10ac037f0>, 
              '__init__': <function LineItem.__init__ at 0x10abd8af0>, 
              'total_price': <function LineItem.total_price at 0x10abd8b80>, 
              '__dict__': <attribute '__dict__' of 'LineItem' objects>, 
              '__weakref__': <attribute '__weakref__' of 'LineItem' objects>, 
              '__doc__': None})
```

同一时刻，内存中可能存在许多 LineItem 实例，但只会存在两个描述符实例：`LineItem.price` 和 `LineItem.amount`。这是因为描述符实例被定义为 LineItem 的类属性，会出现在 LineItem 的类字典中，由全部实例共享。

#### 描述符分类

我们将同时实现了 `__get__` 和 `__set__` 方法的描述符类称为**数据描述符**，将只实现了 `__get__` 的描述符类称为**非数据描述符**。在 CPython 的描述符对象 [descrobject](https://github.com/python/cpython/blob/master/Objects/descrobject.c) 的源码中，会检查描述符是否有 `__set__` 方法来返回描述符是否是数据描述符：

```c
int PyDescr_IsData(PyObject *ob) {
    return Py_TYPE(ob)->tp_descr_set != NULL;
}
```

Python 社区在讨论这些概念时会用不同的术语，数据描述符也被称为**覆盖型描述符**或强制描述符，非数据描述符也被称为**非覆盖型描述符**或遮盖型描述符。总之，这两者的区别在于是否实现了 `__set__` 方法。之所以这么分类，是由于 Python 中**存取属性方式的不对等性**，我们在属性访问规则一节中提到了这点。这种不对等的处理方式也对描述符产生影响。

描述符的覆盖体现在，如果实现了 `__set__` 方法，即使描述符是类属性，也会覆盖对实例属性的赋值操作。比如 `item.amount = -1` 不会直接修改实例字典，而是强制执行描述符的 `__set__` 方法对数值进行非负验证。

如果没有实现 `__set__` 方法，比如 Python 中的方法就是以非覆盖型描述符实现的，只定义了 `__get__` 方法。如果类中定义了名为 method 的方法，使用 `obj.method = 1` 会直接修改实例字典，即**实例属性会遮盖同名描述符属性**，但类中的描述符属性依然存在。如下：

```python
>>> class C:
...     def method(): ...
... 
>>> obj = C()
>>> obj.method = 1
>>> obj.__dict__
{'method': 1}
>>> C.method
<function C.method at 0x10f7ff940>
```

综上所述，数据描述符的表现形式更像可以被随意赋值的数据，提供了完备的取值方法 `__get__` 和设值方法 `__set__`。而非数据描述符表现形式不像数据，比如 Python 中的方法，为非数据描述符赋值会遮盖掉实例的同名描述符属性。

以上讨论的都是是否存在 `__set__` 方法的情形，其实，也可以没有读值方法 `__get__`，比如我们定义的 Quantity 描述符。一般情况下，没有读值方法时访问属性会返回描述符对象本身。然而访问 LineItem 实例属性 `item.amount` 会得到对应数值。这是因为在它的初始化方法 `__init__` 中已经调用了描述符的 `__set__` 方法，该方法为实例字典 `__dict__` 创建了同名实例属性，由于实例属性会遮盖同名描述符属性，读取属性会返回实例字典中的值而不是描述符对象。这也是为什么将实现了 `__set__` 的描述符称为遮盖型描述符的原因。

总之，**按照属性访问规则，数据描述符在实例字典之前被访问（调用 `__get__` 和`__set__` 方法），非数据描述符在实例字典之后被访问（可能会被遮盖）**。

#### 方法是描述符

定义在类中的方法会变成绑定方法（bound method），这是 Python 语言底层使用描述符的最好例证。

```python
>>> class C:
...     def method(): ...
... 
>>> obj = C()
>>> obj.method
<bound method C.method of <__main__.C object at 0x10f837580>>
>>> C.method
<function C.method at 0x10fff6b80>
```

通过类和实例访问函数返回的是不同的对象。CPython 中定义的函数对象 [funcobject](https://github.com/python/cpython/blob/master/Objects/funcobject.c) 实现了描述符协议的 `__get__` 方法，即如下的 `func_descr_get` 方法。与描述符一样，通过托管类访问函数时，传入的 obj 参数为空，函数的 `__get__` 方法会返回自身的引用。通过实例访问函数时，返回的是绑定方法对象，并把托管实例绑定给函数的第一个参数（即 self），这与 functool.partial 函数的行为一致。

```c
/* Bind a function to an object */
static PyObject *
func_descr_get(PyObject *func, PyObject *obj, PyObject *type)
{
    if (obj == Py_None || obj == NULL) {
        Py_INCREF(func);
        return func;
    }
    return PyMethod_New(func, obj);
}

/* Method objects are used for bound instance methods returned by instancename.methodname.
   ClassName.methodname returns an ordinary function. */
PyObject * PyMethod_New(PyObject *func, PyObject *self)
```

绑定方法对象还有个 `__call__` 方法，用于处理真正的调用过程。这个方法会调用 `__func__` 属性引用的原始函数，把函数的第一个参数设为绑定方法的 `__self__` 属性。这就是**形参 self 的隐式绑定过程**。

#### 使用描述符的最佳实践

**使用特性以保持简单**：内置的 property 类创建的是数据描述符，`__get__` 和 `__set__` 方法都实现了。特性的 `__set__` 方法默认抛出 AttributeError: can't set attribute，因此创建只读属性最简单的方式是使用特性。且由于特性存在 `__set__` 方法，不会被同名实例属性遮盖。

**只读描述符也要实现 `__set__` 方法**：如果使用描述符类实现只读数据属性，要记住，`__get__` 和 `__set__` 方法必须都定义。否则，实例的同名属性会遮盖描述符。只读属性的 `__set__` 方法只需抛出 AttributeError 异常，并提供合适的错误消息。

**非特殊的方法可以被实例属性遮盖**：Python 的方法只实现了 `__get__` 方法，所以对与方法名同名的属性将会遮盖描述符，也就是说 `obj.method = 1` 负值后通过实例访问 method 将会得到数字 1，但不影响类或其他实例。然而，特殊方法不受这个问题影响。因为解释器只会在类中查询特殊方法。也就是说 `repr(x)` 执行的其实是 `x.__class__.__repr__(x)`，因此 x 的 `__repr__` 属性对 `repr(x)` 方法调用没有影响。出于同样的原因，实例的 `__getattr__` 属性不会破坏常规的属性访问规则。

**用于验证的描述符可以只实现 `__set__` 方法**：对仅用于验证的描述符来说，`__set__` 方法应该检查 value 参数是否有效，如果有效，使用与描述符实例同名的名称作为键，直接在实例字典中设值，如 Quantity 中的 `instance.__dict__[self.attribute] = value` 语句。这样，从实例字典中读取同名属性就不需要经过 `__get__` 方法处理。

**仅有 `__get__` 方法的描述符可以实现高效缓存**：如果仅实现了 `__get__` 方法，那么创建的是非数据描述符。这种描述符可用于执行某些耗费资源的计算，然后为实例设置同名属性，缓存结果。同名实例属性会遮盖描述符，因此后续访问会直接从实例字典中获取值，而不会再出发描述符的 `__get__` 方法。

#### 描述符应用场景

当将描述符逻辑抽象到单独的代码单元中，如 Quantity 类中，就可以在整个应用中进行重用。在一些框架中，会将描述符定义在单独的工具模块中，比如 Django 框架中与数据库交互的模型字段类，就是描述符类。你会发现下面这段 Django 的测试用例的代码与我们定义的 LineItem 非常类似。只不过我们的描述符类 Quantity 换成了他们的 models.CharFiled 等。

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book)
    person = models.OneToOneField('Person', models.CASCADE, null=True)
```

当然，目前定义的描述符类还有提升的空间，比如 `price = Quantity('price')` 使用字符串对属性名进行初始化可能并不那么可靠。又比如想为字段设置更多限定，比如 Django 中设置的字段 max_length 等。其实，Django 框架使用到了 Python 更高阶的类元编程的特性 —— 元类。除了开放框架，一般用不到这个特性。后面我们会对元类加以介绍。
