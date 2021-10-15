# map、filter 与列表推导

列表是 Python 中非常重要且常用的内置类型，列表被注册为可变序列的虚拟子类，`MutableSequence.register(list)`，所以列表的性质与可变序列性质相符，可以阅读 `collections.abc` 模块中 MutableSequence 类的源码进行了解。列表的性质不做过多介绍，这一节我想介绍一下列表推导。在上一节中就曾经使用 `all()`、`any()` 方法结合列表推导，巧妙地展示了哪些内置类型是序列类的子类。

在介绍列表推导之前，有必要先介绍以下几个函数：`map()`、`filter()` 和 `reduce()` 函数。这几个函数是函数式编程的范例函数。它们都是用于处理可迭代序列的基本函数，所以被视为可迭代数据集函数式编程的基石，包含了数据集的映射、过滤和规约三个思想。所有支持函数式编程的语言都提供了这些函数的接口。Java 8 新增的 Stream API 配合箭头函数可以写出很优雅的链式函数，同样，JavaScript 中也支持链式写法：

```js
> l = [1, 2, 3, 4, 5]
[ 1, 2, 3, 4, 5 ]
> l.map(x => x * x)
[ 1, 4, 9, 16, 25 ]
> l.map(x => x * x).filter(x => x > 10)
[ 16, 25 ]
> l.map(x => x * x).filter(x => x > 10).reduce((x, y) => x + y)
41
```

相比之下，Python 中的写法就不那么优雅了，map、filter 和 reduce 函数作为内置库或者标准库中的函数提供，序列本身并没有实现这些方法，所以不能通过 dot 运算符直接调用，而需要将序列作为这些函数的参数传入。

#### `map()`

> `map(func, *iterables) --> map object`
>
> Make an iterator that computes the function using arguments from each of the iterables. Stops when the shortest iterable is exhausted.

map 函数，又称映射函数，定义在内置模块 builtins 模块中。map 函数将可迭代对象的每个元素依次应用于 func 函数进行映射，返回的 map object 是一个可以依次产出映射后元素的生成器对象，可以使用 `list()` 包装一次性输出。传入的函数 func 可以是预先定义好的函数，也可以是 lambda 表达式定义的匿名函数。

