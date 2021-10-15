# 类的属性

在 Python 中，数据属性和处理数据的方法统称为属性（attribute），方法也可称为方法属性，本质上是可调用的（callable）属性。Python 提供了丰富的 API 用于控制访问属性，以及实现动态属性。即使访问不存在的属性，也可以通过特殊方法实现“虚拟属性”，从而即时计算属性的值。

#### 处理属性的特殊属性

为了方便处理属性，Python 定义了一些特殊属性，包括：

* `__class__`：对象所属类的引用。`obj.__class__` 与 `type(obj)` 效果一致。类和类的实例都具有属性，有些属性只能在类中查询，比如特殊方法；
* `__dict__`：存储类或实例的可写属性的字典。如果设置了 `__slots__` 属性，实例可能没有 `__dict__` 属性；
* `__slots__`：类可以定义这个属性，限制实例能拥有哪些属性。该属性的值可以是个可迭代对象，但通常会使用元组。如果类设置了 `__slots__` 属性且 `__slots__` 中不包含 `'__dict__'`，那么该类的实例没有 `__dict__` 属性。

**`__dict__`**

默认情况下，Python 会使用名为 `__dict__` 的字典存储类和实例中的可写属性。其中，**类属性字典**由名为 `mappingproxy` 的代理对象包装，`mappingproxy` 定义在 `collections.abc` 模块中，特别指代类属性字典的类型：`mappingproxy = type(type.__dict__)`。类属性字典包含显式定义在类中的字段和方法，以及一些可写的特殊属性，包括模块、字典、弱引用和文档字符串。

```python
>>> class Foo:
...     a = 1
...     def __init__(self):
...         self.b = 2
... 
>>> Foo.__dict__
mappingproxy({'__module__': '__main__', 
              'a': 1, 
              '__init__': <function Foo.__init__ at 0x1051fe8b0>, 
              '__dict__': <attribute '__dict__' of 'Foo' objects>, 
              '__weakref__': <attribute '__weakref__' of 'Foo' objects>, 
              '__doc__': None})
```

类属性不仅限于类字典中所展示的，还包含一些不可变的类属性，比如所属类的引用 `__class__`，直接父类组成的元组 `__bases__` 等。

**实例属性字典**则是普通的字典类型，为实例属性赋值，会动态的修改实例字典。如果属性不存在，则将其添加到字典中，包括在初始化方法 `__init__` 中赋值的实例属性。

```python
>>> foo = Foo()
>>> foo.__dict__
{'b': 2}
>>> foo.c = 3
>>> foo.__dict__
{'b': 2, 'c': 3}
```

**`__slots__`**

Python 解释器会默认在类的构造方法 `__new__` 中创建 `__dict__` 存放实例属性，在访问时通过访问实例字典读取属性值。由于字典底层使用了散列表结构，对属性的存取会相当迅速。但同时，为了减少散列冲突，散列表的大小通常要远大于键的数量，这种基于空间换时间的考量会导致字典会消耗大量内存。为此，Python 提供了 `__slots__` 属性，该属性会覆盖 `__dict__` 属性，**使用类似元组的结构存储实例变量**，从而达到节省内存的目的。

我沿用之前定义的 Person 类做了测试，它包含 name 和 age 两个实例属性。使用列表推导生成一百万个 Person 对象，分别对默认使用 `__dict__` 和添加了 `__slots__` 属性的内存占用情况进行测试。

```
➜ time python3 slots.py --use-dict 
Initial RAM Usage:    5,472,256
  Final RAM Usage:  186,380,288
python3 slots.py --use-dict  1.11s user 0.07s system 99% cpu 1.187 total
➜ time python3 slots.py --use-slots
Initial RAM Usage:    5,476,352
  Final RAM Usage:   76,369,920
python3 slots.py --use-slots  0.74s user 0.04s system 99% cpu 0.788 total
```

