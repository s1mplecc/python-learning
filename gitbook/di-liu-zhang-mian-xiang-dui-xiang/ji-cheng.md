# 继承

面向对象编程语言的一个重要功能就是“继承”，它可以使得在现有类的基础上，无需编写重复代码就可以实现功能的扩展。继承体现了从一般到特殊的过程。

通过继承创建的新类称为“子类”或“派生类”，被继承的类称为“基类”、“父类”或“超类”。在某些面向对象语言中，一个子类可以继承自多个父类，这称为多重继承。Python 是一门支持多重继承的语言。

Python 的继承句法是，在类声明的括号中添加父类名，如 `class C(Base):` 声明了类 C 继承自基类 Base。当声明多重继承时，使用逗号隔开，如 `class C(BaseA，BaseB):`。

子类会继承父类的非私有属性和方法，包括类属性。这里的私有属性是指以双下划线开头且不以双下划线结尾命名的属性，由于 Python 的名称改写机制，这类私有属性将会被改写为“类名 + 属性名”的格式，所以不能被子类通过原有名称访问。

如下，B 类派生自 A 类，继承了 A 类的所有非私有属性和方法：

```python
>>> class A:
...     attr1 = 1
...     def __init__(self):
...         self.attr2 = 2 
...         self._attr3 = 3
...         self.__attr4 = 4
...     def method(self): 
...         print('class A method')
... 
>>> class B(A):
...     pass
... 
>>> b = B()
>>> b.attr1
1
>>> b.attr2
2
>>> b._attr3
3
>>> b.__attr4
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'B' object has no attribute '__attr4'
>>> b.method()
class A method
```

子类可以覆盖父类的属性和方法，或者使用 `super()` 调用父类方法，在原有方法基础上添加新功能。`super()` 的一个重要用途是用于初始化方法 `__init__` 中。如下所示：

```python
>>> class B(A):
...     attr1 = 'b1'
...     def __init__(self):
...         super().__init__()
...         self.attr5 = 5
...     def method(self):
...         super().method()
...         print('class B method')
... 
>>> b = B()
>>> b.attr1
'b1'
>>> b.__dict__
{'attr2': 2, '_attr3': 3, '_A__attr4': 4, 'attr5': 5}
>>> b.method()
class A method
class B method
```

#### 多重继承

Python 支持多重继承。人们对于多重继承褒贬不一，C++ 中对于多重继承的滥用一直饱受诟病，借鉴自 C++ 的 Java 选择直接移除了多重继承特性，采用接口（Interface）作为代替，并取得了巨大的成功。事实证明，接口是一种更加优雅的多重继承解决方案。

多重继承首先要解决的问题就是潜在的**命名冲突**，如果一个类继承自两个不相关的类，这两个类拥有实现不同的同名方法，那么该调用哪一个？这种冲突被称为“菱形问题”。为了解决这个问题，Python 会按照特定的顺序遍历继承图。这个顺序称为**方法解析顺序**（Method Resolution Order，缩写 MRO）。**类有一个名为 `__mro__` 的类属性，它的值是一个元组，按照方法解析顺序存放各个超类的名称**。

**`__mro__` 方法解析顺序**

我们定义一个继承结构，类 D 继承自类 B 和 C，而类 B 和 C 又都继承自类 A。

```python
class A:
    def speak(self):
        print('class A:', self)


class B(A):
    def speak(self):
        print('class B:', self)


class C(A):
    def speak(self):
        print('class C:', self)


class D(B, C):
    pass
```

从继承结构上来看，这是一个菱形结构，会存在调用同名方法的二义性。那么，调用 D 实例的 `speak()` 方法会去调用哪个父类呢？

答案是会调用 B 的 `speak()` 方法。D 类的 `__mro__` 属性如下，访问 D 的方法，会按照 `D -> B -> C -> A` 的顺序进行解析。

```python
>>> d = D()
>>> d.speak()
class B: <multiple_inheritance.D object at 0x1086a6580>
>>> D.__mro__
(<class 'multiple_inheritance.D'>, <class 'multiple_inheritance.B'>, <class 'multiple_inheritance.C'>, <class 'multiple_inheritance.A'>, <class 'object'>)
```

**注**：方法解析顺序不会列出虚拟子类的被注册超类。因此虚拟子类也不会从被注册超类中继承任何方法。

**`super()` 调用链**

在使用 `super()` 调用父类方法时，也遵循方法解析顺序。如果父类中的方法也包含 `super()` 语句，则按照方法解析顺序调用下一个父类的方法（下一个父类可能不是当前父类的直接父类）。比如如下添加了 `super()` 语句的 `speak()` 方法打印如下：

