# 前言

在写该系列时我正在阅读《流畅的 Python》这本书，这本书作为 Python 的进阶读物确实名不虚传，不仅囊括了 Python 的诸多特性，而且为我们展示了一种 Python 设计思想，一种与我之前接触的 Java OOP 截然不同的思想，比如 Python 内置了许多特殊方法或者叫魔法方法（magic methods），又比如“鸭子类型”：只要表现的像一个序列，那么就可以对它进行迭代，等等。总的来说，Python 有它自己的设计风格，它是一门注重实用，专为程序员高效编码而生的语言。我相信随着对这本书的深入阅读和更多 Python 的编码实践，我能够对 Python 这门语言有一些更多感悟。

当然，“光看不练假把式”，最开始的时候，我只是在命令行中去验证一些 Python 特性，随后我意识到这远远不够，为什么不将学习中的零碎知识点加以整理做成一个系列呢？于是，该系列诞生了。由于知识点的离散性，所以对 Lecture 的划分就显得有些随心所欲，我尽量在目录中将知识点的名称罗列出来。

代码已经托管到 Github 上，链接：https://github.com/s1mplecc/python-learning-lectures

如果你是在 PyCharm 中运行示例代码，那么 import 语句可能会有恼人的红色报错，但其实是可以正常运行的。只需要将子目录标记为源代码根目录，即 Mark Directory as Sources Root。

# 目录