可以看到使用 `__slots__` 后内存占用得到显著优化，只占了使用 `__dict__` 的一半不到，运行速度也更快。

**定义 `__slots__` 的方式**是，创建一个名为 `__slots__` 的类属性，把它的值设为一个字符串构成的可迭代对象（通常使用元组），其中的元素名称代表实例属性，比如`__slots__ = ('name', 'age')`。定义 `__slots__` 属性相当于告诉解释器：这个类的所有实例属性都在这儿了。**实例不能再有 `__slots__` 所列之外的其他属性**。但应该明白，`__slots__` 并不是用来禁止类的用户新增实例属性的手段，而只是一种内存优化方案。

如果你阅读 `collections.abc` 模块的源码，会发现其中的类都存在一行 `__slots__ = ()` 代码。即使这些类没有实例属性，使用空元组定义的 `__slots__` 属性可以避免类的构造方法创建 `__dict__` 空字典，空字典也会在堆上分配内存空间。对于集合这种基本数据类型，有必要为其声明空元组形式的 `__slots__` 属性。此外，对于模式固定的数据库记录，以及特大型数据集，也有必要声明 `__slots__` 属性。

上面介绍的这些特殊属性，在一些访问和处理属性的内置函数和特殊方法中会被使用。下面列出这些函数和方法。

#### 处理属性的内置函数

`dir([object])`：列出对象的大多数属性。object 参数是可选的，缺省时会列出当前模块的属性。dir 函数能够审查对象有没有 `__dict__` 和 `__slots__` 属性，并列出其中的键。

`getattr(object, name[, default])`：从对象中读取属性值。获取的属性可能来自对象所属的类或超类。如果没有找到指定属性，则抛出 AttributeError 异常，或返回预设默认值。

`hasattr(object, name)`：会调用 getattr 函数查看能否获取指定的属性，当抛出 AttributeError 异常时返回 False。

`setattr(object, name, value)`：为对象指定的属性设值。这个函数可能会创建一个新属性，或者覆盖现有的属性。前提是对象能够接受这个值，比如设定了 `__slots__` 的对象不能添加新属性。

`vars([object])`：返回对象的 `__dict__` 属性，参数缺省时返回当前模块的 `__dict__` 属性。vars 函数不能处理设定了 `__slots__` 属性的对象。

#### 处理属性的特殊方法

`__getattribute__(self, name)`：除了访问特殊属性和特殊方法，尝试获取指定的属性时总会调用这个方法。dot 运算符、`getattr` 和 `hasattr` 会调用这个方法。该方法内部定义了属性访问规则，当未找到指定属性时抛出 AttributeError 异常，`__getattr__` 方法会被调用。

`__getattr__(self, name)`：仅当获取指定属性失败时，即处理不存在的属性时被调用。用户自定义的类可以实现 `__getattr__` 方法从而动态计算属性的值。

`__setattr__(self, name, value)`：尝试为指定属性设值时总会调用该方法。dot 运算符和 `setattr` 会调用这个方法。该方法内部定义了属性设值规则。

`__delattr__(self, name)`：使用 del 关键字删除属性时会调用这个方法。

`__dir__(self)`：内置函数 `dir()` 会调用这个方法。

#### 属性访问规则

Python 解释器在访问属性时会按照一定的规则，从入口方法 `__getattribute__` 开始，按照顺序依次查找，如果找到则返回，未找到则抛出异常，调用 `__getattr__` 动态计算虚拟属性。属性访问规则如下：

1. `__getattribute__` 方法
2. 数据描述符
3. 实例对象的字典
4. 类的字典
5. 非数据描述符
6. 父类的字典
7. `__getattr__` 方法

注：其中，数据描述符是实现了 `__get__` 和 `__set__` 描述符协议的类。描述符的内容，会在后面做详细介绍。

查询属性的入口方法 `__getattribute__` 实现逻辑的伪代码如下：

