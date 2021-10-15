# 如何阅读 Python 源码

### 前言

阅读源码是每个程序员都应当具备的技能，阅读源码不仅能帮助你理解一个模块实现的细节，也能让你从优秀的源码中汲取经验，遵循更好的编码规范，编写出更 Pythonic 的代码。但不可否认的是，阅读源码需要一定的编码功底，盲目的阅读并不能取得应有的效果。在阅读源码之前我们要明白阅读的目的，如果是想了解一个模块的实现细节自不必多说，但如果是想提高自己的 Python 编码水平，那么就应该从 Python 标准库以及一些优秀的第三方开源代码下手。

在《Python编程之美：最佳实践指南》这本书中，作者 Kenneth Reitz 从简单的 HowDoI 项目，到大一点的 requests 库（他本身也是这个库的开发者），再到后面的 Web 框架 Flask，逐步递进地展示如何阅读高质量的代码。如果想阅读优秀的第三方库源码，可以从他在书中罗列出的经典项目开始。除此之外，GitHub 上也有人整理了比较详尽的目录：[Python 开源库及示例代码](https://github.com/programthink/opensource/blob/master/libs/python.wiki)。项目很多，但不是每个都必读。还是强调的那一点：不要盲目的阅读源码，确定有必要的时候再去阅读。

抛开这些问题不谈，本篇我想结合我自己在阅读标准库源码（主要是 typing 模块和 re 模块）时的一点理解，介绍一些阅读源码前需要掌握的先验知识，以及如何结合开发工具在 PyCharm IDE 中高效地阅读源码。让我们先从 Python 代码的类型提示开始。

### 函数注解

> **PEP 3107 -- Function Annotations** : Python Version 3.0, Created Time 2-Dec-2006. This PEP introduces a syntax for adding arbitrary metadata annotations to Python functions.

Python 3 添加了对类型提示（Type Hints）的支持，在此之前 Python 2.x 一直缺乏一种统一的方式去对函数参数和返回值进行标注，一些工具或三方库通过 docstring、注释或者函数装饰器等其他方法尝试去弥补这种缺陷。而自从 Python 3.0 开始，Python 通过 PEP 3107 提案引入了**函数注解**，也就是 Function Annotations，提供了一种标准的解决方案，用于**为函数声明中的参数和返回值附加元数据**。

函数注解的语法如下所示：

```python
def foo(a: expression, b: expression = 5) -> expression:
    ...
```

函数声明中的各个参数可以在 `:` 之后添加注解表达式。如果参数有默认值，表达式后可以跟 `=` 指定默认值，且与常规函数声明一样，指定默认值参数要出现在无默认值参数之后。注解表达式最常使用的是类型（如 str 或 int），也可以是一个字符串（如 'int > 0'）。如果想注解返回值，在 `)` 与 `:` 之间添加 `->` 和一个表达式，表达式可以是任意类型，如果函数无返回值则为 None。

本质上来说，PEP 3107 只是一种前导的语法规范，不对注解任何实质处理，你可以将其理解为官方规定的函数声明的注释。换句话说，**注解只是元数据**，Python 解释器对其不做检查、不做强制、不做验证。Python 对注解所做的唯一的事情，就是将它们存储在函数的 `__annotations__` 属性中：

```python
>>> def foo(a: 'x', b: 5 + 6, c: list) -> max(2, 9): ...
>>> foo.__annotations__
{'a': 'x', 'b': 11, 'c': <class 'list'>, 'return': 9}
```

其中 return 键保存的是返回值的注解，即函数声明里以 `->` 标记的部分。从这个例子我们可以看出，注解表达式的约束非常的宽泛，不管你是类型，还是字符串，或是个表达式。

注解可以供 IDE、框架和装饰器等工具使用，举个例子，框架可以对 `price: 'int > 0'` 这样的字符串注解转换为对参数的验证。注解最大的作用是为 IDE 和 lint 程序中的**静态类型检查**功能提供额外的类型信息，也就是我们接下来要讨论的类型提示。

**延伸**：Java 中的注解也称为 Annotation，使用 `@` 符号标注，本质上也是元数据，本身 Java 解释器不会对其做任何处理，只有结合 Java 运行时的反射（getAnnotation 方法）才能获取注解内容从而针对性地制定处理逻辑，这在一些框架例如 Spring 中使用颇多。这与 Python 中的注解是否存在异曲同工之处呢？我们有理由相信，Python 中的静态类型检查工具也是获取了函数的 `__annotations__` 属性从而进行处理。

### 类型提示

> **PEP 484 -- Type Hints** : Python Version 3.5, Created Time 29-Sep-2014. This PEP aims to provide a standard syntax for type annotations, opening up Python code to easier static analysis and refactoring, potential runtime type checking, and (perhaps, in some contexts) code generation utilizing type information.

在 PEP 3107 提案提出后，已经有一些第三方工具结合函数注解做了静态类型检查方面的工作，其中被采用较多的就是 Jukka Lehtosalo 开发的 mypy 项目。PEP 484 提案受 mypy 的强烈启发（Jukka 也参与了提案的制订），规定了如何给 Python 代码添加**类型提示（Type Hints）**，主要方式就是使用注解，以及引入了一个新模块：**typing 模块**。

#### typing 模块

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

#### 变量注解

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

#### 何时使用类型提示

PEP 484 中强调了 Python 将继续维持作为动态语言的特性，从来没有将类型提示强制化或是惯例化的想法。那么何时采用类型提示呢？一般而言，如果你开发的是供他人使用的第三方库（尤其是在 PyPI 上发布的库中），或是在一个多人协作的稍大项目中，推荐使用类型提示。一方面，这会帮助使用库的用户正确地调用接口。另一方面，类型提示也可以帮助理解类型是如何在代码中传播的。

Bernat Gabor 认为类型提示与单元测试重要性一致，本质上都是为了验证你的代码库的输入输出类型，只是表现形式不同。在他的文章 [the state of type hints in Python](https://www.bernat.tech/the-state-of-type-hints-in-python/) 的最后总结中提到：**只要值得编写单元测试，就应该添加类型提示**，即使代码只有十行，只要你日后需要维护它。所以他给出的建议是，在编写单元测试的同时添加类型提示。虽然会添加额外的代码量，但为了代码平稳工作值得付出这个代价，尤其是发生代码变更时。

我们可以在存根文件中使用类型注解来启用类型提示。并且如果参数声明带有默认值，则可以不指定实际的默认值而使用省略号 `...` 代替，这与冒号后的函数体使用省略号一样，将省略号用作占位符。对于变量，一般只声明类型不给出初值。例如：

```python
def foo(x: AnyStr, y: AnyStr = ...) -> AnyStr: ...

stream: IO[str]
```

### .pyi 存根文件

由于 Python 是动态语言，不对类型做强制约束，所以 IDE 在类型检查、类型推断、代码补全以及重构等方面必然不如 Java 等静态语言来的方便。**存根文件是包含类型提示信息的文件**，运行时不会用到，而是**提供给第三方工具做静态类型检查和类型推断**，这方面 PyCharm 做的很好。

在 PyCharm 中，如果某一行的左边有 \* 号标识，则说明这一行（可以是类、属性或函数）在存根文件中有定义，你可以点击 \* 号跳转到该文件对应的存根文件，通常是存放在 Python 库文件的 Typeshed Stubs 目录中，文件名以 `.pyi` 后缀结尾。同时，存根文件也是 GitHub 上一个单独的项目，项目地址：https://github.com/python/typeshed ，Python 的标准库以及内置 builtins 存根可以在该项目的 stdlib 目录下找到。

我们来看看 Python 正则库 re 的存根文件和源文件：

```python
# re.pyi
@overload
def compile(pattern: AnyStr, flags: _FlagsType = ...) -> Pattern[AnyStr]: ...
@overload
def compile(pattern: Pattern[AnyStr], flags: _FlagsType = ...) -> Pattern[AnyStr]: ...
  
# re.py
def compile(pattern, flags=0):
    "Compile a regular expression pattern, returning a Pattern object."
    return _compile(pattern, flags)
```

这里只截取了源码中的一段 compile 函数。从形式上看，存根文件与 C 语言中的头文件有相似之处，将函数声明与函数定义分文件存放，但与其将存根文件理解为函数声明文件，不如理解为函数接口（Interface）文件，接口的意义就是让用户在调用时可以清晰地查看函数的参数和返回值类型。这也是为什么 PEP 484 的作者之一 Jukka Lehtosalo 说可以将 `.pyi` 中的 i 理解为 Interface。

上述源文件中的 compile 函数，调用了私有的 \_compile 函数并返回一个 Pattern 对象，作用是将字符串处理（编译）成正则表达式模版。进一步 \_compile 的源码会发现，如果传入的 pattern 参数本来就是 Pattern 类型的，为了避免重复处理，方法会直接返回 pattern，如下面的代码所示。

```python
def _compile(pattern, flags):
    if isinstance(pattern, Pattern):
        if flags:
            raise ValueError(
                "cannot process flags argument with a compiled pattern")
        return pattern
    ...
```

这也解释了为什么存根文件中会存在两个 compile 函数声明，其中的第二个就是接收 Pattern 类型作为参数的。除了 compile 函数之外，re 存根文件中的大多数函数都有两个重载函数，原因就是它们实现时都调用了 \_compile 函数。事实上，为了防止用户多次调用 \_compile 引起不必要的开销，\_compile 也设置了缓存优化，这点留给读者自行阅读源码分析。

在最新的 PyCharm 2020.3 版本中，支持直接创建 Python stub 类型的 Python File，只需要存根文件与源文件同名，PyCharm 就会自动按照存根文件中指定的类型进行静态类型检查。并且，你也可以像 Typeshed 项目为存根文件分配单独的文件夹，具体操作详见 JetBrains 官网的 PyCharm 手册：[Python Stubs](https://www.jetbrains.com/help/pycharm/stubs.html)。

### PyCharm 高效阅读源码

除了标注存根文件，PyCharm 还对子类父类方法重载进行了标注，分别用 `O↑` 表示这一行重载了父类方法，点击可以跳转到父类实现；`O↓` 表示这一行有子类重载，点击可以跳转到子类实现。其中 O 代表的是 Override 的含义。

比如我们阅读 Python 内置的列表 list 的源码，append 方法这一行既是重载自父类也有子类重载（存根文件中标注的）：

```python
class list(MutableSequence[_T], Generic[_T]):
    def append(self, __object: _T) -> None: ...
```

可以看到 list 多重继承自 MutableSequence 和 Generic，如果点击 append 左侧 `O↑`，就会跳转到父类 MutableSequence 的 append 实现处。如果点击 `O↓`，可以选择某个子类并进行跳转（list 存在多个子类）。这在阅读一个具有继承结构的源码时会有所帮助。

当然，如果想在 PyCharm 中高效阅读源码，需要结合快捷键来使用。这里列出一些 Mac OS 下的快捷键，Windows 下一般是将 Cmd 替换为 Ctrl，你也可以打开 PyCharm 设置自行查阅 Keymap 快捷键：

| 快捷键                      | 作用                   | PyCharm Keymap              |
| ------------------------ | -------------------- | --------------------------- |
| Cmd + U                  | 跳转到父类实现              | Go to Super Method          |
| Cmd + Alt + B/Left Click | 跳转到子类实现              | Go to Implementations       |
| Cmd + B/Left Click       | 跳转到定义处或调用处           | Go to Declaration or Usages |
| Cmd + \[                 | 跳转到鼠标停留的上一个位置        | Back                        |
| Cmd + ]                  | 跳转到鼠标停留的下一个位置        | Forward                     |
| Cmd + E                  | 跳转到最近浏览的文件           | Iterate Recent Files        |
| Cmd + Shift + O          | 以文件名查询并跳转            | Go to File                  |
| Cmd + O                  | 以类名查询并跳转             | Go to Class                 |
| Cmd + Alt + O            | 以符号查询并跳转，可以查询函数和全局变量 | Go to Symbol                |
| 双击 Shift                 | 整合了所有查询              |                             |
| Cmd + F                  | 搜索当前文件下内容            | Find                        |
| Cmd + Shift + F          | 搜索项目文件中的内容           | Find in Files               |

这些都是 PyCharm 中非常实用的快捷键，不管是阅读源码还是自己编码，熟悉这些快捷键有助于快速定位到某个文件，某个函数或是某个变量，从而提高我们的效率。

### 参考

* [Reading Great Code -- Kenneth Reitz](https://docs.python-guide.org/writing/reading/)
* [PEP 3107 -- Function Annotations](https://www.python.org/dev/peps/pep-3107/)
* [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/)
* [PEP 526 -- Syntax for Variable Annotations](https://www.python.org/dev/peps/pep-0526/#abstract)
* [Python 官方文档：typing — Support for type hints](https://docs.python.org/3/library/typing.html)
* [Python Type Checking (Guide)](https://realpython.com/python-type-checking/#function-annotations)
* [译文：全面理解 Python 中的类型提示（Type Hints）](https://sikasjc.github.io/2018/07/14/type-hint-in-python/#%E4%B8%BA%E4%BB%80%E4%B9%88%E9%9C%80%E8%A6%81%E7%B1%BB%E5%9E%8B%E6%8F%90%E7%A4%BA)