```python
class A:
    def speak(self):
        print('class A:', self)
class B(A):
    def speak(self):
        super().speak()
        print('class B:', self)
class C(A):
    def speak(self):
        super().speak()
        print('class C:', self)
class D(B, C):
    def speak(self):
        super().speak()
        
>>> D().speak()
class A: <__main__.D object at 0x10edc8b80>
class C: <__main__.D object at 0x10edc8b80>
class B: <__main__.D object at 0x10edc8b80>
```

按照 `D -> B -> C -> A` 的方法解析顺序，D 中的 `super()` 方法跳转到 B，B 中的 `super()` 方法跳转到 C（而不是 B 的直接父类 A），C 中的 `super()` 方法再跳转到 A。由于 `super()` 语句在 print 语句之前，最终呈现出的打印顺序是方法解析顺序的出栈顺序。

**方法解析顺序的单调性**

方法解析顺序不仅考虑继承图，还考虑子类声明中所列的超类顺序。如果 D 类声明为 `class D(B, C):`，那么 D 类一定会先于 B、C 类被搜索，且 B 类一定先于 C 类被搜索。我们将这种 `D -> B -> C` 的顺序称为**方法解析顺序的单调性**。 用户在定义继承关系时必须要遵循单调性原则。

Python 方法解析顺序采用的 C3 算法会检查方法解析顺序的单调性。简单地说，C3 算法的基本逻辑是，每定义好一个继承关系顺序，算法会将所有顺序按照满足单调性的方式整合起来，如果整合过程出现冲突，算法会抛出错误。

如下所示，由于定义 B 类时声明为 `class B(A):`，所以 B 的解析顺序要先于 A，然而在使用 `class C(A, B):` 声明 C 类时，A 的解析顺序又先于 B，因此发生冲突，抛出异常。

```python
>>> class A: ...
... 
>>> class B(A): ...
... 
>>> class C(A, B): ...
... 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Cannot create a consistent method resolution
order (MRO) for bases A, B
```

在 Python 标准库中，最常使用多重继承的是 `collections.abc` 模块，其中的类都定义为抽象基类。抽象基类类似于 Java 中的接口声明，只不过它可以提供具体方法。因此在 `collections.abc` 模块中频繁使用多重继承并没有问题，它为 Python 的集合类型构建了一个继承体系。然而，滥用多重继承容易得到令人费解和脆弱的设计。《Effective Python》中也提到：只在使用混入时才使用多重继承。为此，有必要先介绍一下混入类。

#### 混入类

除了传统的面向对象继承方式，还流行一种通过可重用组件创建类的方式，那就是**混入**（mixin），这在 Scala 和 JavaScript 使用颇多。如果一个类的作用是为多个不相关的子类提供方法实现，从而实现重用，但不体现 “is-a” 语义，应该把这个类明确定义为混入类。从概念上讲，混入不定义新类型，只是打包方法，便于重用。因此，**混入类绝对不能实例化，而且具体类不能只继承混入类**。

Python 没有提供定义混入类的专有关键字，而是推荐在名称末尾加上 “Mixin” 后缀。而在 Scala 中，使用 trait（特性）关键字来声明混入类，TypeScript 中则使用 implements 关键字来继承混入类。

抽象基类可以实现具体方法，因此也可以作为混入使用。`collections.abc` 模块中的抽象基类在一定程度上可以被视为混入类，它们都声明了 `__slots__ = ()` 语句，表明了混入类不能具有实例属性，即混入类不能被实例化。但是，抽象基类可以定义某个抽象类型，而混入做不到，因此，抽象基类可以作为其他类的唯一基类，而混入绝不能作为唯一超类。但是，抽象基类有个局限是混入类没有的，即：抽象基类中提供具体实现的抽象方法只能与抽象基类及其超类中的方法协作。