```python
>>> def square(x):
...     return x * x
... 
>>> map(square, range(10))
<map object at 0x106ebb910>
>>> list(map(square, range(10)))
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> list(map(lambda x: x * x, range(10)))
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

从函数签名来看，map 函数能够接受多个可迭代对象，映射时将依次从每个可迭代对象中各取出一个元素应用于 func 函数，因此 func 也须接受同样数量的参数。如果这些可迭代对象的元素个数不一致，以个数最少的为标杆，即个数最少的可迭代对象遍历完毕时终止迭代。

```python
>>> list(map(lambda x, y: x * y, range(5), range(1, 6)))
[0, 2, 6, 12, 20]
>>> list(map(lambda x, y: x * y, range(10), range(1, 6)))
[0, 2, 6, 12, 20]
```

#### `filter()`

> `filter(function or None, iterable) --> filter object`
>
> Return an iterator yielding those items of iterable for which function(item) is true. If function is None, return the items that are true.

filter 函数，又称过滤函数，定义在内置模块 builtins 模块中。过滤函数将可迭代对象中的每个元素应用于谓词函数 function 后为 True 的保留下来。返回的 filter object 也是一个生成器对象，可以依次产出过滤后为真的元素。如果 function 为 None，直接判断元素是否为真值。

```python
>>> list(filter(lambda x: x > 5, range(10)))
[6, 7, 8, 9]
>>> list(filter(None, [0, 1, True, False, 0.0, -1, [], (1, 2)]))
[1, True, -1, (1, 2)]
```

#### `reduce()`

> `reduce(function, sequence[, initial]) -> value`
>
> Apply a function of two arguments cumulatively to the items of a sequence, from left to right, so as to reduce the sequence to a single value. For example, reduce(lambda x, y: x + y, \[1, 2, 3, 4, 5]) calculates ((((1 + 2) + 3) + 4) + 5). If initial is present, it is placed before the items of the sequence in the calculation, and serves as a default when the sequence is empty.

reduce 函数，又称规约函数，定义在 functools 模块中。规约函数的参数除了函数和序列之外，还接收一个可选的初始值。规约函数会将一个序列从左至右逐步规约为一个值。参数 function 接收两个参数，第一个参数代表每步规约后的累积值（首次规约为初始值），第二个参数代表每次迭代的序列中的元素，返回值为规约的结果，作为下一步规约的第一个参数传入。也就是说，function 函数的第一个参数、每步规约的返回值和 reduce 函数的返回值应为同一类型，function 的第二个参数为迭代序列的元素类型，两者可以是相同类型也可以是不同类型。

```python
>>> from functools import reduce
>>> reduce(lambda x, y: x + y, range(10))
45
>>> def concat_string(s, ch):
...     return s + str(ch)
... 
>>> reduce(concat_string, ['a', 1, 'b'], '0')
'0a1b'
```

#### 列表推导

如果想像 JavaScript 代码演示的那样，依次对一个序列数据流进行映射、过滤和规约操作，Python 的写法会显得不那么优雅。由于序列必须作为参数传入，无法放在左侧使用 dot 运算符进行链式书写，我们不得不编写多层嵌套的表达式：

```python
>>> import operator
>>> from functools import reduce
>>> list(filter(lambda x: x < 50, map(lambda x: x * x, range(10))))
[0, 1, 4, 9, 16, 25, 36, 49]
>>> reduce(operator.add, (filter(lambda x: x < 50, map(lambda x: x**2, range(10)))))
140
```

且不说冗余的 lambda 关键字，即使预先定义了函数使用函数名代替，整个表达式从右至左的执行循序也会不利于理解。所幸的是，Python 提供了一种精炼的表达式，来代替多层嵌套下纠缠不清的 map 和 filter 方法，那就是**列表推导**（list comprehension）。

列表推导是一个语法糖，可以根据可迭代对象构建出一个新的列表。列表推导使用一对中括号 "\[]"，内部至少包含一个 for 循环表达式，对应 map 方法；以及可选的 if 条件表达式，对应 filter 方法。列表推导返回的是列表类型。

```python
>>> [x * x for x in range(10)]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> [x * x for x in range(10) if x < 5]
[0, 1, 4, 9, 16]
>>> [_ * _ for _ in range(10) if _ < 5]
[0, 1, 4, 9, 16]
>>> [x * y for x in range(1, 3) for y in ('a', 'b', 'c')]
['a', 'b', 'c', 'aa', 'bb', 'cc']
>>> [x for y in [(1, 2), (3, 4), (5,)] for x in y]
[1, 2, 3, 4, 5]
```

表达式内的变量是一个局部变量，作用域仅限于该列表推导表达式。但 Python2 中的列表推导存在变量泄漏问题，表达式内的变量会影响到上下文中的同名变量，在 Python 3 中这个缺陷已被修复。

列表推导也支持**多重循环**，即多个 for 循环表达式，这些 for 表达式会按照从左至右的顺序来嵌套。与多层嵌套的 for 循环函数一致，先定义（左侧）的 for 循环在外层，后定义（右侧）的 for 循环在内层。外层定义的变量可用作内层的 for 循环，如上述代码中的最后一个列表推导式。如果用函数形式书写，那么代码如下：

```python
>>> [x for y in [(1, 2), (3, 4), (5,)] for x in y]
[1, 2, 3, 4, 5]
>>> def flat():
...     for y in [(1, 2), (3, 4), (5,)]:
...         for x in y:
...             yield x
... 
>>> list(flat())
[1, 2, 3, 4, 5]
```

字典和集合也有类似的推导机制，可以通过这些推导机制创建衍生的数据结构。字典推导可以从任何以键值对为元素的可迭代对象中构建出字典。集合推导可以从可迭代对象中去除重复元素，构建集合。

```python
>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> {i: j for j, i in d.items()}  # 字典推导
{1: 'a', 2: 'b', 3: 'c'}
>>> {i for i in d.keys()}  # 集合推导
{'a', 'c', 'b'}
```

**列表推导的最佳实践**

使用列表推导的原则是：**只用于创建新的列表，并且尽量保持简短，不建议使用含有两个以上表达式的列表推导**。依照函数式编程中的纯函数定义，函数不应该对传入的参数进行修改，否则会产生副作用。所以列表推导不该对传入序列做修改，而应该只用于创建新的列表。尽量保持简短则是出于可读性的考量。如果包含两个较长的表达式，可以考虑拆分为两行。Python 会忽略 \[]、{} 和 () 中换行，所以可以省略不太好看的续行符 \。

```python
>>> [(i, j) for i in range(2)
...         for j in range(3)]
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
```

如果列表推导式过长，就要考虑是否需要使用函数形式改写，有时命名清晰且带有缩进的函数可读性要更高。

列表推导也不是银弹，相较于生成器表达式的惰性求值，它会**及早求值**（eager evaluation）。在声明了一个列表推导式时，序列中的所有数据都会被即时处理，并将处理后的完整列表存放在内存中。并且在推导过程中，对于输入序列的每个值都可能创建一个仅含一项元素的全新列表。所以当序列的数据量很大时，如读文件或读数据库，将会消耗大量内存并导致程序崩溃。所以，列表推导另一个最佳实践是：**使用生成器表达式代替数据量较大的列表推导**。生成式表达式将在后续章节进行介绍。