* [Lecture 1](#lecture-1)
  * [使用 pytest 做单元测试](#%E4%BD%BF%E7%94%A8-pytest-%E5%81%9A%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95)
  * [如何阅读 Python 源码](#%E5%A6%82%E4%BD%95%E9%98%85%E8%AF%BB-python-%E6%BA%90%E7%A0%81)
* [Lecture 2](#lecture-2)
  * [鸭子类型](#%E9%B8%AD%E5%AD%90%E7%B1%BB%E5%9E%8B)
  * [重载特殊方法](#%E9%87%8D%E8%BD%BD%E7%89%B9%E6%AE%8A%E6%96%B9%E6%B3%95)
  * [重载运算符](#%E9%87%8D%E8%BD%BD%E8%BF%90%E7%AE%97%E7%AC%A6)
  * [生成式表达式](#%E7%94%9F%E6%88%90%E5%BC%8F%E8%A1%A8%E8%BE%BE%E5%BC%8F)
  * [\* 和 \*\* 运算符](#-%E5%92%8C--%E8%BF%90%E7%AE%97%E7%AC%A6)
* [Lecture 3](#lecture-3)
  * [函数是一等公民](#%E5%87%BD%E6%95%B0%E6%98%AF%E4%B8%80%E7%AD%89%E5%85%AC%E6%B0%91)
  * [闭包](#%E9%97%AD%E5%8C%85)
  * [装饰器](#%E8%A3%85%E9%A5%B0%E5%99%A8)

# Lecture 1

以单元测试作为系列学习的开始，应当还算合理。我想尽量给这个学习系列带入些测试驱动的思想，一方面，熟练掌握一门语言的过程其实是特性累积的过程，今天学习了 Python 重载运算符，明天学习如何编写 Python 装饰器，这样看来，每次编写一个单元测试用于验证一个语言特性最适合不过了（当然可能不止需要一个单元测试）。另一方面，如果验证结果的时候还是使用一堆 print 方法，就会显得相当凌乱而且不那么专业，而通过运行测试时打印的一系列方法名，可以清楚这些模块涉及了哪些 Python 特性。

尽管我的测试方法命名不严格遵循 TDD 中的  “Given-When-Then” 格式，但是通过 `should_` 这种命名规范，也可以清晰的明白某个测试用例测试了什么功能。比如，看到 `test_should_add_two_vectors_with_add_operator()`，你可能能猜到这个测试用例测试的是加法运算符的重载。

## 使用 pytest 做单元测试

至于为什么选择 pytest 作为单元测试框架，也不是多么深思熟虑后的结果，只是我单纯的讨厌 Python 自带的 unittest 的写法，需要继承一个测试基类，而且到处充斥着 `self`。反观 pytest，只需要符合它的命名规范，测试方法就会被框架自动检测到并运行，而且 pytest 重写了 assert 关键字，打印信息也更加人性化。

编写 pytest 测试样例需要符合如下规范：

- 测试文件如果不指定，必须以 `test_` 开头或结尾；
- 测试类必须以以 `Test` 开头，且不能含有 `__init__` 构造函数；
- 测试函数必须以 `test_` 开头；
- pytest 框架没有提供特殊的断言方法，直接使用 Python 的 assert 关键字。

需要注意的是，测试类不是必须的，在类之外的函数只要符合以 `test_` 开头的规范，也会被 pytest 测试框架检测到。同样，测试类中的测试方法也必须以 `test_` 开头。而非测试类（不以 `Test `开头）中的 `test_` 方法也不会被执行。

有两种方式运行 pytest 测试。**第一种**，在命令行中使用 `pytest` 命令，可以后接文件名指定待测文件，如果不指定，将测试当前文件夹下的所有符合命名规则的文件。 下面这条命令可以避免生成 pytest_cache 测试缓存文件。

```sh
pytest -p no:cacheprovider
```

**第二种**，在 main 函数运行 pytest，提供的接口是 `pytest.main()`，该方法接收一个参数数组。这样做的好处是可以在 IDE 中例如 PyCharm  中直接 run 起来或者 debug 调试，也可以方便地控制测试的粒度，可以只跑某个测试方法或者某个测试类（命令行通过参数也可以限定）。目前 PyCharm 集成的测试工具包括 unittest、pytest、Nosetests 和 Twisted Trial。

```
class TestClass:
    def test_one(self):
        assert 1 + 1 == 2

if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
```

如果测试都通过了，打印结果如下图所示，显示总共有 4 个单元测试，`.py` 右侧的 `.` 代表该文件中有几个测试方法，右侧的百分比代表的是测试进度，即已跑完的测试占总测试比例。

```
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /Users/s1mple/Projects/PycharmProjects/python-learning-lecture/lecture2
collected 4 items

test_example.py ...                                                      [ 75%]
vector_test.py .                                                         [100%]

============================== 4 passed in 0.01s ===============================
```

有趣的是，如果某个测试方法未通过（断言报错），上述的 `.` 会变为 `F`，表明文件中的第几个测试方法失败了，并在下面打印出错信息。如果断言的是一个简单的表达式，pytest 不会为你计算等式左侧的值，因为它相信你能一眼就看出问题所在。而如果断言是为了验证被调用的方法输出是否正确，pytest 则会提示你具体的出错位置，方便程序员定位问题。

```
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /Users/s1mple/Projects/PycharmProjects/python-learning-lecture/lecture2
collected 4 items

test_example.py .F.                                                      [ 75%]
vector_test.py F                                                         [100%]

=================================== FAILURES ===================================
____________________________ TestClass2.test_three _____________________________

self = <test_example.TestClass2 object at 0x110e157f0>

    def test_three(self):
>       assert 1.1 * 999 == 3
E       assert (1.1 * 999) == 3

test_example.py:15: AssertionError
____________________ TestVector.test_should_print_correctly ____________________

self = <vector_test.TestVector object at 0x110e15eb0>

    def test_should_print_correctly(self):
        v1 = Vector()
>       assert str(v1) == 'Vector(0,)'
E       AssertionError: assert 'Vector(0)' == 'Vector(0,)'
E         - Vector(0,)
E         ?         -
E         + Vector(0)

vector_test.py:8: AssertionError
=========================== short test summary info ============================
FAILED test_example.py::TestClass2::test_three - assert (1.1 * 999) == 3
FAILED vector_test.py::TestVector::test_should_print_correctly - AssertionErr...
========================= 2 failed, 2 passed in 0.04s ==========================
```

## 如何阅读 Python 源码

# Lecture 2

## 鸭子类型

## 重载特殊方法

## 重载运算符

在_Python 2_中，请始终记住也要重写`ne`函数

在_Python 3_中，这不再是必需的，因为https://docs.python.org/3/reference/datamodel.html#object.ne[documentation]指出：

_ 默认情况下，ne （）委托给eq （）并反转结果，除非结果为NotImplemented。 比较运算符之间没有其他隐含关系，例如，（x的真值并不意味着x ⇐ y。 _

## 生成式表达式 

## * 和 ** 运算符

# Lecture 3

## 函数是一等公民

虽然《流畅的Python》作者一再强调 Python 不是一门函数式编程语言，但它的的确确具备了一些函数式编程的特性。其中的一个重要特性是：Python 将**函数作为一等公民**。这与 JavaScript、Scala 等语言一样，意味着在这类语言中：**函数与其他数据类型处于同等地位，函数可以定义在函数内部，也可以作为函数的参数和返回值**。基于这个特性，我们可以很容易的定义高阶函数。来看一个 JavaScript 的例子：

```js
const add = function(x) {
  return function(y) {
    return x + y
  }
}
```

这个函数将一个函数作为了返回值，很明显它是一个高阶函数，那么问题来了：这样定义有什么作用或者是好处呢？事实上，这段代码是 JavaScript 中的一个优雅的函数式编程库 [Ramda](https://ramdajs.com/) 对于加法实现的基本思路（还需要可变参数以及参数个数判断）。最终我们可以这样去使用它：

```js
const R = require('ramda')
R.add(1, 2) // -> 3
const increment = R.add(1) // 返回一个函数
increment(2) // -> 3
R.add(1)(2) // -> 3
```

既可以像代码第二行一次性传入两个参数，也可以像代码第三、四行分两个阶段传入，这与代码第五行效果一致。我们将这种特性称为**函数柯里化（Currying）**，这样做的好处一是可以**代码重用**，就像特意将 `R.add(1)` 取名为 increment 一样，它可以单独地作为一个递增函数；二是可以实现**惰性求值**，只有当函数收集到了所有所需参数，才进行真正的计算并返回结果，这一点在许多流处理框架中有广泛使用。

Python 中的函数之所以可以作为一等公民，究其原因，是因为 Python 中的**一切皆是对象**，即 *Everything in Python is an object*。使用 `def` 关键字定义的任何函数，都是 `function` 类的一个实例。

```python
>>> def func():
...     pass
... 
>>> type(func)
<class 'function'>
```

既然函数是对象，那就可以持有属性，这也是为什么 Python 中函数可以持有外部定义的变量（也就是闭包问题）的根本原因。这一点与 Java 和 C++ 这类语言是有本质区别的。以 Java8 为例，虽然 Java8 提供了一些语法糖让我们得以编写所谓的“高阶函数”，但 Java 中的函数（方法）依然不能脱离类或者对象而存在：

```java
Arrays.asList(1, 2, 3, 4, 5)
        .stream()
        .filter(i -> i >= 3)
        .forEach(System.out::println);
```

上述代码第三行接收一个 Lambda 表达式作为参数，第四行接收一个方法引用，看上去函数可以作为参数传入。但实际上，Java 编译器会将它们转换为**函数接口（Functional Interfaces）**的具体实现，函数接口是 Java8 函数式编程引入的核心概念。例如上述代码中的 `System.out::println` 方法引用会被实例化为 Consumer 函数接口的具体实现，Consumer 是 Java8 提供的四类函数接口中的一类，称为消费者接口，它有一个 accept 抽象方法接受一个输入且返回值为空，编译器将会用 `System.out.println(t)` 重写这个方法。

```java
@FunctionalInterface
public interface Consumer<T> {
    void accept(T t);
    // ...
}    

// Consumer consumer = System.out::println;
// consumer.accept("hello");
```

所以在 Java8 中，看似函数可以作为参数传入，但实际上传入的依旧是类的实例。如果对 Java8 的函数式编程感兴趣可以参考这篇：[Java8 函数接口](https://s2mple.xyz/2018/11/16/Java8%20%E5%87%BD%E6%95%B0%E6%8E%A5%E5%8F%A3/)。

言归正传，既然已经清楚了 Python 中可以定义高阶函数，那么接下来就可以探讨一下 Python 怎么使用高阶函数实现装饰器的。但在这之前，不得不提及一下什么是闭包。

## 闭包

首先注意，只有涉及到**嵌套函数**才会存在闭包问题。而不要将闭包与匿名函数搞混，是不是匿名函数不是必要条件，只是人们通常将闭包与匿名函数搭配使用罢了（尤其是在 JavaScript 中）。

实际上，闭包是指**延伸了作用域的函数**，关键在于它**能够访问定义体之外定义的非全局变量**。听上去有些绕，不过看看下面这段代码就很好理解了：

```python
def make_average():
    series = []

    def average(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return average
```

关注点放在 series 这个变量。它定义在内层函数 average 之外并在内层函数中做了修改（末尾追加了一个值）。并且，内层函数被当作外层函数的返回值返回。显然，内层函数 average 设计出来是为了多次调用的，然而 series 是在内层函数之外定义的，当多次调用 average 时 series 作用域是否已经消亡了呢？答案是否。看看下面的输出：

```python
>>> avg = make_average()  # 返回 average 函数
>>> avg(1)  # (1) / 1
1.0
>>> avg(2)  # (1 + 2) / 2
1.5
>>> avg(3)  # (1 + 2 + 3) / 3
2.0
```

原因在于，上述代码中的 series 变量声明语句与 average 函数定义体构成了一个闭包，average 函数的作用域延伸到函数外部，换句话说，series 已经绑定到 average 函数对象上了。我们将 series 这种变量称为**自由变量**（free variable）。可以通过 Python 提供的内省属性访问：

```python
>>> avg.__code__.co_freevars
('series',)
>>> avg.__closure__
(<cell at 0x104301400: list object at 0x1041a9580>,)
>>> avg.__closure__[0].cell_contents
[1, 2, 3]
```

`__code__.co_freevars` 以元组形式存放了自由变量的**名称**。要想访问自由变量的值，需要通过 `__closure__` 属性，也就是说，实际上 series 是绑定到 `avg.__closure__` 中的。Python 在自由变量之上包装了一个 cell 对象，用 `cell_contents` 存放其真正的值。

## 装饰器

装饰器，又称函数装饰器，本质上是一个**可调用对象**（实现了 `__call__` 方法），可以是一个函数或者一个类。它接受一个函数作为参数，即被装饰的函数，可能会对这个函数进行处理然后将它返回，或者替换为另一个函数或可调用对象。我们先来看一个简单样例：

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

事实上，**大多数装饰器会在内部定义一个函数然后将其返回**，原封不动地返回被装饰的函数是没有多大用处的。接下来，我会为你展示一个稍微“实用”一点的例子 —— 定义一个 clock 计时器，记录被装饰函数的运行时间。在这个例子中，你将会看到闭包问题是如何在装饰器中体现的，以及如何定义并使用一个有参数的装饰器。

```python
def clock(unit=TimeUnit.SECONDS):  # ①
    def decorate(func):
        def clocked(*args, **kwargs):  # ②
            start = time.perf_counter()
            result = func(*args, **kwargs)  # ③
            end = time.perf_counter()
            arg_str = ', '.join(repr(arg) for arg in args)
            if unit == TimeUnit.SECONDS:
                print(f'running {func.__name__}({arg_str}): {end - start}s')
            else:
                print(f'running {func.__name__}({arg_str}): {(end - start) * 1000}ms')
            return result
        return clocked
    return decorate
```

首先，不要被上述代码的两层嵌套函数（共三层函数）吓到，你可能会有一个疑问：装饰器不是通常只有一层嵌套吗（定义一个内部函数然后将其返回），为什么这里会出现两层嵌套？实际上，这是一种**带参装饰器**的妥协，原因是**装饰器只能且必须接收一个函数作为参数**。在这三层函数中，最外层定义的 clock 函数是参数化装饰器**工厂函数**，内层的 decorate 函数才是真正的装饰器，clocked 函数则是包装了被装饰的函数（真正给被装饰函数附加功能）。

上述代码有几个需要注意的点，已经用带圈数字标注出来：

- ① 最外层的 clock 工厂函数接收一个名为 unit 的时间单位的参数，默认值为秒（这里采用枚举类型）；
- ② **如果被装饰的函数带参数，只需要把装饰器最内层函数跟被装饰函数的参数列表保持一致即可**。这里 clocked 函数接收任意个定位参数和仅限关键字参数，写成这样的目的是想体现 clock 计时器的泛用性，你可以在 ③ 处原封不动地将这些参数传给被装饰函数 func 调用；
- ③ func 实际上是定义在 clocked 外层的自由变量（作为 decorate 的参数传入），所以它已经被绑定到 clocked 的闭包中。

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

首先应当注意第一个空参装饰器 `@clock()`，其中的 `()` 是不能省略的，它使用了 `TimeUnit.SECONDS` 作为默认参数，这是在 clock 定义处声明的。此外，clock 装饰器中的参数并不是和函数名绑定的，打印的时间单位完全取决于传入 clock 装饰器的参数。比如，也可以让 sleep_ms 按照秒的格式打印时间：

```python
>>> @clock(unit=TimeUnit.SECONDS)
... def sleep_ms(ms):
...     time.sleep(ms / 1000)
... 
>>> sleep_ms(100)
running sleep_ms(100): 0.10072612899966771s
```

### 类装饰器

### 延伸：面向切面编程

