# 类型提示

> **PEP 484 -- Type Hints** : Python Version 3.5, Created Time 29-Sep-2014. This PEP aims to provide a standard syntax for type annotations, opening up Python code to easier static analysis and refactoring, potential runtime type checking, and (perhaps, in some contexts) code generation utilizing type information.

在 PEP 3107 提案提出后，已经有一些第三方工具结合函数注解做了静态类型检查方面的工作，其中被采用较多的就是 Jukka Lehtosalo 开发的 mypy 项目。PEP 484 提案受 mypy 的强烈启发（Jukka 也参与了提案的制订），规定了如何给 Python 代码添加**类型提示（Type Hints）**，主要方式就是使用注解，以及引入了一个新模块：**typing 模块**。

### **typing 模块**

为了给 Python 静态类型检查提供统一的命名空间，标准库以渐进定型（gradual typing）的方式引入名为 [typing](https://docs.python.org/3/library/typing.html) 的新模块，新模块不会影响现有程序的正常运行，只会对不规范的类型作出提示。

在 typing 模块中，定义了一些**特殊类型**（\_SpecialForm），包括 Any, NoReturn, ClassVar, Union, Optional 等，从名称可以大概猜出这些类型的作用，比如：Any 代表任意类型；联合类型 `Union[X, Y]` 表示类型非 X 即 Y；Optional 作用则与 Java8 中的 Optional 类似，允许传入参数为空，可以避免空值引用的问题。

除此之外，还有一些常见的数据类型，比如 List、Tuple、Dict、Sequence，它们只是作为标准库类型的别名存在，如：`List = _alias(list, T, inst=False)`。typing 模块也提供了对于**泛型**（Generics）的支持，让我们得以像 `List[int]` 这样去定义特定类型集合。想了解更多 typing 模块的功能，建议阅读 PEP 484文档或者直接阅读源码，源码的文档注释介绍了该模块的结构，通过 `__all__` 属性也可以查明 typing 模块都提供了哪些功能。

PEP 484 旨在为类型注解提供一种标准语法，让 Python 代码更易于静态分析和重构，尽管 typing 模块也提供了一些潜在的用于运行时类型检查的功能模块，尤其是 `get_type_hints()` 函数，但它本身不对其做直接支持，仍然需要开发第三方库才能实现特定的运行时类型检查功能，比如使用装饰器或元类。`get_type_hints` 函数用于获取对象的类型提示，它的源码中包含这么一行：

```python
hints = getattr(obj, '__annotations__', None)
```

这验证了我们之前猜想的类型提示会去查询对象的 `__annotations__` 属性，此外该方法还会对注解字符串进行验证，我们将这个方法再应用到之前随意注解的 foo 函数时就会报错：找不到 “x” 类型。

```python
>>> from typing import get_type_hints
>>> def foo(a: 'x', b: 5 + 6, c: list) -> max(2, 9): ...
>>> foo.__annotations__  # No error
{'a': 'x', 'b': 11, 'c': <class 'list'>, 'return': 9}
>>> get_type_hints(foo)  # Error
NameError: name 'x' is not defined
>>>
>>> def bar(a: int) -> str: ...
>>> get_type_hints(bar)
{'a': <class 'int'>, 'return': <class 'str'>}
```

### **变量注解**

> **PEP 526 -- Syntax for Variable Annotations** : Python Version 3.6, Created Time 09-Aug-2016. This PEP aims at adding syntax to Python for annotating the types of variables (including class variables and instance variables), instead of expressing them through comments.

为了丰富类型提示的功能，Python 随即在 3.6 版本中引入了**变量注解（Variable Annotations）**，用于规定变量的类型。与函数注解相同，变量注解也只是元数据，Python 解释器不对其做任何处理，仅供框架和工具做类型检查。语法上变量注解与函数注解类似，使用 `:` 后接参数类型。

```python
primes: List[int] = []

def signal(flag: bool):
    color: str  # Note: no initial value!
    if flag: color = 'green'
    else: color = 'red'
    return color

class Starship:
    captain: str = 'Picard'  # instance variable with initial value
    stats: ClassVar[Dict[str, int]] = {}  # class variable
```

变量注解适用于全局变量、局部变量、类属性以及实例属性。上述代码中的 ClassVar 是由 typing 模块定义的特殊类型，向静态类型检查程序标示在类实例中不允许对该变量进行赋值。注解的同时可以对变量进行初始化，如果省略初始化，也能很方面的在后续的条件分支中进行初始化。

全局变量的注解存储在当前模块的 `__annotations__` 字典中，如果在 Python 交互式命令行中就是 `__main__`：

```python
>>> a: int = 1
>>> b: str
>>> __annotations__
{'a': <class 'int'>, 'b': <class 'str'>}
>>> 
>>> import __main__
>>> get_type_hints(__main__)
{'a': <class 'int'>, 'b': <class 'str'>}
```

### **何时使用类型提示**

PEP 484 中强调了 Python 将继续维持作为动态语言的特性，从来没有将类型提示强制化或是惯例化的想法。那么何时采用类型提示呢？一般而言，如果你开发的是供他人使用的第三方库（尤其是在 PyPI 上发布的库中），或是在一个多人协作的稍大项目中，推荐使用类型提示。一方面，这会帮助使用库的用户正确地调用接口。另一方面，类型提示也可以帮助理解类型是如何在代码中传播的。

Bernat Gabor 认为类型提示与单元测试重要性一致，本质上都是为了验证你的代码库的输入输出类型，只是表现形式不同。在他的文章 [the state of type hints in Python](https://www.bernat.tech/the-state-of-type-hints-in-python/) 的最后总结中提到：**只要值得编写单元测试，就应该添加类型提示**，哪怕代码只有十行，只要你日后需要维护它。所以他给出的建议是，在编写单元测试的同时添加类型提示。虽然这会添加额外的代码量，但为了代码平稳工作值得付出这个代价，尤其是发生代码变更时。

我们可以在存根文件中使用类型注解来启用类型提示。并且如果参数声明带有默认值，则可以不指定实际的默认值而使用省略号 `...` 代替，这与冒号后的函数体使用省略号一样，将省略号用作占位符。对于变量，一般只声明类型不给出初值。例如：

```python
def foo(x: AnyStr, y: AnyStr = ...) -> AnyStr: ...

stream: IO[str]
```
