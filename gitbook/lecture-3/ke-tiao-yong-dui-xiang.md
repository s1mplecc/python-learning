# 可调用对象

除了用户定义的函数，调用运算符，即 "()" 括号对，还能应用到其他对象上。我们将能应用调用运算符的对象称为**可调用对象**，通过内置的 `callable()` 方法可以判断对象是否是可调用对象。在 Python 3 的[数据模型文档](https://docs.python.org/3/reference/datamodel.html)中，一共列出了 7 种可调用对象：

* **内置函数和内置方法**：使用 C 语言（CPython）实现的函数和方法，如 `len()` 和 `alist.append()`；
* **用户定义的函数**：包括使用 def 创建的普通函数和 lambda 创建的匿名函数；
* **实例方法与类方法**：定义在类中的方法，实例方法是指第一个参数为 `self` 的方法，类方法是指第一个参数为 `cls` 的方法；
* **类**：对类使用调用运算符，如 `C()`，会执行类的 `__new__` 方法创建类的实例，然后执行 `__init__` 初始化；
* **类的实例**：如果类定义了 `__call__` 方法，那它的实例可以作为函数调用；
* **生成器函数**：内部使用了 yield 关键字的函数，调用生成器函数会返回生成器对象；
* **协程函数和异步生成器函数**：从 Python 3.5 开始支持使用 `async def` 关键字来定义协程函数，如果内部包含 yield 关键字则被称为异步生成器函数。该函数被调用时会返回一个异步迭代器对象。

#### 自定义的可调用类型

在装饰器一节，我们已经认识到了，装饰器不仅可以是函数，也可以是类。任何类只要实现了 `__call__` 方法，那它就是可调用对象，就可以表现的如同函数。因此，我们可以编写用户自定义的可调用类型，将其用在任何期待函数的地方。下面我将通过 Java 和 Python 两种语言，展现它们在可调用类型上的异同。

假设现有一副扑克，要求按照 `A, 2 ~ 10, J, Q, K` 的顺序进行排序。在 Java 中，可以通过 `Collections.sort()` 集合类的接口对一个集合进行排序。Python 也提供了内置的 `sorted()` 方法，对可迭代对象进行排序。但两种语言都不支持直接对字符串和数字类型进行比较，所以还需要实现特定的排序逻辑。

Java 中要实现排序逻辑通常有两种方法。一种是让类实现 Comparable 接口，重写其中的 `compareTo()` 抽象方法：

```java
public class Poker implements Comparable<Poker> {
    @Override
    public int compareTo(Poker otherPoker) {
        // return ...
    }
}
```

这里重点想展示第二种方法：新建一个实现了 Comparator 接口的比较器类，重写其 `compare()` 抽象方法。

```java
public class PokerComparator implements Comparator<Poker> {
    @Override
    public int compare(Poker firstPoker, Poker secondPoker) {
       // return ...
    }
}

PokerComparator pokerComparator = new PokerComparator();
Collections.sort(pokers, pokerComparator);
```

对于这种方法，需要将比较器对象作为第二个参数传入 `Collections.sort()` 接口中。由于 Java 对象不能将函数作为参数的限制，我们定义了一个辅助类，实际上这个类对我们而言只有一个方法有用，那就是 `compare()` 方法，`Collections.sort()` 接口会去调用该方法，所以它就是对应的排序逻辑，只不过是用类实现的。

Python 的函数可以直接作为参数传递，但我们接下来要讲的是如何定义一个类似 Comparator 的类，让它能实现排序逻辑。

Python 内置的排序方法 `sorted()`，**允许接收一个关键字参数 key 作为排序的键**，比如 `key=len` 时依照元素的长度进行排序。对于扑克牌 A \~ K，可以维护一个映射数字类型的字典，比如将 'K' 映射到 13，排序时直接通过映射的数值大小排序。维护一个字典，函数当然可以做到，但将其作为类的属性更加合适。可以定义一个扑克序列类，在初始化这个类时就构建好字典。为了让类可被调用，还需要实现 `__call__` 方法，直接返回字典中扑克牌对应的数值作为排序的键。

```python
class PokerOrder:
    def __init__(self):
        self._seq = {str(i): i for i in range(2, 11)}
        self._seq.setdefault('J', 11)
        self._seq.setdefault('Q', 12)
        self._seq.setdefault('K', 13)
        self._seq.setdefault('A', 1)

    def __call__(self, item):
        return self._seq.get(item)

    def show(self):
        print(self._seq)
```

由于 PokerOrder 类实现了 `__call__` 方法，它的实例会被 `callable()` 方法判定为可调用对象，可以直接应用调用运算符，传入扑克牌值返回对应数值。在排序时，将 PokerOrder 类的实例作为关键字传入，相当于将序列中的每项元素执行 `__call__` 方法返回的值作为键进行排序。

```python
>>> pokerorder = PokerOrder()
>>> pokerorder.show()
{'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1}
>>> callable(pokerorder)
True
>>> pokerorder('K')
13
>>> sorted(['K', '3', 'A', '7', 'J', 'Q', '2'], key=pokerorder)
['A', '2', '3', '7', 'J', 'Q', 'K']
```

将类定义为可调用类型，不仅能维护内部属性，还能自定义方法，比如如上代码中的 `show()` 方法。除此之外，在实现更复杂的排序逻辑时，比如按照花色排序等，使用类要比使用函数更合适。甚至如果你觉的 PokerOrder 类应该被实现为单例模式，还可以添加 `__new__` 方法保证创建类中的字典只会被创建一次。