```python
def __getattribute__(name)：
    # 先在类(包括父类、祖先类)字典中查找数据描述符
    if find data descriptor in class and base class __dict__:
        # 如果是数据描述符，则调用该数据描述符的 __get__ 方法并将结果返回
        return descriptor.__get__(instance, instance.__class__)
    # 如果不是数据描述符，继续查询实例字典
    if name in instance.__dict__:
        return instance.__dict__[name]
    # 实例字典中没有，则继续查询类字典
    if name in instance.__class__.__dict__:
        return instance.__class__.__dict__[name]
    # 在类和父类字典中查询非数据描述符
    if find non-data descriptor in class and base class __dict__:
        # 如果找到，返回描述符实例
        return descriptor.instance
    # 如果不是描述符，继续在父类字典中查找
    if name in baseclass __dict__:
        return baseclass.__dict__[name]
    # 如果依然没有找到，抛出异常，__getattr__ 函数会被调用
    raise AttributeError
```

为实例属性赋值则没有这么麻烦，`__setattr__` 作为入口方法，只需要判断属性是否是数据描述符，如果是则调用其 `__set__` 方法，如果不是则为实例字典添加新的属性。`__setattr__` 实现逻辑的伪代码如下：

```python
__setattr__(name, value):
    # 先在类(包括父类、祖先类)字典中查找描述符
    if find data descriptor in class and base class __dict__:
        # 如果是数据描述符，则调用描述符的 __set__ 方法进行设值
        descriptor.__set__(instance, value)
    else:
        # 否则，为实例属性字典添加新值
        instance.__dict__[name] = value
```

由此也可以发现，Python 存取属性的方式特别不对等。通过实例访问属性时，如果实例中没有指定属性，那么会尝试获取类属性。而为实例中的属性赋值时，如果属性不存在会在实例中创建该属性，根本不影响类。

下面介绍如何使用 `__getattr__` 方法动态计算虚拟属性。

#### 自定义 `__getattr__` 即时计算属性

处理 JSON 是非常常见的需求，JavaScript 对 JSON 具有天生的支持，可以使用 dot 运算符链式获取属性的值，如 `res.cities[0].ext.province`。而 Python 原生的字典不支持使用 dot 运算符直接获取属性，只能使用 `res['cities'][0]['ext']['province']` 的形式，会显得格外冗长。但可以通过实现一个近似字典的类，达到同样的效果。如下是 Python 中的效果演示：

```python
>>> from json_parser import JsonParser
>>> json = {
...   "code": "200",
...   "cities": [
...     {
...       "lat": "41.2334465",
...       "lng": "116.9772857",
...       "citycode": 207,
...       "ext": {
...         "province": "河北省",
...         "city": "承德市"
...       }
...     } 
...   ]
... }
>>> 
>>> res = JsonParser(json)
>>> res.code
'200'
>>> res.cities[0].citycode
207
>>> res.cities[0].ext.province
'河北省'
```

能够使用 dot 运算符链式获取属性的关键在于定义在 JsonParser 中的 `__getattr__` 方法。前面已经说过，Python 解释器在查询对象属性失败时会调用 `__getattr__` 方法动态计算属性。下面代码定义了动态计算的逻辑：

```python
class JsonParser:
    def __new__(cls, arg):
        if isinstance(arg, Mapping):
            return super().__new__(cls)
        elif isinstance(arg, MutableSequence):
            return [cls(i) for i in arg]
        else:
            return arg

    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        return JsonParser(self._data[name])
```

通过 `__getattr__` 方法递归地创建 JsonParser 类，并将下级的 JSON 结构 `_data[name]` 作为构造参数传入。构造方法 `__new__` 会判断传入参数的类型，如果是映射类型直接创建 JsonParser 对象，如果是可变序列，则通过列表推导式返回 JsonParser 列表。之所以要这么处理是因为 JSON 结构可能是数组，除了映射结构还需要对数组类型进行解析，以支持 `cities[0]` 式的访问。
