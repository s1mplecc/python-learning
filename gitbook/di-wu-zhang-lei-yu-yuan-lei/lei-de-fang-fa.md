# 类的方法

Python 中类的方法可以分为三类：实例方法、类方法和静态方法。**实例方法**是指定义在类中的第一个参数为 self 的方法。**类方法**是指定义在类中的第一个参数为 cls 的方法。在函数一章的函数对象与方法对象一节中，我们已经介绍过，通过实例访问实例方法和通过类访问类方法会返回一个**绑定方法对象**，分别绑定在实例和类上。而访问**静态方法**则会返回一个**函数对象**。

```python
>>> class Demo:
...     def instance_method(*args):
...         return args
...     @classmethod
...     def class_method(*args):
...         return args
...     @staticmethod
...     def static_method(*args):
...         return args
... 
>>> d = Demo()
>>> Demo.class_method
<bound method Demo.class_method of <class '__main__.Demo'>>
>>> d.instance_method
<bound method Demo.instance_method of <__main__.Demo object at 0x110c84f40>>
>>> Demo.static_method
<function Demo.static_method at 0x110c95700>
```

其中，类方法使用 `@classmethod` 装饰器标注，静态方法使用 `@staticmethod` 标注，这两个装饰器会改变方法的调用方式。

Python 解释器在调用方法对象时会调用对应的下层函数对象，并将相应参数插入到参数列表的开头作为第一个参数，如果是实例方法则插入实例 self，如果是类方法则插入类本身 cls。所以通常情况下，实例方法的第一个参数为 self，类方法的第一个参数为 cls。而静态方法由于本身就是函数对象，所以不会插入参数。

```python
>>> d = Demo()
>>> Demo.class_method(1)
(<class '__main__.Demo'>, 1)
>>> d.instance_method(1)
(<__main__.Demo object at 0x110c84f40>, 1)
>>> Demo.static_method(1)
(1,)
```

可以看到，静态方法就是一个普通的函数，只是定义在类中，而不是模块中。静态方法通常不依赖于类实例，但功能又与类紧密相关。最常见的就是类的构造方法 `__new__`。

类方法则通常用于定义备选构造方法，《Effective Python》中也提到：**以 `@classmethod` 形式的多态去通用地构建对象**。由于 Python 不支持方法重载，所以类的初始化方法 `__init__` 只能存在一个，即通过类名 + "()" 构造并初始化类实例的方式是固定的，如果想通过其他方式构造类实例，可以使用类方法。第一个参数传入 cls，方法返回时调用 `cls()` 生成类实例。

```python
>>> class Person:
...     def __init__(self, name, age):
...         self.name = name
...         self.age = age
...
...     @classmethod
...     def fromtuple(cls, arg):
...         name, age, *rest = arg
...         return cls(name, age)
...
>>> p1 = Person('John', 18)
>>> p1.__dict__
>>> {'name': 'John', 'age': 18}
>>> t = ('Jack', 20, 'abc@email.com')
>>> p2 = Person.fromtuple(t)
>>> p2.__dict__
>>> {'name': 'Jack', 'age': 20}
```
