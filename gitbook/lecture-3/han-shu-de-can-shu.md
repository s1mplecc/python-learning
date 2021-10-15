# 函数的参数

Python 最好的特性之一就是提供了极为灵活的参数处理机制。除了基础的定位参数（positional argument）之外，Python 还支持传入关键字参数（keyword argument），如我们之前所使用的内置方法 `sorted()`，就支持关键字参数 key 与 reverse。关键字参数允许提供默认值，如果无默认值一般为 None。

```python
'''
Return a new list containing all items from the iterable in ascending order.
 
A custom key function can be supplied to customize the sort order, and the
reverse flag can be set to request the result in descending order.
'''
sorted(iterable, /, *, key=None, reverse=False)
```

`sorted()` 参数列表中的斜杠表示在它之前的形参是仅限定位参数，在传参时不能指定关键字，即不能使用 `sorted(iterable=...)` 的形式。参数列表中的星号表示之后的参数是仅限关键字参数，在使用时必须指定关键字，如 `sorted([], key=...)`。

Java 5 中引入了不定长参数，允许在形参后添加 `...` 表示该形参可以接收多个参数值，多个参数将被当做数组传入，如 `void foo(String... args)`。Python 也支持**不定长参数**，它的形式是在参数名称前添加星号运算符，如 `*args`，不定长参数将被打包成**元组**传入。除此之外，Python 还支持传入**非具名关键字参数**，即没有明确指定名称的关键字参数，如 `**kwargs`，参数将会被打包成一个**字典**传入。

```python
>>> def func(*args, **kwargs):
...     print('args: ', args)
...     print('kwargs: ', kwargs)
... 
>>> func(0, 'a', key1=1, key2='b') 
args: (0, 'a')
kwargs: {'key1': 1, 'key2': 'b'}
```

如果同时使用 `*args` 和 `**kwargs`，`*args` 参数必须要在 `**kwargs` 之前。它们可以与其他类型的参数混合使用，但**参数的顺序必须是：定位参数，默认参数，不定长参数，具名关键字参数和非具名关键字参数**。即如下形式：

```python
>>> def record(name, age=18, *phones, email=None, **other):
...     print('name: ', name)
...     print('age: ', age)
...     print('phones: ', phones)
...     print('email: ', email)
...     print('other: ', other)
... 
>>> record('Jack', 20, 123456, 654321, email='abc@email.com', height=180, weight=90)
name: Jack
age: 20
phones: (123456, 654321)
email: abc@email.com
other: {'height': 180, 'weight': 90}
```

其中，默认参数与具名关键字参数形式上一样，默认参数通常是用来简化函数调用者的传参的。这两者可以通过位置进行区分，在不定长参数之前的是默认参数，之后的是关键字参数。如果要传入不定长参数，默认参数就不能省略，此时默认参数被视为定位参数（默认值失去了意义），其后的非关键字参数会被不定长参数 `*phones` 捕获。如果省略了默认参数，那么不定长参数的第一个元素会被赋值给默认参数。具名关键字参数则没有这一限制。

```python
>>> record('Jack', 123456, 654321, height=180)
name:  Jack
age:  123456
phones:  (654321,)
email:  None
other:  {'height': 180}
```

**仅限关键字参数**（keyword-only argument）是 Python 3 新增的特性。如果定义函数时想指定仅限关键字参数，需要将它们放在带有 `*` 的不定长参数之后。如果不想支持不定长参数，可以在签名中放一个 `*`，标志着定位参数到此终结，之后的参数只能以关键字形式提供，即仅限关键字参数。如下所示：

```python
>>> def func(a, *, b, c=3): 
...     return a, b, c
... 
>>> func(1, b=2)
(1, 2, 3)
>>> func(1, b=2, c=4)
(1, 2, 4)
```

可以看到，仅限关键字参数不一定要有默认值，但如果没有默认值，调用函数时必须传入该参数。内置方法 `sorted()` 的参数就包含一个 `*`，其后的 key 和 reverse 参数就是带有默认值的仅限关键字参数。

#### 函数参数的最佳实践

对于函数参数如何正确的使用，《Effective Python》给出了一些建议。我结合自己的一些看法，给出如下几点建议。

