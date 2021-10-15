# 序列

之前我们已经讨论过，Python 的“序列协议”是指：任何类，只要使用标准的签名和语义实现了 `__getitem__` 和 `__len__` 方法，就能用在任何期待序列的地方，解释器会为这些类做特殊的支持，比如支持迭代和 in 运算符。序列协议的接口定义可以查阅官方的 CPython API 接口文档：[Python/C API Reference Manual -- Sequence Protocol](https://docs.python.org/3.8/c-api/sequence.html)，其中有这样一个函数：

```c
int PySequence_Check(PyObject *o)
/* Return 1 if the object provides sequence protocol, and 0 otherwise. 
   Note that it returns 1 for Python classes with a __getitem__() method 
   unless they are dict subclasses since in general case it is impossible to determine what the type of keys it supports. */
```

这个函数的作用是检查并返回对象是否支持序列协议 —— 只在实现了 `__getitem__` 方法且不是字典子类时才返回 1。这也符合我们之前所说的，协议是非正式的，没有强制力，只要你知道类的具体使用场景，可以只实现协议的一部分。比如，仅为了支持迭代，甚至不需要提供 `__len__` 方法。

Python 常用的内置序列类型包括：字符串 str、列表 list、元组 tuple 和范围 range。尽管字典 dict 和集合 set 实现了序列协议中的 `__getitem__` 和 `__len__` 方法，但它们并不算序列类型，因为它们的特征与序列有本质差异，比如这两个类型不支持通过整数下标索引访问元素，不支持切片，并且字典和集合内的元素是无序的。

序列类 Sequence，定义在标准库 `collections.abc` 模块中，继承自 Reversible 和 Collection 类，而 Collection 又继承自 Sized、Iterable 和 Container，体现了序列类可反转、具有规模、可迭代和是一个容器的语义。

从 `collections.abc` 模块的源码中，我们还能了解到序列类包含哪些子类。除了显示继承了 Sequence 的子类，如 ByteString 和 MutableSequence，还有通过 register 关键字绑定为 Sequence 虚拟子类的一些内置类型，在绑定虚拟子类一节中也提到过这一点。

```python
>>> from collections.abc import Sequence
>>> all([issubclass(i, Sequence) for i in (str, list, tuple, range, bytes, bytearray, memoryview)])
True
>>> any([issubclass(i, Sequence) for i in (dict, set)])
False
```

上面列表推导表达式中的所有类型都是定义在 builtsin 模块中的内置类型，可以看到，除了 dict 和 set 之外，第二行的所有内置类型都是序列类型。除此之外，标准库中还定义了其他序列类型，比如 array 模块的 array 数组类型，collections 模块中的 deque 双端队列类型。

#### 序列分类

对于这些序列类型，按照序列内可容纳的类型，可以划分为以下两组：

* **容器序列**：list、tuple 和 collections.deque 这些序列类能存放不同类型的数据；
* **扁平序列**：str、bytes、bytearray、memoryview、array.array 和 range 这类序列类只能容纳一种或某种特定类型的数据。

容器序列存放的是它们所包含的任意类型的对象的引用，而扁平序列存放的是值而不是引用。扁平序列存储在一段连续的内存空间之上，只能存放诸如字符、字节和数值这种基础类型。

序列类型还能按照能否被修改来分类：

* **可变序列**：list、bytearray、memoryview、array.array 和 collections.deque；
* **不可变序列**：tuple、str、bytes 和 range。

可变序列 MutableSequence 也定义在 `collections.abc` 模块中，并在继承 Sequence 的基础上还添加了一些支持序列修改的默认方法，如 `append()`、`pop()` 方法等。除了 Sequence 基类中要实现的 `__getitem__` 和 `__len__` 方法外，可变序列还要求具体子类必须实现 `__setitem__`、`__delitem__` 和 `insert()` 方法。

序列不可变意味着序列一旦被声明赋值，序列的大小就固定下来，其内的元素也不能被修改。这里用来说明序列可变不可变的典型案例是列表和元组。在 Python 中，列表是可变的，元组是不可变的。列表可变体现在它支持对元素的增加删除和直接赋值，且列表支持**就地运算**，比如使用 "+=" 运算符可以直接将一个可迭代对象中的元素添加到当前列表的末尾。而元组是不可变的，元组一经定义大小就已固定，不能增加删除元素，也不对其内元素重新赋值。即使元组也支持就地运算符，但会生成一个新的元组对象重新绑定。

```python
>>> l = [1, 2]  # list
>>> id(l)
4411278528
>>> l[0] = 0
>>> l += [3, 4]
>>> l
>>> [0, 2, 3, 4]
>>> id(l)
4411278528
>>> t = (1, 2)  # tuple
>>> id(t)
4410964416
>>> t += (3, 4)
>>> id(t)
4411277824
>>> t[0] = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> t
(1, 2, 3, 4)
```

此外，Python 中的可散列对象一定是不可变类型，散列方法 `__hash__` 通常和 `__eq__` 方法一起用来判断两个对象是否相等，如集合 set 和字典的键要求元素是可散列的，这被用来判断元素是否重复。所以，元组可以作为集合的元素和字典的键，而列表却不可以。

```python
>>> t1 = (1, 2)
>>> t2 = (1, 2)
>>> id(t1) == id(t2)
False
>>> hash(t1) == hash(t2)
True
>>> set([(1, 2), (3,)])
{(1, 2), (3,)}
>>> dict({(1, 2): 1})
{(1, 2): 1}
```

注：在散列时，元组内的每一项元素会被散列然后进行 XOR 异或运算，因此只有当元组中的每个元素都是不可变类型时，该元组才能被散列。

#### 序列切片 \[TODO]
