# 特殊方法

想要更深入地理解鸭子类型，必须要了解 Python 中的特殊方法。前面我们提到的以双下划线开头和结尾的方法，比如 `__iter__`，就称为**特殊方法**（special methods），或称为**魔法方法**（magic methods）。

Python 标准库和内置库包含了许多特殊方法，需要注意的是，永远不要自己命名一个新的特殊方法，因为你不知道下个 Python 版本会不会将其纳入到标准库中。我们需要做的，是重写现有的特殊方法，并且通常情况下，不需要显式的调用它们，应当使用更高层次的封装方法，比如使用 `str()` 代替 `__str__()`，对特殊方法的调用应交由 Python 解释器进行。

Python 对于一些内置方法及运算符的调用，本质上就是调用底层的特殊方法。比如在使用 `len(x)` 方法时，实际上会去查找并调用 x 对象的 `__len__` 方法；在使用 `for` 循环时，会去查找并调用对象的 `__iter__` 方法，如果没有找到这个方法，那会去查找对象的 `__getitem__` 方法，正如我们之前所说的这是一种后备方案。

可以说，特殊方法是 Python 语言灵活的精髓所在，下面我们结合鸭子类型一章中的 SeqDuck 类与特殊方法，尝试还原 Python 解释器运行的逻辑。

```python
class SeqDuck:
    def __getitem__(self, pos):
        return range(3)[pos]
```

1. Python 解释器读入 SeqDuck 类，对所有双下划线开头结尾的特殊方法进行检索。
2. 检索到 `__getitem__` 方法，方法签名符合序列协议。
3. 当需要对 SeqDuck 实例进行循环迭代时，首先查找 `__iter__` 方法，未找到。
4. 执行 `__getitem__` 方法，传入从 0 开始的整数索引进行迭代直至索引越界终止循环。

该过程可以理解为 Python 解释器对 SeqDuck 类的功能进行了**运行时扩充**。显然这增强了 Python 语言的动态特性，但另一方面也解释了为什么 Python 运行效率较低。

下面我将对一些常用特殊方法进行介绍。

### `__new__` & `__init__`

在 Java 和 C\# 这些语言中，可以使用 `new` 关键字创建一个类的实例。Python 虽然没有 `new` 关键字，但提供了 `__new__` 特殊方法。在实例化一个 Python 类时，最先被调用的就是 `__new__` 方法。大多数情况下不需要我们重写 `__new__` 方法，Python 解释器也会执行 object 中的 `__new__` 方法创建类实例。但如果要使用单例模式，那么 `__new__` 方法就会派上用场。下面的代码展示了如何通过 `__new__` 控制只创建类的唯一实例。

```python
>>> class Singleton:
...     _instance = None
...     def __new__(cls):
...         if cls._instance is None:
...         cls._instance = object.__new__(cls)
...         return cls._instance
... 
>>> s1 = Singleton()
>>> s2 = Singleton()
>>> s1 is s2  ## id(s1) == id(s2)
True
```

`__init__` 方法则类似于构造函数，如果需要对类中的属性赋初值，可以在 `__init__` 中进行。在一个类的实例被创建的过程中，`__new__` 要先于 `__init__` 被执行，因为要先创建好实例才能进行初始化。`__new__` 方法的第一个参数必须是 `cls` 类自身，`__init__` 方法的第一个参数必须是 `self` 实例自身。

```python
>>> class Employee:
...     def __new__(cls):
...         print('__new__ magic method is called')
...         return super().__new__(cls)
...
...     def __init__(self):
...         print ("__init__ magic method is called")
...         self.name = 'Jack'
... 
>>> e = Employee()
__new__ magic method is called
__init__ magic method is called
>>> e.name
'Jack'
```

由于 Python 不支持方法重载，即同名方法只能存在一个，所以 Python 类只能有一个构造函数。如果需要定义和使用多个构造器，可以使用带默认参数的 `__init__` 方法，但这种方法实际使用还是有局限性。另一种方法则是使用带有 `@classmethod` 装饰器的类方法，可以像使用类的静态方法一样去调用它生成类的实例。

```python
class Person:
    def __init__(self, name, sex='MAlE'):
        self.name = name
        self.sex = sex

    @classmethod
    def male(cls, name):
        return cls(name)

    @classmethod
    def female(cls, name):
        return cls(name, 'FEMALE')

p1 = Person('Jack')
p2 = Person('Jane', 'FEMALE')
p3 = Person.female('Neo')
p4 = Person.male('Tony')
```

### `__str__` & `__repr__`

> str\(\) is used for creating output for end user while repr\(\) is mainly used for debugging and development. repr’s goal is to be **unambiguous** and str’s is to be **readable**.