第一点，**使用不定长参数减少视觉杂讯**。这是一种比喻，目的是使函数签名内容不要过于过多，而应凸显重要部分。如果一个函数支持传入多个相同类型的对象，或对不同类型的对象做相同处理，可以考虑不定长参数（或者组合成一个可迭代对象传入）。拿 Python 的内置方法来举例，`map()` 的最后一个参数就是不定长参数 `*iterables`，支持传入多个可迭代对象；`print()` 方法的第一个参数 `*values` 也是不定长参数，对于传入多个参数，不管它们是什么类型都能将其打印。

第二点，**使用关键字参数来表达可选的行为**。关键字参数的名称可以辅助调用者明确参数的用途，比如 `sorted()` 方法中的 reverse 参数用来反向排序。关键字参数还能提供默认值，就如同一个开关，如果使用函数默认功能，就不需要操心这些参数，还可以避免传参时的重复代码。如果想开启附加功能，可以传入指定的关键字参数。带有默认值的关键字参数还能在不改变调用代码的基础上为函数添加新功能，保证了代码的兼容性。从另一种角度看，带有默认值的关键字参数提供了类似多态重载的动态语言特性，虽然 Python 并不支持函数重载。

第三点，**使用仅限关键字参数来确保代码清晰**。关键字参数可以提高可读性，但不能保证调用者一定使用关键字来明确指出参数的含义，关键字参数可以通过位置来赋值，比如定义的函数 `def func(a, b=1)` 可以通过 `func(1, 2)` 来为关键字参数 b 赋值。如果有必要，可以使用仅限关键字参数来强制调用者使用关键字。比如 `sorted()` 方法签名 `*` 后指定的仅限关键字参数 key 和 reverse。

第四点，**不要使用可变类型作为参数的默认值**。如果想将参数默认值指定为空，应该使用 None，而绝不是可变序列 `[]` 和 `{}`。参数的默认值会在模块被加载时执行一次并绑定，如果默认值定义为了可变序列，那么以默认形式调用函数的代码都会共享同一份序列，从而导致难以预料的结果。比如如下解析 JSON 的函数，默认值为空字典，在解析出错时将其返回，导致两个对象共用一个字典。解决的方法是使用 None 作为参数默认值，在函数内重新赋值为空字典，并添加文档说明参数默认值的实际行为。如果参数默认值是动态变化的，如当前时间，也应如此做。总之，要避免参数默认值是可变的。

```python
>>> def decode(data, default={}):
...     try:
...         return json.loads(data)
...     except ValueError:
...         return default
... 
>>> foo = decode('bad data')
>>> bar = decode('also bad')
>>> foo['a'] = 1
>>> bar
{'a': 1}
>>> foo is bar
True
```

第五点，**纯函数应避免修改传入参数的值**。函数式编程中非常强调的一点是，函数要无副作用。无副作用指的是函数内部不与外部互动（最典型的情况是，修改全局变量的值），产生除函数本身运算以外的其他效果。函数无副作用，意味着函数要保持独立，不依赖于上下文环境，不得修改外部变量包括传入参数的值。即使函数要在传入参数本身上做运算，也应该新建一个副本将其返回。就拿 `sorted()` 来说，即使排序前后元素位置没有变化，也返回一个全新的列表。除此之外，`map()`、`filter()` 等其他内置方法也都遵循这一点，不对参数本身做修改。

```python
>>> l = [1, 2, 3]
>>> sorted(l)
[1, 2, 3]
>>> sorted(l) is l
False
```

第六点，**如果发生就地修改应返回 None**。如果一个函数或方法对对象进行了就地修改，那么它应该返回 None，以便让调用者知道传入的参数发生了改变，而且并未产生新的对象。例如，就地排序方法 `list.sort()` 和洗牌方法 `random.shuffle()`。

```python
>>> import random
>>> l = list(range(10))
>>> random.shuffle(l)
>>> l
[9, 8, 4, 1, 0, 7, 2, 3, 6, 5]
>>> list.sort(l)
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### 自定义的 `sorted()` 函数

在本章中我一直拿内置的 `sorted()` 函数来举例，不妨自己来实现一个。借此案例我想演示：如何使用仅限关键字参数，如何编写高阶函数，以及如何使用卫语句对异常参数进行处理。

这里的排序算法不是关键，使用的是最简单的冒泡排序算法。函数签名上尽可能与 `sorted()` 保持一致，为了保证函数无副作用，函数内部新建了一个列表副本保存传入可迭代序列的值。

```python
def sort(iterable, *, key=None, reverse=False):
    if key is not None and not callable(key):
        raise TypeError(f'{type(key)} object is not callable')

    _l = list(iterable)
    for i in range(len(_l)):
        for j in range(i):
            if key is None:
                if _l[j] > _l[i]:
                    _l[j], _l[i] = _l[i], _l[j]
            else:
                if key(_l[j]) > key(_l[i]):
                    _l[j], _l[i] = _l[i], _l[j]
    if reverse:
        _l.reverse()
    return _l
