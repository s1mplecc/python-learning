# lambda 表达式

Python 中的 lambda 关键字用于创建**匿名函数**。lambda 表达式的格式如下：

```python
lambda arguments : statement
```

表达式以 lambda 关键字开头，冒号 ":" 左侧是函数的**传入参数**，当有多个入参时使用逗号划分开，冒号右侧是**返回值**的表达式语句，函数会根据表达式计算结果并将其返回。lambda 表达式会创建一个函数对象，可以对其赋值并如同普通函数一样使用。下面定义了一个求平方的 lambda 表达式：

```python
>>> square = lambda x : x * x
>>> square
<function <lambda> at 0x101631e50>
>>> square(3)
9
```

lambda 句法只是语法糖，上述定义的 lambda 表达式与如下使用 def 关键字定义的普通函数没有本质区别，甚至 lambda 表达式的功能要更加受限。由于 Python 简单的句法限制了 lambda 定义体只能使用纯表达式，不能进行赋值，也不能使用 while 和 try 等 Python 语句。

```python
>>> def square(x):
...     return x * x
... 
>>> square
<function square at 0x101631dc0>
```

在 Python 中，**lambda 表达式的通常作用是作为参数传入给高阶函数**。比如在列表推导一节介绍的 map、filter 和 reduce 函数，这些函数接收一个函数作为参数，如果不想额外定义函数，那么使用 lambda 表达式创建匿名函数就是最佳的应用场景。

```python
>>> list(map(lambda x : x * x, [1, 2, 3]))
[1, 4, 9]
>>> list(filter(lambda x : x < 2, [1, 2, 3]))
[1]
```

除了上述这种应用场景之外，Python 很少使用匿名函数。受到句法的限制，lambda 表达式无法实现复杂的函数功能。同时，在使用 lambda 表达式时要尽可能保证表达式的清晰简短，否则冗长的 lambda 表达式将会导致代码难以阅读。此时，应该使用 def 关键字创建普通函数，即《Effective Python》所提倡的：**使用辅助函数来取代复杂的表达式**，并赋予函数清晰的名称以提高代码可读性。
