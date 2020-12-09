## Lecture 1

## Lecture 2

### 使用 pytest 做单元测试

编写pytest测试样例非常简单，只需要按照下面的规则：

- 测试文件以test_开头（以_test结尾也可以）
- 测试类必须以以 `Test` 开头，且不能含有 `__init__` 构造函数
- 测试函数必须以 `test_` 开头
- 断言使用 Python 的 assert 关键字即可

使用该命令可以避免生成 pytest_cache 测试缓存文件

```sh
pytest -p no:cacheprovider
```

在 PyCharm 中可以以如下方式运行测试，测试类名

```
class TestClass:
    def test_one(self):
        assert 1 + 1 == 2

if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
```