```

仅限关键字参数是指在 `*` 运算符之后定义的关键字参数，在调用时必须指定关键字名称，如上述函数中的 key 和 reverse 关键字。

在函数的开头，首先判断传入的 key 参数在非 None 情况下是否是可调用的，若不可调用则抛出 TypeError 异常。这种 if 条件分支语句叫做**卫语句**（guard clause），目的是将可能出错的每个分支做单独检查，要么抛出异常要么立即返回。通过在函数头部的集中处理及早抛出各种可能的异常（又称迅速失败），避免无效的运算。函数真正的实现代码放在卫语句之后，保证运行到此处时所有条件都已通过。

通过了卫语句检测的 key 参数是可调用的，在函数内部直接使用 `key()` 调用。对于接收函数作为参数的 `sort()` 函数，我们将其称之为**高阶函数**，这也是 Python 函数式编程特性之一。

下面是测试方法：

```python
def test_should_sort_number_sequence(self):
    _l = [1, 5, 3, 2, 7, 4]
    result = [1, 2, 3, 4, 5, 7]
    assert sort(_l) == result

def test_should_sort_sequence_with_key_function(self):
    _l = ['a', 'aab', 'ab', 'aabb']
    result = ['a', 'ab', 'aab', 'aabb']
    assert sort(_l, key=len) == result

def test_should_sort_sequence_with_key_function_and_reverse(self):
    _l = ['a', 'aab', 'ab', 'aabb']
    result = ['aabb', 'aab', 'ab', 'a']
    assert sort(_l, key=len, reverse=True) == result

def test_should_raise_error_when_key_function_is_not_callable(self):
    _l = [1, 5, 3, 2, 7, 4]
    with pytest.raises(TypeError) as e:
        sort(_l, key=1)
```

pytest 框架支持对抛出异常的测试，使用 with 语句加 `pytest.raises()` 方法可以断言定义体内调用的方法是否会抛出对应的异常。

#### `*` 与 `**` 运算符

在 Python 中，`*` 与 `**` 运算符除了能用作数学运算符中的乘法和乘方之外，还有一些其他的巧妙用法。之前讨论的函数中的不定长参数 `*args` 和不具名关键字参数 `**kwargs` 是它们的经典用法之一。此外，这两个运算符还可以用来对参数列表进行**拆包**。

运用 `*` 运算符可以把一个可迭代对象拆开作为函数的参数：

```python
>>> def func(a, b):
...     print(f'a={a}, b={b}')
... 
>>> func(1, 2)
a=1, b=2
>>> t = (1, 2)
>>> func(*t)
a=1, b=2
```

类似的，运用 `**` 运算符可以把一个字典拆开作为函数的参数，同名键会绑定到对应的具名参数上，如果函数还定义了非具名关键字参数 `**kwargs`，除了绑定的同名键外余下参数会被 `**kwargs` 捕获。

```python
>>> def func(a=None, b=None, **kwargs):
...     print(f'a={a}, b={b}, kwargs={kwargs}')
... 
>>> d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
>>> func(**d)
a=1, b=2, kwargs={'c': 3, 'd': 4}
```

`*` 运算符对于函数参数中的可迭代对象拆包概念，在 Python 3 被扩展到了**平行赋值**。在平行赋值中，`*` 前缀只能被用在一个变量名前，但这个变量可以出现在赋值表达式的任何位置，用来处理剩下的元素。拆包所赋值的元素是列表类型，即使其中只有一个元素。

```python
>>> a, b, *rest = range(5)
>>> a, b, rest
(0, 1, [2, 3, 4])
>>> a, *rest, d, e = range(5)
>>> a, rest, d, e
(0, [1, 2], 3, 4)
>>> a, *rest, c, d, e = range(5)
>>> a, rest, c, d, e
(0, [1], 2, 3, 4)
```
