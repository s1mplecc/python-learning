## 前言

在写该系列时我正在阅读《流畅的 Python》这本书，首先夸一下这本书，这本书不仅囊括了 Python 的诸多特性，而且为我们展示了一种 Python 设计思想，一种与我之前接触的 Java OOP 截然不同的思想，比如 Python 内置了许多特殊方法或者叫魔法方法（magic methods），又比如“鸭子类型”：只要表现的像一个序列，那么就可以对它进行迭代，等等。总的来说，Python 有它自己的设计风格，它是一门注重实用，专为程序员高效编码而生的语言。我相信随着对这本书的深入阅读和更多 Python 的编码实践，我能够对 Python 这门语言有一些更多感悟。

当然，“光看不练假把式”，最开始的时候，我只是在命令行中去验证一些 Python 特性，随后我意识到这远远不够，为什么不将学习中的零碎知识点加以整理做成一个系列呢？于是，该系列诞生了。由于知识点的离散性，所以对 Lecture 的划分就显得有些随心所欲，我尽量在目录中将知识点的名称罗列出来。

代码已经托管到 Github 上，链接：https://github.com/s1mplecc/python-learning-lectures

如果你是在 PyCharm 中运行示例代码，那么 import 语句可能会有恼人的红色报错，但其实是可以正常运行的。只需要将子目录标记为源代码根目录，即 Mark Directory as Sources Root。

## Table of Contents

* [Lecture 1](#lecture-1)
  * [使用 pytest 做单元测试](#%E4%BD%BF%E7%94%A8-pytest-%E5%81%9A%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95)
  * [重载运算符](#%E9%87%8D%E8%BD%BD%E8%BF%90%E7%AE%97%E7%AC%A6)
* [Lecture 2](#lecture-2)

## Lecture 1

以单元测试作为系列学习的开始，应当还算合理。我想尽量给这个学习系列带入些测试驱动的思想，一方面，熟练掌握一门语言的过程其实是特性累积的过程，今天学习了 Python 重载运算符，明天学习如何编写 Python 装饰器，这样看来，每次编写一个单元测试用于验证一个语言特性最适合不过了（当然可能不止需要一个单元测试）。另一方面，如果验证结果的时候还是使用一堆 print 方法，就会显得相当凌乱而且不那么专业，而通过运行测试时打印的一系列方法名，可以清楚这些模块涉及了哪些 Python 特性。

尽管我的测试方法命名不严格遵循 TDD 中的  “Given-When-Then” 格式，但是通过 `should_` 这种命名规范，也可以清晰的明白某个测试用例测试了什么功能。比如，看到 `test_should_add_two_vectors_with_add_operator()`，你可能能猜到这个测试用例测试的是加法运算符的重载。

### 使用 pytest 做单元测试

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

### 重载运算符

在_Python 2_中，请始终记住也要重写`ne`函数

在_Python 3_中，这不再是必需的，因为https://docs.python.org/3/reference/datamodel.html#object.ne[documentation]指出：

_ 默认情况下，ne （）委托给eq （）并反转结果，除非结果为NotImplemented。 比较运算符之间没有其他隐含关系，例如，（x的真值并不意味着x ⇐ y。 _

### 生成式表达式 

### * 和 ** 运算符



## Lecture 2

### 鸭子类型

### 重载特殊方法

## Lecture 3

### 闭包

### 装饰器

### 注解