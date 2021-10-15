# 函数对象与方法对象

Python 中一切皆对象，不管是函数还是类中定义的方法都是对象。对于类中的实例方法来说，通过类访问该实例方法，如 `C.foo`，会返回一个**函数对象**，即 `function` 类型；通过实例访问实例方法，如 `c.foo`，会返回一个**绑定方法对象**，即 `method` 类型，该方法对象绑定在实例上。对于类方法而言，无论是通过类还是实例访问，都返回绑定方法对象，该方法对象绑定在类上。

```python
>>> class C:
...     def foo(self, x): print(x)
...     @classmethod
...     def bar(cls, x): print(x)
... 
>>> C.foo
<function C.foo at 0x10d613f70>
>>> type(C.foo)
<class 'function'>
>>> c = C()
>>> c
<__main__.C object at 0x10b0a5820>
>>> c.foo
<bound method C.foo of <__main__.C object at 0x10b0a5820>>
>>> type(c.foo)
<class 'method'>
>>> C.bar
<bound method C.bar of <class '__main__.C'>>
>>> c.bar
<bound method C.bar of <class '__main__.C'>>
```

方法对象中包含一些特殊的只读属性：

* `__self__` 为类实例对象本身；
* `__func__` 为函数对象；
* `__doc__` 为方法的文档，与 `__func__.__doc__` 作用相同；
* `__name__` 为方法名称，与 `__func__.__name__` 作用相同；
* `__module__` 为方法所属模块的名称，没有则为 None。

**访问方法对象的 `__func__` 属性会获得函数对象**。虽然两者都能通过调用运算符 "()" 调用，但函数对象还需要手动传入第一个位置的参数，即 `self` 和 `cls` 参数，方法对象则不需要。原因在于，**调用方法对象会调用对应的下层函数对象 `__func__`，并将 `__self__` 参数插入到参数列表的开头**，如果是实例方法则插入类实例，如果是类方法则插入类本身。

```python
>>> class C:
...     def foo(self, x): print(x)
...     @classmethod
...     def bar(cls, x): print(x)
... 
>>> c = C()
>>> c.foo(1)
1
>>> c.foo.__func__(c, 1)
1
>>> C.bar(1)
1
>>> C.bar.__func__(C, 1)
1
```

就如同上述代码所展示的，对于实例方法 `foo()` 来说，调用 `c.foo(1)` 相当于调用 `c.foo.__func__(c, 1)`。对于类方法 `bar()` 来说，无论是调用 `c.bar(1)` 还是 `C.bar(1)` 都相当于调用 `C.bar.__func__(C, 1)`。

#### 函数内省

将函数作为对象处理，可以用于运行时内省，类似于 Java 中的反射，可以在运行时获取函数的信息，比如注解、闭包、参数默认值等。下面列出了一些函数对象特有的属性和方法：

```python
>>> def func(): ...
... 
>>> sorted(set(dir(func)) - set(dir(object)))
['__annotations__', '__call__', '__closure__', '__code__', '__defaults__', '__dict__', '__get__', '__globals__', '__kwdefaults__', '__module__', '__name__', '__qualname__']
```

`dir()` 函数可以查看一个模块或一个类中的所有属性，当然方法也算方法属性。上述代码将 func 函数对象与常规对象 object 的属性集合做了一个差集，只打印函数对象特有的属性。下表对这些特有属性做了简要说明。

| 名称                | 类型             | 说明                      |
| ----------------- | -------------- | ----------------------- |
| `__annotations__` | dict           | 参数和返回值的注解               |
| `__call__`        | method-wrapper | 实现 () 运算符，即可调用对象协议      |
| `__closure__`     | tuple          | 函数闭包，即自由变量的绑定（没有则是None） |
| `__code__`        | code           | 编译成字节码的函数元数据和函数定义体      |
| `__defaults__`    | tuple          | 形式参数的默认值                |
| `__get__`         | method-wrapper | 实现只读描述符协议               |
| `__globals__`     | dict           | 函数所在模块中的全局变量            |
| `__kwdefaults__`  | dict           | 仅限关键字形式参数的默认值           |
| `__name__`        | str            | 函数名称                    |
| `__qualname__`    | str            | 函数的限定名称，如 Random.choice |

函数内省经常被一些框架使用发挥出强大效果。比如 `__defaults__`、`__code__` 和 `__annotations__` 属性，经常被 IDE 用来提取关于函数签名的信息，我们之前也提到过 IDE 和 lint 工具使用函数注解做静态类型检查。还比如一些 Python Web 后端框架，可以自动解析 HTTP 请求中的参数将其注入到接口函数中执行，而不用程序员手动处理。