`__str__` 和 `__repr__` 都可以用来输出一个对象的字符串表示。使用 `str()` 时会调用 `__str__` 方法，使用 `repr()` 时则会调用 `__repr__` 方法。`str()` 可以看作 string 的缩写，类似于 Java 中的 `toString()` 方法；`repr()` 则是 representation 的缩写。

这两个方法的区别主要在于受众。`str()` 通常是输出给终端用户查看的，可读性更高。而 `repr()` 一般用于调试和开发时输出信息，所以更加强调含义准确无异义。在 Python 控制台以及 Jupyter notebook 中输出对象信息会调用的 `__repr__` 方法。

```python
>>> x = list(("a", 1, True))
>>> x  # list.__repr__
['a', 1, True]
```

如果类没有定义 `__repr__` 方法，控制台会调用 object 类的 `__repr__` 方法输出对象信息：

```python
>>> class A: ...
... 
>>> a = A()
>>> a  # object.__repr__
<__main__.A object at 0x104b69b50>
```

`__str__` 和 `__repr__` 也可以提供给 `print` 方法进行输出。如果只定义了一个方法则调用该方法，如果两个方法都定义了，会优先调用 `__str__` 方法。

```python
>>> class Foo:
...     def __repr__(self):
...         return 'repr: Foo'
...     def __str__(self):
...         return 'str: Foo'
... 
>>> f = Foo()
>>> f
repr: Foo
>>> print(f)
str: Foo
```

### `__call__`

在 Python 中，函数是一等公民。这意味着 Python 中的函数可以作为参数和返回值，可以在任何想调用的时候被调用。为了扩充类的函数功能，Python 提供了 `__call__` 特殊方法，允许类的实例表现得与函数一致，可以对它们进行调用，以及作为参数传递。这在一些需要保存并经常更改状态的类中尤为有用。

下面的代码中，定义了一个从 0 开始的递增器类，它保存了计数器状态，并在每次调用时计数加一：

```python
>>> class Incrementor:
...     def __init__(self):
...         self.counter = 0
...     def __call__(self):
...         self.counter += 1
...         return self.counter
... 
>>> inc = Incrementor()
>>> inc()
1
>>> inc()
2
```

允许将类的实例作为函数调用，如上面代码中的 `inc()`，本质上与 `inc.__call__()` 直接调用对象的方法并无区别，但它可以以一种更直观且优雅的方式来修改对象的状态。

`__call__` 方法可以接收可变参数, 这意味着可以像定义任意函数一样定义类的 `__call__` 方法。当 `__call__` 方法接收一个函数作为参数时，那么这个类就可以作为一个函数装饰器。基于类的函数装饰器就是这么实现的。如下代码我在 func 函数上使用了类级别的函数装饰器 Deco，使得在执行函数前多打印了一行信息。

```python
>>> class Deco:
...     def __init__(self, func):
...         self.func = func
...     def __call__(self, *args, **kwargs):
...         print('decorate...')
...         return self.func(*args, **kwargs)
... 
>>> @Deco
... def func(name):
...     print('execute function', name)
... 
>>> func('foo')
decorate...
execute function foo
```

实际上类级别的函数装饰器必须要实现 `__call__` 方法，因为本质上函数装饰器也是一个函数，只不过是一个接收被装饰函数作为参数的高阶函数。有关装饰器可以详见装饰器一章。

### `__add__`

Python 中的运算符重载也是通过重写特殊方法实现的。比如重载 “+” 加号运算符需要重写 `__add__`，重载比较运算符 “==” 需要重写 `__eq__` 方法。合理的重载运算符有助于提高代码的可读性。下面我将就一个代码示例进行演示。

考虑一个平面向量，由 x，y 两个坐标构成。为了实现向量的加法（按位相加），重写了加号运算符，为了比较两个向量是否相等重写了比较运算符，为了在控制台方便验证结果重写了 `__repr__` 方法。完整的向量类代码如下：

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)
```

在控制台验证结果：

```python
>>> from vector import Vector
>>> v1 = Vector(1, 2)
>>> v2 = Vector(2, 3)
>>> v1 + v2
Vector(3, 5)
>>> v1 == v2
False
>>> v1 + v1 == Vector(2, 4)
True
```

重载了 “+” 运算符后，可以直接使用 `v1 + v2` 对 Vector 类进行向量相加，而不必要编写专门的 `add()` 方法，并且重载了 `==` 运算符取代了 `v1.equals(v2)` 的繁冗写法。从代码可读性来讲直接使用运算符可读性更高，也更符合数学逻辑。

当然，运算符重载涉及的知识不止于此，《流畅的 Python》将其作为单独的一章，可见其重要性。下一节我们将就运算符重载进行深入的讨论。

