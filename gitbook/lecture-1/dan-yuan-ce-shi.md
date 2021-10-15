# 单元测试

### 前言

我已经不止一次被强调单元测试的重要性，单元测试作为一个黑盒接受输入验证输出，可以有效的测试一个方法的健壮性。此外，我想尽量给这个学习系列带入些测试驱动的思想。所以以单元测试作为特性学习的开始，应当还算合理。一方面，熟练掌握一门语言其实是语言特性掌握的累积，为了验证一个特性而编写一个单元测试看来最适合不过了（当然可能不止需要一个单元测试）。另一方面，如果验证结果的时候还是使用一堆 print 方法，就会显得相当凌乱而且不那么专业，而通过运行测试时打印的一系列方法名，可以清楚这些模块涉及了哪些 Python 特性。

### 使用 pytest 编写测试用例

选择 pytest 作为单元测试框架，是因为它简单实用。我个人不太欣赏 Python 自带的 unittest 模块的写法，测试类需要继承一个测试基类，并且到处充斥着 `self`。而 pytest 编写的测试用例只需要符合一定的命名规范，就会被框架自动检测到并运行。此外 pytest 还重写了 assert 关键字，打印信息也更加人性化。

**编写 pytest 测试用例需要符合如下规范**：

* 测试文件如果不指定，必须以 `test_` 开头或结尾；
* 测试类必须以以 `Test` 开头，且不能含有 `__init__` 构造函数；
* 测试函数必须以 `test_` 开头；
* 断言使用 Python 原生的 assert 关键字，pytest 框架没有提供特殊的断言方法。

需要注意的是，测试类不是必须的，在类之外的函数只要符合以 `test_` 开头的规范，也会被 pytest 测试框架检测到。同样，测试类中的测试方法也必须以 `test_` 开头。而非测试类（不以 `Test `开头的类）中的 `test_` 方法也不会被执行。

pytest 不包含在 Python 标准库中，需要另行安装依赖。有两种方式运行 pytest 测试。**第一种**，在命令行中使用 `pytest` 命令，可以后接文件名指定待测文件，如果不指定，将测试当前文件夹下的所有符合命名规则的文件。下面这条命令可以避免生成 pytest_cache 测试缓存文件。

```
pytest -p no:cacheprovider
```

**第二种**，在 main 函数中运行 pytest，提供的接口是 `pytest.main()`，该方法接收一个参数数组。这样做的好处是可以在 PyCharm 等 IDE 中直接 run 或者 debug 调试，也可以方便地控制测试的粒度，譬如只跑某个测试方法或者某个测试类（命令行通过参数也可以限定）。除了 pytest，目前 PyCharm 2020 版本集成的测试工具还包括 原生的 unittest、Nosetests 以及 Twisted Trial。

```python
import pytest

class TestClass:
    def test_one(self):
        assert 1 + 1 == 2

if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
```

如果测试均通过了，打印结果如下图所示，以 `.` 代表文件中成功通过的测试方法，右侧的百分比代表的是测试进度，即已跑完的测试占总测试比例。

```
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /Users/s1mple/Projects/PycharmProjects/python-learning-lecture/lecture2
collected 4 items

test_example.py ...                                                      [ 75%]
vector_test.py .                                                         [100%]

============================== 4 passed in 0.01s ===============================
```

如果某个测试方法未通过（断言报错），pytest 会提示你具体的出错位置，方便定位问题。

```
=================================== FAILURES ===================================
____________________ TestVector.test_should_print_correctly ____________________

self = <vector_test.TestVector object at 0x110e15eb0>

    def test_should_print_correctly(self):
        v1 = Vector()
>       assert str(v1) == 'Vector(0,)'
E       AssertionError: assert 'Vector(0)' == 'Vector(0,)'
E         - Vector(0,)
E         ?         -
E         + Vector(0)
```

**关于测试用例命名**：尽管我的测试用例命名不严格遵循 TDD 中的 “Given-When-Then” 格式，但是通过 “should + 下划线”这种命名规范，也可以清晰的明白某个测试用例测试了什么功能。比如，看到 `test_should_add_two_vectors_with_add_operator()`，你可能能猜到这个测试用例测试的是加法运算符的重载。
