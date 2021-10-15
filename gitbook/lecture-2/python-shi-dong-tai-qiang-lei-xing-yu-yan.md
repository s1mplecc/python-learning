# Python 是动态强类型语言

> **Dynamic programming language**: In computer science, a dynamic programming language is a class of high-level programming languages, which at runtime execute many common programming behaviours that **static programming languages perform during compilation**. These behaviors could include an extension of the program, by **adding new code, by extending objects and definitions, or by modifying the type system**.

以上内容摘自维基百科对于动态编程语言（Dynamic programming language）的定义。动态语言是相对于静态语言而言的。相比之下，静态语言有更严格的语法限制，在编译阶段就能够确定数据类型，典型的静态语言包括 C、C++ 和 Java 等。这一类语言的优势在于代码结构规范，易于调试和重构。缺点则是语法冗杂，编码方式不灵活。

而动态语言最典型的特点在于不需要编码时指定数据类型，类型信息由运行时推断得出。常见的动态语言都是一些脚本语言，比如 JavaScript、Python、PHP 等。这类语言虽然调试和重构的支持不如静态语言，但由于没有类型约束编码更加灵活。

Python 就是一门动态编程语言，编码时不用指定类型，且运行时可以变更数据类型：

```python
>>> a = 1
>>> type(a)
<class 'int'>
>>> a = '1'
>>> type(a)
<class 'str'>
```

尽管 “PEP 484 -- Type Hints” 引入了类型提示，但它明确指出：Python 依旧是一门动态类型语言，作者从未打算强制要求使用类型提示，甚至不会把它变成约定。但是 API 作者能够添加可选的类型注解，执行某种静态类型检查。

另外值得注意的是，虽然 Python 支持运行时变更数据类型，但变量所指向的内存地址空间已经在变更时发生了变化。也就是说，数据类型变更后不再指向原先的内存地址空间。我们可以用查看对象内存地址的 `id()` 函数加以验证：

```python
>>> a = '123456'
>>> id(a)
4316699376
>>> a = 123456
>>> id(a)
4316579216
```

### 强弱类型

确定了 Python 是动态语言后，接下来我们讨论**强弱类型**语言。首先，强弱类型与是否是动态语言没有必然联系，动态语言并不一定就是弱类型语言，Python 就是一门动态强类型语言。这里的“强弱”可以理解为用以**描述编程语言对于混入不同类型的值进行运算时的处理方式**。

比如在弱类型语言 JavaScript 中，我们可以直接对字符串和数值类型进行相加，虽然得出的结果并不一定是我们想要的：

```javascript
> '1' + 2
'12'
```

出现这种现象的原因是 JavaScript 支持**变量类型的隐式转换**。上面的例子就是将数值类型隐式转换为了字符串类型再进行相加。也因此，JavaScript 中才会存在三个等号的判等运算符 `===`。与 `==` 不同，`===` 在判等时不会进行隐式转换，所以才会有下面这样的结果：

```javascript
> 1 == '1'
true
> 1 === '1'
false
```

而 Python 作为强类型语言，不支持类型的隐式转换，所以整型和字符型相加会直接报错：

```python
>>> 1 + '2'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

所以，强弱类型语言的区别体现在：强类型语言在遇到函数声明类型和实际调用类型不符合的情况时会直接出错或者编译失败；而弱类型的语言可能会进行隐式转换，从而产生难以意料的结果。
