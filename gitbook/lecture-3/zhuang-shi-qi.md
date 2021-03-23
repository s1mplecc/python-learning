# 装饰器

装饰器，又称函数装饰器，本质上是一个**可调用对象**（实现了 `__call__` 方法），可以是一个函数或者一个类。它的作用是可以让其他函数或类在不需要做任何代码修改的前提下增加额外功能。装饰器接受一个函数作为参数，即被装饰的函数，可能会对这个函数进行处理然后将它返回，或者替换为另一个函数或可调用对象。

先来看一个最简单的装饰器示例：

```python
>>> def decorate(func):
...     print('running decorator...')
...     return func
... 
>>> @decorate
... def target():
...     print('running target...')
... 
running decorator...
>>> target()
running target...
```

上述代码定义了一个名为 decorate 的装饰器，然后通过 `@decorate` 标注在 target 函数上表明用它来装饰 target 函数。乍一看，这与 Java 中的注解语法是一样的，但其实两者作用是完全不同的。Java 中的注解只是元数据，不会对被修饰的对象做任何修改，必须通过运行时的反射（`getAnnotation` 方法）才能发挥它的作用。而在 Python 中，**装饰器的作用就是定义一个嵌套函数**。你可以理解为，通过装饰器装饰后，target 函数被重新定义为了如下形式：

```python
target = decorate(target)
```

但装饰器与这样直接定义还是有几点区别的。第一点，**装饰器是在被装饰的函数定义之后立即执行的**，这通常是在**导入时**（import），也就是 Python 加载模块时发生的。如果你足够细心，就会发现上述代码中的 `'running decorator...'` 是在 target 函数定义后就被立即打印了，并且调用 target 函数时也没有重复打印。也就是说，**函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行**。这突出了 Python 的导入时和运行时的区别。

第二点，函数装饰器既然要体现它的“装饰”语义，就需要接收一个函数作为参数然后返回一个函数，无论返回的函数是原封不动的原函数还是“装饰”后的函数。也就是说，**装饰器对于函数调用者是透明的**。那么，装饰器返回一个其他类型就没有意义。事实证明，如果返回了其他类型，代码运行将会报出 TypeError 错误（没有找到 `__call__` 方法）。而如果只是嵌套函数 `decorate(target)` 的写法是没有返回类型的限制的。

```python
def decorate(func):
    print('running decorator...')
    return 1

# TypeError: 'int' object is not callable
```

### 函数装饰器

事实上，**大多数装饰器会在内部定义一个函数然后将其返回**，原封不动地返回被装饰的函数是没有多大用处的。像这样的双层嵌套函数足以应对绝大多数的装饰器需求了，其最大的好处是：可以**支持带有参数的被装饰函数**。

```python
def logger(func):
    def target(*args, **kwargs):
        print(f'[INFO]: the function {func.__name__}() is running...')
        return func(*args, **kwargs)
    return target
```

不管原函数（被装饰函数）func 接收什么类型的参数，在使用 logger 装饰器时都将被打包成定位参数 `*args` 和仅限关键字参数 `**kwargs`，原封不动的传入到装饰器的内部函数 target 中，执行完装饰逻辑后通过 `func(*args, **kwargs)` 执行原函数。从而能够实现“不修改原有函数接口、不影响原有函数执行”的前提下添加额外功能。如下所示：

```python
>>> @logger
... def person(name, age=18):
...     print(name, age)
... 
>>> person('Jack')
[INFO]: the function person() is running...
Jack 18
```

除了被装饰函数可以带有参数外，装饰器本身也可以带有参数，如 `@logger(Level.INFO)` 在装饰器中指定日志等级，根据业务逻辑标注在不同的函数上，从而最大程度的发挥装饰器的灵活性。

接下来，我会结合一个更实用的例子 —— 记录被装饰函数运行时间的计时器，展示如何定义并使用一个带参装饰器。同时，你还将看到闭包问题是如何在装饰器中体现的。

```python
def clock(unit=TimeUnit.SECONDS):  # ①
    def decorate(func):
        def wrapper(*args, **kwargs):  # ②
            start = time.perf_counter()
            result = func(*args, **kwargs)  # ③
            end = time.perf_counter()
            arg_str = ', '.join(repr(arg) for arg in args)
            if unit == TimeUnit.SECONDS:
                print(f'running {func.__name__}({arg_str}): {end - start}s')
            else:
                print(f'running {func.__name__}({arg_str}): {(end - start) * 1000}ms')
            return result
        return wrapper
    return decorate
```

带参装饰器比无参装饰器多了一层嵌套，这是一种妥协，原因是**装饰器只能且必须接收一个函数作为参数**，所以为了使装饰器接收其他参数，不得不在之上再包装一层函数。在上述代码的三层函数中，最外层定义的 clock 函数是参数化装饰器**工厂函数**，第二层 decorate 函数才是真正的装饰器，wrapper 函数则是执行装饰逻辑的包裹函数（被装饰函数在其中执行）。

此外代码中用带圈数字标注的几个需要注意的点是：

* ① 最外层的 clock 工厂函数接收一个名为 unit 的时间单位的参数，默认值为秒（这里采用枚举类型）；
* ② **如果被装饰的函数带参数，只需要把装饰器最内层函数跟被装饰函数的参数列表保持一致即可**。这里 wrapper 函数接收任意个定位参数 `*args` 和仅限关键字参数 `**kwargs`，写成这样的目的是想体现 clock 计时器的泛用性，你可以在 ③ 处原封不动地将这些参数传给被装饰函数 func 调用；
* ③ func 实际上是定义在 wrapper 外层的自由变量（作为 decorate 的参数传入），所以它已经被绑定到 wrapper 的闭包中。

