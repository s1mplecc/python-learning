Table of Contents
=================

* [前言](#%E5%89%8D%E8%A8%80)
* [Lecture 1](#lecture-1)
  * [使用 pytest 做单元测试](#%E4%BD%BF%E7%94%A8-pytest-%E5%81%9A%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95)
  * [重载运算符](#%E9%87%8D%E8%BD%BD%E8%BF%90%E7%AE%97%E7%AC%A6)
* [Lecture 2](#lecture-2)

## 前言

## Lecture 1

### 使用 pytest 做单元测试

编写 pytest 测试样例需要符合的规范：

- 测试文件必须以 `test_` 开头或结尾；
- 测试类必须以以 `Test` 开头，且不能含有 `__init__` 构造函数；
- 测试函数必须以 `test_` 开头；
- pytest 框架没有提供特殊的断言方法，直接使用 Python 的 assert 关键字。

需要注意的是，测试类不是必须的，在类之外的函数只要符合以 `test_` 开头的规范，就会被 pytest 测试框架检测到。同样，测试类中的测试方法也必须以 `test_` 开头。而非测试类（不以 `Test `开头）中的 `test_` 方法也不会被执行。

有两种方式运行 pytest 测试。**第一种**，在命令行中使用 `pytest` 命令，可以后接文件名指定待测文件，如果不指定，将测试当前文件夹下的所有符合命名规则的文件。 下面这条命令可以避免生成 pytest_cache 测试缓存文件：

```sh
pytest -p no:cacheprovider
```

**第二种**，在 main 函数运行 pytest，提供的接口是 `pytest.main()`，该方法接收一个参数数组，本质上等同于在命令行执行。这样做的好处是可以在 IDE 中例如 PyCharm  中直接 run 起来或者 debug 调试。另外需要注意的是，如果使用这种方法运行测试，实际测试覆盖的范围是与第一种方法相同的，即**当前文件夹下所有符合命名规范的测试，而不只是当前 main 函数所在的文件**。

```
class TestClass:
    def test_one(self):
        assert 1 + 1 == 2

if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
```

如果测试都通过了，打印结果如下图所示，显示总共有 4 个单元测试，`.py` 右侧的 `.` 代表该文件中有几个测试方法，右侧的百分比代表的是测试进度，即以跑完的测试占总测试比例。

```
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /Users/s1mple/Projects/PycharmProjects/python-learning/lecture2
collected 4 items

test_example.py ...                                                      [ 75%]
vector_test.py .                                                         [100%]

============================== 4 passed in 0.01s ===============================
```

有趣的是，如果某个测试方法未通过（断言报错），上述的 `.` 会变为 `F`，表明文件中的第几个测试方法 Failed 了，并在下面打印出错信息。如果断言的是一个简单的表达式，pytest 不会为你计算等式左侧的值，因为它相信你能一眼就看出问题所在。而如果断言是为了验证被调用的方法输出是否正确，pytest 则会提示你具体的出错位置，方便程序员定位问题。

```
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /Users/s1mple/Projects/PycharmProjects/python-learning/lecture2
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

## Lecture 2