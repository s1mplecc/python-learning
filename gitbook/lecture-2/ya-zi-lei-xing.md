# 鸭子类型

在面向对象的静态类型语言中，如果要实现一个带特定功能的序列类型，你可能会想到使用继承，以期能在添加特定功能的同时尽可能的重用代码。这符合面向对象的设计原则，但在 Python 中，继承却不是首选方案。

在 Python 这类动态类型语言中，有一种风格叫做**鸭子类型**（duck typing）。在这种风格中，一个对象有效的语义，不是由继承自特定的类或实现特定的接口决定的，而是由"**当前方法和属性的集合**"决定。这个概念最早来源于 James Whitcomb Riley 提出的“鸭子测试”，“鸭子测试”可以这样表述：“如果一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么它就可以被称为鸭子。”

在 Python 中创建功能完善的序列类型无需使用继承，只需实现符合序列协议的方法。那么，协议又是什么呢？在面向对象编程中，协议是非正式的接口，只在文档中定义，不在代码中定义，可以看作是约定俗成的惯例。例如，Python 的迭代器协议就包含 `__iter__` 和 `__next__` 两个方法，任何实现了 `__iter__` 和 `__next__` 方法的类，Python 解释器会将其视为迭代器，所有迭代器支持的操作，该类也会支持，譬如 `next()` 方法和 `for` 循环。用鸭子类型来解释就是：这个类看起来像是迭代器，那它就是迭代器。

```python
>>> from collections.abc import Iterator
>>> class IterDuck:
...     def __iter__(self): return self
...     def __next__(self): return 1
... 
>>> i = IterDuck()
>>> issubclass(IterDuck, Iterator)
True
>>> isinstance(i, Iterator)
True
>>> next(i)
1
```

由于实现了迭代器协议，上面代码中的 IterDuck 类甚至不需要显式的继承 Iterator 类，Python 解释器就已经将它绑定为 Iterator 类的子类。

**在鸭子类型中，关注点在于对象的行为，即提供的方法，而不在于对象所属的类型。**

### 序列协议

序列协议之所以要专门作为单独的一节，是因为序列在 Python 中尤为重要，Python 会特殊对待看起来像是序列的对象。序列协议包含 `__len__` 和 `__getitem__` 两个方法。任何类，只要实现了 `__len__` 和 `__getitem__` 方法，就可以被看作是一个序列，即使这一次 Python 解释器不再将其绑定为 Sequence 类的子类。

由于序列的特殊性，如果你知道类的具体应用场景，甚至只需要实现序列协议的一部分。下面的代码演示了一个只实现了 `__getitem__` 方法的类，对于序列操作的支持程度：尽管只实现了 `__getitem__` 方法，但 SeqDuck 实例却可以使用 `for` 循环迭代以及 `in` 运算符。

```python
>>> class SeqDuck:
...     def __getitem__(self, index):
...         return range(3)[index]
... 
>>> s = SeqDuck()
>>> s[2]  # __getitem__
2
>>> for i in s: print(i)  # __iter__
... 
0
1
2
>>> 2 in s  # __contains__
True
```

即使没有 `__iter__` 方法，SeqDuck 实例依然是可迭代的对象，因为当 Python 解释器发现存在 `__getitem__` 方法时，会尝试调用它，传入从 0 开始的整数索引进行迭代（这是一种后备机制）。同样的，即使没有 `__contains__` 方法，但 Python 足够智能，能够迭代 SeqDuck 实例检查有没有指定元素。

综上，鉴于序列协议的重要性，如果没有 `__iter__` 和 `__contains__` 方法，Python 会尝试调用 `__getitem__` 方法设法让迭代和 `in` 运算符可用。

