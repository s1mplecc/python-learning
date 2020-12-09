## Lecture 1

## Lecture 2

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

有趣的是，如果某个测试方法未通过（断言报错），上述的 `.` 会变为 `F`，表明是 test_example.py 文件中的第二个测试方法未通过，并在下面打印具体的出错信息。但 pytest 框架并不会告诉你

```
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /Users/s1mple/Projects/PycharmProjects/python-learning/lecture2
collected 4 items

test_example.py .F.                                                      [ 75%]
vector_test.py .                                                         [100%]

=================================== FAILURES ===================================
____________________________ TestClass2.test_three _____________________________

self = <test_example.TestClass2 object at 0x104e6c880>

    def test_three(self):
>       assert 1 + 1 == 3
E       assert (1 + 1) == 3

test_example.py:15: AssertionError
=========================== short test summary info ============================
FAILED test_example.py::TestClass2::test_three - assert (1 + 1) == 3
========================= 1 failed, 3 passed in 0.03s ==========================
```

