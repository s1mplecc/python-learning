# 可迭代对象、迭代器和生成器源码分析

迭代，或称循环，是数据处理的基石。Python 中的可迭代类型的抽象基类定义在 `collections.abc` 模块中，从抽象层次来说，可以分为以下三类：

* **可迭代对象**，`class Iterable(metaclass=ABCMeta)`，抽象类；
* **迭代器**，`class Iterator(Iterable)`，继承自 Iterable 的抽象类；
* **生成器**，`class Generator(Iterator)`，继承自 Iterator 的抽象类。

在这三个抽象基类的实现中，都有一个名为 `__subclasshook__` 的钩子方法，用于将实现了特定方法的类绑定为这些抽象基类的虚拟子类。如下是可迭代对象 Iterable 的部分代码，钩子方法检查了类中有无实现 `__iter__` 方法，对于实现了的类，会被绑定为 Iterable 的虚拟子类。

```python
class Iterable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Iterable:
            return _check_methods(C, "__iter__")
        return NotImplemented
```

联系到鸭子类型一节中所说的“协议”的概念，可以得出结论：可迭代对象的协议需要实现 `__iter__` 方法；类似的，迭代器协议需要同时实现 `__iter__` 和 `__next__` 方法；生成器协议要更复杂一些，除了这两个方法外还需要实现 `send()`、`throw()` 和 `close()` 方法，这三个方法体现了生成器除了迭代之外的功能：可以用作**协程**。

除了钩子方法之外，`collections.abc` 模块中还使用 register 关键字手动绑定了 Iterator 和 Generator 的虚拟子类。这里截取了部分源码：

```python
dict_keyiterator = type(iter({}.keys()))
dict_valueiterator = type(iter({}.values()))
dict_itemiterator = type(iter({}.items()))
list_iterator = type(iter([]))
range_iterator = type(iter(range(0)))
set_iterator = type(iter(set()))
str_iterator = type(iter(""))
tuple_iterator = type(iter(()))

Iterator.register(dict_keyiterator)
Iterator.register(dict_valueiterator)
Iterator.register(dict_itemiterator)
Iterator.register(list_iterator)
Iterator.register(range_iterator)
Iterator.register(set_iterator)
Iterator.register(str_iterator)
Iterator.register(tuple_iterator)

generator = type((lambda: (yield))())
Generator.register(generator)
```

上述代码出现的所有内置类型，包括 list、range、set、str 和 tuple，都实现了 `__iter__` 方法，所以都是可迭代对象。特殊一点的是字典的键、值和键值对，也都分别被定义为可迭代的视图类型 KeysView、ValuesView 和 ItemsView。这些类型都是 Python 的集合类型，集合由于继承了 Iterable 类，所以 **Python 中的所有集合都是可迭代对象**。此处说的集合不是内置类型 set 而是 Collection，定义在 `collections.abc` 模块中。也有人将 Collection 称之为“容器”的，这里将其称之为集合而不是容器是为了与 `collections.abc` 模块中的另一个类 Container 做区分。集合类的钩子方法会去检测是否实现了 `__len__`、`__iter__` 和 `__contains__` 这三个方法。

尽管上述所说的这些内置类型都是可迭代对象，但要注意它们并不是迭代器，被注册的是经过 `iter()` 方法包装后的类型。也就是说，访问这些内置类型的 `__iter__` 方法将会返回一个迭代器，即 `iter(iterable) -> iterator`。迭代器除了能被 for 循环遍历外，还能使用 `next()` 方法产出下一个值。编码时如果要使用 `next()` 方法，首先要注意对象是不是一个迭代器。

```python
>>> l = [1, 2]
>>> isinstance(l, Iterator)
False
>>> iter(l)
<list_iterator object at 0x106e2f640>
>>> next(iter(l))
1
```

除了可迭代对象和迭代器之外，`collections.abc` 模块中还定义了生成器类 Generator，并将形如 `type((lambda: (yield))())` 的类型注册为了生成器的虚拟子类。其中，yield 是一个关键字，意为产出一个值。**只要 Python 函数的定义中含有 yield 关键字，该函数就是生成器函数，调用生成器函数时会返回一个生成器对象**。`lambda: (yield)` 语句其实是定义了一个返回生成器函数的匿名函数，再调用这个生成器函数得到生成器对象，如下：

```python
>>> def gen():
...     return (yield)
... 
>>> gen()
<generator object gen at 0x104b36660>
>>> type(gen())
<class 'generator'>
>>> type((lambda: (yield))())
<class 'generator'>
```

生成器尤为重要，有必要将其作为单独的一节进行介绍。下一节我们将介绍生成器函数的执行过程，以及如何使用生成器表达式返回一个生成器对象。
