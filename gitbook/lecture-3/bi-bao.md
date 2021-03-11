# 闭包

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