一些三方库和框架中也有用到混入，比如 Django 框架，我截取了 [Django 视图模块](https://github.com/django/django/blob/main/django/views/generic/base.py)的一小部分源码，以便更好的理解混入类与多重继承的关系。

**Django 源码**

在 Django 中，视图是可调用对象，它的参数是表示 HTTP 请求的对象，返回值是一个表示 HTTP 响应的对象。我们要关注的是这些响应对象。响应可以是简单的重定向，没有主体内容，为我们导向另一个 url，也可以是复杂的网页内容，需要使用 HTML 模版渲染，最终呈现在浏览器终端上。为此，Django 框架提供了重定向视图 RedirectView，以及模版视图 TemplateView。

我们将注意力放在 TemplateView 类上，它继承自三个类，从左到右分别是模版响应混入类 TemplateResponseMixin、上下文混入类 ContextMixin，以及视图基类 View。

```python
class TemplateView(TemplateResponseMixin, ContextMixin, View):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get(self, request, *args, **kwargs): 
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
```

从类型上来说，TemplateView 依然是一个视图类型。View 是所有视图的基类，提供核心功能，如 dispatch 方法。RedirectView 由于不需要渲染，所以只继承了 View 类。

```python
class View:
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs): ...
    def as_view(cls, **initkwargs): ...
    def setup(self, request, *args, **kwargs): ...
    def dispatch(self, request, *args, **kwargs): ...
    def http_method_not_allowed(self, request, *args, **kwargs): ...
    def options(self, request, *args, **kwargs): ...
```

两个混入类 TemplateResponseMixin 和 ContextMixin 并不代表某一特定类型，而是打包了若干属性和方法，此类方法又不是 RedirectView 所需要的，因此不能定义在 View 基类中。TemplateResponseMixin 提供的功能只针对需要使用模版的视图，除了 TemplateView 还提供给其他视图，例如用于渲染列表的 ListView 视图以及默认视图 DetailView 等。

```python
class TemplateResponseMixin:
    """A mixin that can be used to render a template."""
    template_name = None
    template_engine = None
    response_class = TemplateResponse
    content_type = None

    def render_to_response(self, context, **response_kwargs): ...
    def get_template_names(self): ...
    

class ContextMixin:
    """
    A default context mixin that passes the keyword arguments received by
    get_context_data() as the template context.
    """
    extra_context = None

    def get_context_data(self, **kwargs): ...
```

Django 基于类的视图 API 是多重继承的一个优雅示例，尤其是 Django 的混入类易于理解：各个混入类的目的明确，且都以 “Mixin” 作为后缀。

#### 继承的最佳实践

**明确使用继承的目的**：在决定使用继承之前，首先明确这么做的目的。如果是为了继承重用代码，那么组合和委托也可以达到相同效果。《设计模式：可复用面向对象软件的基础》一书中明确指出：“**优先使用对象组合，而不是类继承**”。组合体现的是 “has-a” 语义，与继承相比，组合的耦合性更低，可扩展性更高。继承并不是银弹，继承意味着父类与子类的强耦合性，一旦父类接口发生变化，所有子类都会受到影响。如果继承用错了场合，那么后期的维护可能是灾难性的。但如果目的是继承接口，创建子类型，实现 “is-a” 关系，那么使用继承是合适的。**接口继承是框架的支柱**，如果类的作用是定义接口，就应该明确定义为抽象基类，就像 `collections.abc` 模块所做的那样。

**不要继承多个具体类**：最多只有一个具体父类，也可以没有。也就是说，除了这一个具体父类之外，其余都是抽象基类或混入。并且，如果抽象基类或混入的组合被经常使用，那么就可以考虑定义一个聚合类，使用易于理解的方式将他们结合起来，就如同 `collections.abc` 模块中定义的 Collection 类：`class Collection(Sized, Iterable, Container):`。

**只在使用混入时才使用多重继承**：这比上一条要更加严苛，尽管抽象基类有时可被视为混入类。不管怎么说，如果不是开发框架，尽量避免使用多重继承，如果不得不用多重继承，请使用混入类。混入类不会破坏现有的继承结构树，它就像小型的可插拔的扩展接口坞，目的不是声明 “is-a” 关系，而是为子类扩展特定功能。所以有时也将混入类称为混入组件。

**在声明多重继承自混入类和基类时，先声明混入类，最后声明基类**：这是由于，在定义混入类时使用 `super()` 是普遍的。为了保证继承自混入类和基类的子类，在调用方法时会执行基类的同名方法，需要先声明混入类再声明基类。这样，按照方法解析顺序的单调性，混入类中的 `super()` 方法会调用到基类中的方法。

如下定义了一个属性只能赋值一次的字典，为其属性赋值时，按照方法解析顺序，会先调用混入类的 `__setitem__` 方法，执行到 `super()` 语句，调用基类 UserDict 的 `__setitem__` 方法进行设值。

```python
from collections import UserDict

class SetOnceMappingMixin:
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)
        
class SetOnceDefaultDict(SetOnceMappingMixin, UserDict): ...
```

**使用 `collections` 模块子类化内置类型**：内置类型的原生方法使用 C 语言实现，不会调用子类中覆盖的方法。比如，如下 DoubleDict 中定义的 `__setitem__` 方法并不会覆盖初始化方法 `__init__` 中的设值方法。因此，需要定制 list、dict 或 str 类型时，应该使用 `collections` 模块中的 UserList、UserDict 或 UserString 等。这些类是对内置类型的包装，会把操作委托给内置类型 —— 这是标准库中优先选择组合而不是继承的又一例证。如果所需的行为与内置类型区别很大，那么子类化 `collections.abc` 中的抽象基类自己实现或许更加容易。

```python
>>> class DoubleDict(dict):
...     def __setitem__(self, key, value):
...         super().__setitem__(key, value * 2)
... 
>>> d = DoubleDict(a=1)
>>> d
{'a': 1}
>>> from collections import UserDict
>>> class DoppelDict(UserDict):
...     def __setitem__(self, key, value):
...         super().__setitem__(key, value * 2)
... 
>>> d = DoppelDict(a=1)
>>> d
{'a': 2}
```