③ 处是被装饰函数真正执行的地方，上下两行使用计时器记录并统计了 func 函数运行前后的时间差值，在打印时根据传入 clock 的参数决定打印时间单位采用秒还是毫秒。我们来看看如何使用这个装饰器：

```python
>>> @clock()
... def sleep(secs):
...     time.sleep(secs)
... 
>>> @clock(unit=TimeUnit.SECONDS)
... def sleep_secs(secs):
...     time.sleep(secs)
... 
>>> @clock(unit=TimeUnit.MILL_SECONDS)
... def sleep_ms(ms):
...     time.sleep(ms / 1000)
... 
>>> sleep(0.1)
running sleep(0.1): 0.10221230299998751s
>>> sleep_secs(1)
running sleep_secs(1): 1.000441283999976s
>>> sleep_ms(100)
running sleep_ms(100): 103.84234799994374ms
```

需要注意，第一个空参装饰器 `@clock()`，其中的 `()` 是不能省略的，它使用了 `TimeUnit.SECONDS` 作为默认参数，这是在 clock 定义处声明的。此外，clock 装饰器中的参数并不是和函数名绑定的，打印的时间单位完全取决于传入 clock 装饰器的参数。比如，也可以让 sleep\_ms 按照秒的格式打印时间：

```python
>>> @clock(unit=TimeUnit.SECONDS)
... def sleep_ms(ms):
...     time.sleep(ms / 1000)
... 
>>> sleep_ms(100)
running sleep_ms(100): 0.10072612899966771s
```

### 类装饰器

前面提到，装饰器本质上是一个可调用对象。到目前为止，给出的示例都是函数类型的装饰器，函数当然是可调用对象。但如果阅读 Python 源码，会发现许多装饰器是用类定义的，比如内置模块中的 property、classmethod 和 staticmethod 类。这些类都可调用对象（callable），对于用户来说，自定义一个类装饰器需要让这个类实现 `__call__` 方法，这样解释器在运行时会将这个类绑定为 Callable 类的子类。

```python
>>> callable(property)
True
>>> callable(staticmethod)
True
>>> class Foo:
...     def __call__(self): ...
...
>>> callable(Foo())
True
>>> from collections.abc import Callable
>>> issubclass(Foo, Callable)
True
```

对于不含参数的类装饰器来说，除了需要实现 `__call__` 方法之外，唯一要做的就是在构造函数 `__init__` 中初始化被装饰函数。下面定义了一个基于类的无参装饰器。

```python
class Logger:
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        print(f'[INFO]: the function {self._func.__name__}() is running...')
        return self._func(*args, **kwargs)
```

函数类型的装饰器是将装饰逻辑定义在嵌套函数的内部函数中，而无参类装饰器则是将装饰逻辑定义在类中的 `__call__` 方法内，类装饰器同样可以装饰带有参数的函数。两者的区别只不过是，定义函数装饰器时被装饰函数 func 作为参数传入，定义类装饰器时 func 作为属性传入。类装饰器同样是以 `@ + 类名` 的形式标注在被装饰函数上：

```python
>>> from class_decorator import Logger
>>> @Logger
... def person(name, age=18):
...     print(name, age)
... 
>>> person('Jack')
[INFO]: the function person() is running...
Jack 18
```

定义类形式的装饰器与函数形式的装饰器并无太大差别，本质上 Python 解释器都将它们作为可调用对象进行处理。只不过现在最外层的装饰器工厂函数变成了类，传入的装饰器的参数变成了类的属性；而第二层对应的是 `__call__` 方法，接收被装饰函数作为参数；`__call__` 方法内还需定义执行装饰逻辑的包裹函数。用类改写的日志装饰器的代码如下所示：

```python
class Logger:
    def __init__(self, level='INFO'):
        self._level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f'[{self._level}]: the function {func.__name__}() is running...')
            return func(*args, **kwargs)
        return wrapper
```

使用时可以指定日志的输出级别：

```python
>>> @Logger('Debug')
... def person(name, age=18):
...     print(name, age)
... 
>>> person('Jack')
[Debug]: the function person() is running...
Jack 18
```

### 面向切面的程序设计

面向切面的程序设计是一种程序设计思想，旨在将横切关注点与业务主体进行分离。**横切关注点**指的是一些具有横越多个模块的行为，使用传统的软件开发方法不能够达到有效的模块化的一类特殊关注点。通俗点说，面向切面编程就是**使得解决特定领域问题的代码从业务逻辑中独立出来**。业务逻辑的代码中不再含有针对特定领域问题代码的调用，业务逻辑同特定领域问题的关系通过切面来封装、维护。

联系到本文所编写的几个装饰器，日志记录 logger、性能测试 clock 计时器，这些都是较为常见的**横切关注点**。试想一下，如果需要记录多个函数的运行时间，在这些函数内部硬编码计时代码是否合适？显然，这不仅会造成代码重复，更关键的是破坏了函数的存粹性（将不该属于它的计时功能强加于它），造成了代码的紧耦合。现在有了装饰器，只需要在需要计时的函数之上添加 `@clock` 标注即可，计时器的逻辑统一在装饰器中定义和维护，实现了与业务代码的解耦。

因此，装饰器非常适用于有切面需求的场景，诸如：插入日志、性能测试、事务处理、缓存、权限校验等。装饰器是解决这类问题的绝佳设计。通过装饰器，我们可以抽离出与函数功能本身无关的代码到装饰器中，从而实现面向切面编程。

