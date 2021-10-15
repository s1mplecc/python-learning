# 全书总览

## 前言

在写该系列时我正在阅读《流畅的 Python》这本书，这本书作为 Python 进阶的必读书物确实名副其实，它不仅囊括了 Python 的诸多特性，包括一些 Python 独特的高级特性，更重要的是，它为我们展示了一种 Python 的设计理念，一种与我之前接触的 Java OOP 不尽相同的设计思想。在面向对象语言中，非常强调对象的类型，一切行为都是通过对象之间的相互协作完成的。Python 虽然也是一门面向对象语言，但它却将这种类型的限定模糊了，最为典型的就是 Python 中的“**鸭子类型**”：只要表现的像一个序列，就可以对它进行迭代操作。究其根本原因，是因为 Python 内置了许多特殊方法或称为魔法方法（magic methods），这种设计显然与 Java 纯面向对象截然不同。

总的来说，Python 是一门注重实用，专为程序员高效编码而生的语言，它有自己的设计风格，Python 程序员为这种风格取名为 “**Pythonic**”。我相信随着对这本书的深入阅读和更多 Python 的编码实践，我能够对这种风格以及 Python 的设计理念有一些更深的感悟。

当然，“光看不练假把式”，最开始的时候，我只是在命令行中去验证一些 Python 特性，随后我意识到这远远不够，为什么不将学习中的零碎知识点加以整理做成一个系列呢？于是，该系列诞生了。由于知识点的离散性，所以对 Lecture 的划分就显得有些随心所欲，我尽量在目录中将知识点的名称罗列出来。

代码已经托管到 Github 上，链接：[https://github.com/s1mplecc/python-learning-lectures](https://github.com/s1mplecc/python-learning-lectures)

本系列教程的工作环境：

* 系统版本：Mac OS 10.14
* 命令行工具：Terminal + Zsh
* 开发工具：PyCharm Professional 2020.3
* Python 版本：3.8.6

## 目录

* [第一章](lecture-1/)
  * [环境准备](lecture-1/huan-jing-zhun-bei.md)
    * [Python 版本](broken-reference)
    * [依赖管理](broken-reference)
    * [环境隔离](broken-reference)
  * [Python 编码规范](lecture-1/python-bian-ma-gui-fan.md)
    * [Python 之禅](broken-reference)
    * [Python 风格指导](broken-reference)
  * [如何阅读 Python 源码](lecture-1/ru-he-yue-du-python-yuan-ma.md)
    * [函数注解](broken-reference)
    * [类型提示](broken-reference)
    * [.pyi 存根文件](broken-reference)
    * [PyCharm 高效阅读源码](broken-reference)
  * [单元测试](lecture-1/dan-yuan-ce-shi.md)
    * [使用 pytest 编写测试用例](broken-reference)
* [第二章](lecture-2/)
  * [Python 是动态强类型语言](lecture-2/python-shi-dong-tai-qiang-lei-xing-yu-yan.md)
  * [鸭子类型](lecture-2/ya-zi-lei-xing.md)
  * [特殊方法](lecture-2/te-shu-fang-fa.md)
* [第三章](lecture-3/)
  * [函数是一等公民](lecture-3/han-shu-shi-yi-deng-gong-min.md)
  * [闭包](lecture-3/bi-bao.md)
  * [装饰器](lecture-3/zhuang-shi-qi.md)

## Lecture 1

作为系列学习的开始，我一直在思考应当安排哪些内容，考虑到动手实践的重要性，最终我安排了以下这四个章节。**环境准备**，将引导你搭建一个自己的 Python 开发环境；**编码规范**以及**阅读源码**章节，我相信这对于任何语言的学习和实践都具有重要意义，阅读源码教会你拿到一份源码该如何下手，遵循编码规范则让你编写出令人赏心悦目的代码；以及最后的**单元测试**章节，我将其作为验证语言特性的最佳工具，也是作为特性学习的正式开始。

### 环境准备

#### Python 版本

目前 Python 主要活跃的有 Python 2.x 和 Python 3.x 两个大版本，与 C++ 和 Java 这种向后兼容的语言不同，Python 的两个版本互不兼容。舍弃兼容性是一种设计上的取舍，在我看来 Python 这种尤为注重“简约”的语言，敢于大胆摒弃一些有设计缺陷的旧包袱，从而拥抱新特性的作风，未尝不是一种 Pythonic 的体现，很大程度上避免了走向像 C++ 一样越来越臃肿晦涩的道路。

Python 核心团队已于 2019 年正式宣布将在 2020 年停止对 Python2 的更新，在此期间会对 Python2 版本进行一些 bug 修复、安全增强以及移植等工作，以便使开发者顺利的从 Python2 迁移到 Python3。Python 2.7 是 2.x 系列的最后一个版本，官网上最新的 Python 2.7.18 版本发布于 2020 年 4 月 20 日。官方停止 Python2 更新的主要动机是想进行 Python3 的推广，以及同时维护两个版本给他们带来的工作负担。目前大部分 Python 开源项目已经兼容 Python3 了，所以**强烈建议使用 Python3 来开发新的项目**。

一般较新的 Linux 发行版已经预装了 Python2 和 Python3，如果没有，也可以通过各自的包管理器进行安装和更新。Mac OS 环境下可以通过 Homebrew 工具来安装 Python，可以附加 `@ + 版本号` 安装指定版本。在一般情况下（不手动修改软链接），命令行中的 `python` 通常是 python 2.7 或其旧版本的别名，`python3` 才指代 Python3 版本，可以通过 `--version` 参数来查看安装的具体版本。由于两个版本互不兼容，在命令行运行 Python 脚本前需要先确定其所用的 Python 版本。

```bash
➜ brew install python  # brew install python@2.7
➜ python --version 
Python 2.7.10

➜ brew install python3  # brew install python@3.8
➜ python3 --version
Python 3.8.6
```

有时也需要在代码中，也就是**运行时确定 Python 版本**，此时用到的是内置的 sys 模块：

```python
>>> import sys
>>> print(sys.version)
3.8.6 (default, Oct  8 2020, 14:07:53) 
[Clang 11.0.0 (clang-1100.0.33.17)]
>>> print(sys.version_info)
sys.version_info(major=3, minor=8, micro=6, releaselevel='final', serial=0)
```

可以通过在运行时判断 Python 版本从而达到较好的兼容性，这在 Python 的内置模块以及标准库中使用较多。由于 `version_info` 本身是个 tuple 类型，重载了比较运算符，所以可以像下面这样直接进行比较：

```python
# builtins.pyi
if sys.version_info >= (3, 9):
    from types import GenericAlias

# contextlib2.py
if sys.version_info[:2] >= (3, 4):
    _abc_ABC = abc.ABC
else:
    _abc_ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})
```

上面的源码来自于两个不同的文件，阅读源码可以发现一些 Python 版本变更的内容。比如自 Python 3.9 引入的 GenericAlias 类型；Python 3.4 之前继承抽象类时还得使用 ABCMeta 形式。

一般情况下，除非你开发的是供他人使用的第三方库，并不需要你在运行时显式判断版本。一方面是版本对于你是可控的，另一方面是如果滥用版本判断会降低代码的整洁性。如果不得不这么做，可以像内置模块 builtins.pyi 一样在存根文件中统一进行处理。

#### 依赖管理

> **pip** - The Python Package Installer. You can use pip to install packages from the Python Package Index (PyPI) and other indexes.

[pip](https://pip.pypa.io/en/stable/) 是 Python 的包安装和管理工具，类似于 npm 之于 JavaScript。Python 3.x 以上的发行版本中都是自带 pip 的。在使用之前先确定 pip 的版本，Python3 中的 pip 是 pip3 的别名，但如果安装了 Python2 的 pip，那么在为 Python3 项目安装依赖时请使用 pip3 命令，因为这两个命令会将依赖安装在不同的目录下。

```bash
➜ pip --version
pip 20.3.3 from /usr/local/lib/python3.8/site-packages/pip (python 3.8)
```

常见的 pip 命令使用可以查阅官方文档，或者 `pip -h` 查阅帮助文档。与 JavaScript 的 package.json 一样，Python 也提供了统一管理依赖的配置文件 **requirements.txt**。文件中可以指定依赖的版本号，如果缺省则默认安装最新依赖。

```
####### example-requirements.txt #######
beautifulsoup4              # Requirements without Version Specifiers
docopt == 0.6.1             # Version Matching. Must be version 0.6.1
keyring >= 4.1.1            # Minimum version 4.1.1
coverage != 3.5             # Version Exclusion. Anything except version 3.5
Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
```

使用 `-r` 参数指定通过 requirements.txt 文件安装依赖：

```bash
pip install -r requirements.txt
```

有时我们需要进行项目迁移，比如将本地项目部署至服务器，为了保证重新安装依赖时不影响项目的正常运行，可以使用 freeze 指令将所需的依赖和具体版本号写入 requirements.txt 文件中，再一次性安装所有依赖。

```bash
➜ pip freeze > requirements.txt
➜ cat requirements.txt 
certifi==2020.11.8
matplotlib==3.3.2
numpy==1.19.4
six==1.15.0
```

#### 环境隔离

在 JavaScript 中，使用 npm 安装依赖会在当前目录下生成一个 node_modules 文件夹，依赖会被安装在这个文件夹中。除非指定 `-g` 或 `--global` 参数，将会在全局环境中安装依赖，在 Mac OS 或 Linux 系统中一般会被安装到 `/usr/local/lib/node_modules` 目录下。这样做的好处是将全局环境与局部环境隔离，避免依赖冲突，尤其是两个项目依赖同一个库的不同版本时。

Python 中也有类似的问题，《Effective Python -- 编写高质量Python代码的59个有效方法》一书中的协作开发章节就提到：**使用虚拟环境隔离项目**。问题在于，通过 pip 命令安装的依赖是全局性的，这意味着这些安装好的模块可能会影响系统内的所有 Python 程序。全局依赖会被安装在特定 Python 版本的目录下，如 `/usr/local/lib/python3.8/site-packages`，对于使用 Python 3.8 的所有项目来说依赖是共享的。

为此，Python 提供了一种解决方案，类似于 JavaScript 的局部环境，隔离出一个单独的 Python 局部环境，这种方案的典型就是 venv。

**venv**

> **venv** (for Python 3) and **virtualenv** (for Python 2) allow you to manage separate package installations for different projects. If you are using Python 3.3 or newer, the venv module is the preferred way to create and manage virtual environments. venv is included in the Python standard library and requires no additional installation.

从 Python 2.7 开始，Python 社区开发了一些较底层的创建**虚拟环境**（virtual environment）的工具，在 Python 2.7 中这个工具叫做 virtualenv，这是一个三方工具，需要使用 pip 安装。而《Effective Python》一书中提到的工具 pyvenv 是 Python 3.3 所引入的，但由于一些缺陷在 Python 3.6 中已被弃用。取而代之的是 Python 3.5 引入的内置模块 venv，可以通过 `python3 -m venv` 使用这个命令。

[官方文档](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)中已经明确给出建议，如果使用的是 Python 3.3 及以后的版本，更加推荐使用 venv 去管理你的虚拟环境。下面我们扼要的介绍一下 venv 命令的使用方式。

首先创建一个空项目 myproject，在该目录下执行 `python3 -m venv venv` 命令，第二个 venv 是创建的虚拟环境的文件夹名，系统中的环境会被拷贝到该目录下，包括 bin 中的 pip 和 python 命令，而 pip 安装的依赖会存放在 lib 目录中。

```bash
➜ mkdir myproject; cd myproject
➜ python3 -m venv venv
➜ ls -F
venv/
➜ ls -F venv
bin/        include/    lib/        pyvenv.cfg
```

为了启用这套虚拟环境需要先运行**激活**脚本，启用后会发现命令行多了 `(venv)` 前缀，这明确的提示了开发者现在处于虚拟环境中。默认情况下虚拟环境只安装了 pip 和 setuptools 两个初始依赖，此时的环境已经独立于全局环境，全局依赖不会影响到此项目。pip 和 python3 命令都指向虚拟环境 bin 目录下的命令。

```bash
➜ source venv/bin/activate
(venv) ➜ pip list    
Package    Version
---------- -------
pip        20.2.1
setuptools 49.2.1
(venv) ➜ which python3
/Users/s1mple/Downloads/myproject/venv/bin/python3
(venv) ➜ python3 --version
Python 3.8.6
```

退出虚拟环境时使用 `deactivate` 命令。

```bash
(venv) ➜ deactivate
➜ which python3
/usr/local/bin/python3
```

为了代替手动的在命令行创建虚拟环境，PyCharm 集成了 virtualenv 工具，并且官方文档已经标明：Python 3.3 版本之前使用第三方的 virtualenv 工具，Python 3.3 之后使用内置的 venv 模块。在新建项目时可以选择 New Virtualenv Environment 自动创建虚拟环境。

有了虚拟环境，我们就可以使用 `pip freeze` 命令和 requirements.txt 文件很方便的重现一套环境。此外，在使用 venv 时，应当尽量避免移动环境目录，包括重命名项目名称，因为所有的路径（包括 python3 命令所指向的路径），都以硬编码的形式写在了安装目录中，更改目录路径将导致环境失效。解决办法是修改 `bin/active` 脚本中的 VIRTUAL_ENV 路径值，并重新激活。

```bash
# active
VIRTUAL_ENV="/Users/s1mple/Downloads/myproject/venv"
```

**Anaconda**

如果你觉得 pip + venv 的方式太过底层，也可以使用 Anaconda。Anaconda 是一个更高层次的包管理器和环境管理器，它依托于 conda 之上开发的，conda 可以理解为整合了 pip 和 venv 的功能，区别在于 conda 是跨平台和不限语言的（支持 R 语言）。PyCharm 也对 conda 提供了支持，可以直接通过 conda 创建虚拟环境。

Anaconda 的下载文件较大（500MB），不仅自带 Python 还附带了许多常用数据科学包，已经成为了数据科学方向百宝箱式的存在。Anaconda 也提供可视化界面。总的来说，对于不太熟悉底层操作的数据分析师来说，Anaconda 易于上手体验友好。但对于软件开发来说，Anaconda 显得过于臃肿，这也是我不选择使用它的原因。现如今的 Python 环境支持官方库已经做的很好，如果不是做数据科学方向的，建议使用原生的 pip + venv。

### Python 编码规范

> PEP，全称 Python Enhancement Proposals，译为 Python 增强提案。PEP 已经成为 Python 发布新特性的主要机制，它会收集社区对 Python 的改进意见，经过核心开发者的审查和认可最终形成提案向公众公示。[PEP 的官网首页](https://www.python.org/dev/peps/) 也是 PEP 0 的地址，在这里官方列举了所有的 PEP 的索引，你可以按序号、标题和类型进行检索。

#### Python 之禅

Python 开发者喜欢用 “Pythonic” 这个单词来形容符合 Python 编码风格的代码。这种风格既不是严格的规范也不是编译器强加给开发者的规则，而是大家在使用 Python 语言协同工作的过程中逐渐形成的习惯。要记住：**Python 开发者不喜欢复杂的事物，他们崇尚直观、简洁而又易读的代码**。为此，Python 语言的早期贡献者 Tim Peters 提出了 [PEP 20 -- The Zen of Python](https://www.python.org/dev/peps/pep-0020/)，译为 Python 之禅，提出了共计 19 条 Python 编码的指导性原则。这已经作为一个彩蛋加入到 Python 标准库中，你可以在 Python 交互式命令行中敲入 `import this` 查看。

```
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

这 19 条指导思想强调了代码简约可读的重要性，其中的大多数条目不仅仅适用于 Python，也适用于任何一门其他语言。

#### Python 风格指导

除此之外，[PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) 也是每个 Python 程序员应当阅读的，相较于 Python 之禅它提出了更为细致的建议，目的是让 Python 程序员遵循一致的编码风格。PEP 8 中的大部分都能在 Pycharm IDE 中找到智能提示，缩进、空格与空行也可以通过代码格式化快捷键（Reformat Code）来一键规范化，在 Mac OS 中默认快捷键为 `Cmd + Alt + L`，Windows 中为 `Ctrl + Alt + L`。如果你不使用 PyCharm，也可以安装 Pylint，这是一款 Python 源码静态分析工具，可以自动检测代码是否符合 PEP 8 风格指南。

**命名规范**

这里，我想强调一下 Python 中的命名规范。PEP 8 提倡采用不用的命名风格来区分 Python 语言中的不同角色：

* 文件名（模块名）使用小写字母，单词间以下划线连接，如 `base_futures.py`；私有模块使用单个下划线开头，如 `_collections_abc.py`；
* 函数、变量及属性名，使用小写字母，单词间以下划线连接，如 `dict_keys`；
* 受保护的属性和函数（子类可以访问），使用单个下划线开头，如 `_protected_method`；
* 私有的属性和函数（子类也不能访问），使用两个下划线开头，如 `__private_method`；
* 类与异常，以每个单词首字母大写来命名，如 `BaseHandler`、`TypeError`；
* 模块级别的常量，全部用大写字母，单词间以下划线连接，如 `STDIN_FILENO`；
* 类中的实例方法（instance method），首个参数命名为 `self` 表示对象自身；类方法（class method），首个参数命名为 `cls` 表示类自身。

有几点需要说明的是，Python 中**下划线前缀仅仅是个约定**，由于 Python 没有 public、protected、private 等访问权限控制关键字，只能以有没有下划线开头这种约定俗成的规范告诉程序员这个变量或函数的范围，注意这并不是强制约束。即使函数以下划线开头，在导入模块后仍能够通过 dot 运算符直接访问。

```python
>>> import another
>>> another.external_func()
This is a external_func.
>>> another._internal_func()
This is a _internal_func.
```

但需要注意的是，如果通过 \* 通配符导入的模块，单下划线以及双下划线开头的函数和属性并不会被导入到当前模块中，除非导入模块显式定义了包含这些函数和属性的 `__all__` 列表（但通常不会这么做）。此外，也不建议通过通配符导入模块，应当按照最小导入原则，显式的导入需要用到的函数和属性。

```python
>>> from another import *
>>> external_func()
This is a external_func.
>>> _internal_func()
NameError: name '_internal_func' is not defined
```

在命名时，尤其要**避免以双下划线开头且结尾的命名格式**，如 `__foo__`，这是 Python 内置的魔法方法（magic methods，或称特殊方法，如 `__init__`），以及内置属性（如 `__code__`）的命名方式。因为你不能保证在后续版本中 Python 不会将 `__foo__` 作为内置方法或属性。

如果你阅读 Python 标准库源码，会发现基本上私有命名都是以单下划线开头，不论是私有函数还是私有类或是私有变量和常量，很少会看到以双下划线开头的。PEP 8 也提倡对于**非公有方法和属性使用单个下划线开头**，只有在避免子类命名冲突时才采用双下划线开头（且不以双下划线结尾），这是由于双下划线前缀会导致 Python 解释器改写属性名称（name mangling）。比如下面代码中的 `__v3` 就被改写为 `_Foo__v3` 类名 + 变量名的格式：

```python
>>> class Foo:
...     v1 = 1
...     _v2 = 2
...     __v3 = 3
...     __v4_ = 4 
...     __v5__ = 5
... 
>>> [_ for _ in dir(Foo) if 'v' in _]
['_Foo__v3', '_Foo__v4_', '__v5__', '_v2', 'v1']
```

上面代码使用一个**单独的下划线** `_` 作为循环中的变量名称，代表这个变量是临时的，名称无关紧要，你可以将其理解为**占位符**。

PEP 8 还提到，对于与 Python 保留关键字命名冲突的公有属性，可以采用**单个下划线结尾**的命名格式，这要优于使用缩略格式。比如下面的 `class_` 变量：

```python
tkinter.Toplevel(master, class_='ClassName')
```

另外，Python 在维持语义清晰的原则上为了保证简洁性，一些**简短的介词和连词间会省略下划线**，并没有严格的按照单词间下划线连接，而是直接拼接，比如 `isinstance`、`__setattr__` 和 `getstate`。

### 如何阅读 Python 源码

阅读源码是每个程序员都应当具备的技能，阅读源码不仅能帮助你理解一个模块实现的细节，也能让你从优秀的源码中汲取经验，遵循更好的编码规范，编写出更 Pythonic 的代码。但不可否认的是，阅读源码需要一定的编码功底，盲目的阅读并不能取得应有的效果。在阅读源码之前我们要明白阅读的目的，如果是想了解一个模块的实现细节自不必多说，但如果是想提高自己的 Python 编码水平，那么就应该从 Python 标准库以及一些优秀的第三方开源代码下手。

在《Python编程之美：最佳实践指南》这本书中，作者 Kenneth Reitz 从简单的 HowDoI 项目，到大一点的 requests 库（他本身也是这个库的开发者），再到后面的 Web 框架 Flask，逐步递进地展示如何阅读高质量的代码。如果想阅读优秀的第三方库源码，可以从他在书中罗列出的经典项目开始。除此之外，GitHub 上也有人整理了比较详尽的目录：[Python 开源库及示例代码](https://github.com/programthink/opensource/blob/master/libs/python.wiki)。项目很多，但不是每个都必读。还是强调的那一点：不要盲目的阅读源码，确定有必要的时候再去阅读。

抛开这些问题不谈，本篇我想结合我自己在阅读标准库源码（主要是 typing 模块和 re 模块）时的一点理解，介绍一些阅读源码前需要掌握的先验知识，以及如何结合开发工具在 PyCharm IDE 中高效地阅读源码。让我们先从 Python 代码的类型提示开始。

#### 函数注解

> **PEP 3107 -- Function Annotations** : Python Version 3.0, Created Time 2-Dec-2006. This PEP introduces a syntax for adding arbitrary metadata annotations to Python functions.

Python 3 添加了对类型提示（Type Hints）的支持，在此之前 Python 2.x 一直缺乏一种统一的方式去对函数参数和返回值进行标注，一些工具或三方库通过 docstring、注释或者函数装饰器等其他方法尝试去弥补这种缺陷。而自从 Python 3.0 开始，Python 通过 PEP 3107 提案引入了**函数注解**，也就是 Function Annotations，提供了一种标准的解决方案，用于**为函数声明中的参数和返回值附加元数据**。

函数注解的语法如下所示：

```python
def foo(a: expression, b: expression = 5) -> expression:
    ...
```

函数声明中的各个参数可以在 `:` 之后添加注解表达式。如果参数有默认值，表达式后可以跟 `=` 指定默认值，且与常规函数声明一样，指定默认值参数要出现在无默认值参数之后。注解表达式最常使用的是类型（如 str 或 int），也可以是一个字符串（如 'int > 0'）。如果想注解返回值，在 `)` 与 `:` 之间添加 `->` 和一个表达式，表达式可以是任意类型，如果函数无返回值则为 None。

本质上来说，PEP 3107 只是一种前导的语法规范，不对注解任何实质处理，你可以将其理解为官方规定的函数声明的注释。换句话说，**注解只是元数据**，Python 解释器对其不做检查、不做强制、不做验证。Python 对注解所做的唯一的事情，就是将它们存储在函数的 `__annotations__` 属性中：

```python
>>> def foo(a: 'x', b: 5 + 6, c: list) -> max(2, 9): ...
>>> foo.__annotations__
{'a': 'x', 'b': 11, 'c': <class 'list'>, 'return': 9}
```

其中 return 键保存的是返回值的注解，即函数声明里以 `->` 标记的部分。从这个例子我们可以看出，注解表达式的约束非常的宽泛，不管你是类型，还是字符串，或是个表达式。

注解可以供 IDE、框架和装饰器等工具使用，举个例子，框架可以对 `price: 'int > 0'` 这样的字符串注解转换为对参数的验证。注解最大的作用是为 IDE 和 lint 程序中的**静态类型检查**功能提供额外的类型信息，也就是我们接下来要讨论的类型提示。

**延伸**：Java 中的注解也称为 Annotation，使用 `@` 符号标注，本质上也是元数据，本身 Java 解释器不会对其做任何处理，只有结合 Java 运行时的反射（getAnnotation 方法）才能获取注解内容从而针对性地制定处理逻辑，这在一些框架例如 Spring 中使用颇多。这与 Python 中的注解是否存在异曲同工之处呢？我们有理由相信，Python 中的静态类型检查工具也是获取了函数的 `__annotations__` 属性从而进行处理。

#### 类型提示

> **PEP 484 -- Type Hints** : Python Version 3.5, Created Time 29-Sep-2014. This PEP aims to provide a standard syntax for type annotations, opening up Python code to easier static analysis and refactoring, potential runtime type checking, and (perhaps, in some contexts) code generation utilizing type information.

在 PEP 3107 提案提出后，已经有一些第三方工具结合函数注解做了静态类型检查方面的工作，其中被采用较多的就是 Jukka Lehtosalo 开发的 mypy 项目。PEP 484 提案受 mypy 的强烈启发（Jukka 也参与了提案的制订），规定了如何给 Python 代码添加**类型提示（Type Hints）**，主要方式就是使用注解，以及引入了一个新模块：**typing 模块**。

**typing 模块**

为了给 Python 静态类型检查提供统一的命名空间，标准库以渐进定型（gradual typing）的方式引入名为 [typing](https://docs.python.org/3/library/typing.html) 的新模块，新模块不会影响现有程序的正常运行，只会对不规范的类型作出提示。

在 typing 模块中，定义了一些**特殊类型**（\_SpecialForm），包括 Any, NoReturn, ClassVar, Union, Optional 等，从名称可以大概猜出这些类型的作用，比如：Any 代表任意类型；联合类型 `Union[X, Y]` 表示类型非 X 即 Y；Optional 作用则与 Java8 中的 Optional 类似，允许传入参数为空，可以避免空值引用的问题。

除此之外，还有一些常见的数据类型，比如 List、Tuple、Dict、Sequence，它们只是作为标准库类型的别名存在，如：`List = _alias(list, T, inst=False)`。typing 模块也提供了对于**泛型**（Generics）的支持，让我们得以像 `List[int]` 这样去定义特定类型集合。想了解更多 typing 模块的功能，建议阅读 PEP 484文档或者直接阅读源码，源码的文档注释介绍了该模块的结构，通过 `__all__` 属性也可以查明 typing 模块都提供了哪些功能。

PEP 484 旨在为类型注解提供一种标准语法，让 Python 代码更易于静态分析和重构，尽管 typing 模块也提供了一些潜在的用于运行时类型检查的功能模块，尤其是 `get_type_hints()` 函数，但它本身不对其做直接支持，仍然需要开发第三方库才能实现特定的运行时类型检查功能，比如使用装饰器或元类。`get_type_hints` 函数用于获取对象的类型提示，它的源码中包含这么一行：

```python
hints = getattr(obj, '__annotations__', None)
```

这验证了我们之前猜想的类型提示会去查询对象的 `__annotations__` 属性，此外该方法还会对注解字符串进行验证，我们将这个方法再应用到之前随意注解的 foo 函数时就会报错：找不到 “x” 类型。

```python
>>> from typing import get_type_hints
>>> def foo(a: 'x', b: 5 + 6, c: list) -> max(2, 9): ...
>>> foo.__annotations__  # No error
{'a': 'x', 'b': 11, 'c': <class 'list'>, 'return': 9}
>>> get_type_hints(foo)  # Error
NameError: name 'x' is not defined
>>>
>>> def bar(a: int) -> str: ...
>>> get_type_hints(bar)
{'a': <class 'int'>, 'return': <class 'str'>}
```

**变量注解**

> **PEP 526 -- Syntax for Variable Annotations** : Python Version 3.6, Created Time 09-Aug-2016. This PEP aims at adding syntax to Python for annotating the types of variables (including class variables and instance variables), instead of expressing them through comments.

为了丰富类型提示的功能，Python 随即在 3.6 版本中引入了**变量注解（Variable Annotations）**，用于规定变量的类型。与函数注解相同，变量注解也只是元数据，Python 解释器不对其做任何处理，仅供框架和工具做类型检查。语法上变量注解与函数注解类似，使用 `:` 后接参数类型。

```python
primes: List[int] = []

def signal(flag: bool):
    color: str  # Note: no initial value!
    if flag: color = 'green'
    else: color = 'red'
    return color

class Starship:
    captain: str = 'Picard'  # instance variable with initial value
    stats: ClassVar[Dict[str, int]] = {}  # class variable
```

变量注解适用于全局变量、局部变量、类属性以及实例属性。上述代码中的 ClassVar 是由 typing 模块定义的特殊类型，向静态类型检查程序标示在类实例中不允许对该变量进行赋值。注解的同时可以对变量进行初始化，如果省略初始化，也能很方面的在后续的条件分支中进行初始化。

全局变量的注解存储在当前模块的 `__annotations__` 字典中，如果在 Python 交互式命令行中就是 `__main__`：

```python
>>> a: int = 1
>>> b: str
>>> __annotations__
{'a': <class 'int'>, 'b': <class 'str'>}
>>> 
>>> import __main__
>>> get_type_hints(__main__)
{'a': <class 'int'>, 'b': <class 'str'>}
```

**何时使用类型提示**

PEP 484 中强调了 Python 将继续维持作为动态语言的特性，从来没有将类型提示强制化或是惯例化的想法。那么何时采用类型提示呢？一般而言，如果你开发的是供他人使用的第三方库（尤其是在 PyPI 上发布的库中），或是在一个多人协作的稍大项目中，推荐使用类型提示。一方面，这会帮助使用库的用户正确地调用接口。另一方面，类型提示也可以帮助理解类型是如何在代码中传播的。

Bernat Gabor 认为类型提示与单元测试重要性一致，本质上都是为了验证你的代码库的输入输出类型，只是表现形式不同。在他的文章 [the state of type hints in Python](https://www.bernat.tech/the-state-of-type-hints-in-python/) 的最后总结中提到：**只要值得编写单元测试，就应该添加类型提示**，哪怕代码只有十行，只要你日后需要维护它。所以他给出的建议是，在编写单元测试的同时添加类型提示。虽然这会添加额外的代码量，但为了代码平稳工作值得付出这个代价，尤其是发生代码变更时。

我们可以在存根文件中使用类型注解来启用类型提示。并且如果参数声明带有默认值，则可以不指定实际的默认值而使用省略号 `...` 代替，这与冒号后的函数体使用省略号一样，将省略号用作占位符。对于变量，一般只声明类型不给出初值。例如：

```python
def foo(x: AnyStr, y: AnyStr = ...) -> AnyStr: ...

stream: IO[str]
```

#### .pyi 存根文件

由于 Python 是动态语言，不对类型做强制约束，所以 IDE 在类型检查、类型推断、代码补全以及重构等方面必然不如 Java 等静态语言来的方便。**存根文件是包含类型提示信息的文件**，运行时不会用到，而是**提供给第三方工具做静态类型检查和类型推断**，这方面 PyCharm 做的很好。

在 PyCharm 中，如果某一行的左边有 _号标识，则说明这一行（可以是类、属性或函数）在存根文件中有定义，你可以点击_ 号跳转到该文件对应的存根文件，通常是存放在 Python 库文件的 Typeshed Stubs 目录中，文件名以 `.pyi` 后缀结尾。同时，存根文件也是 GitHub 上一个单独的项目，项目地址：[https://github.com/python/typeshed](https://github.com/python/typeshed) ，Python 的标准库以及内置 builtins 存根可以在该项目的 stdlib 目录下找到。

我们来看看 Python 正则库 re 的存根文件和源文件：

```python
# re.pyi
@overload
def compile(pattern: AnyStr, flags: _FlagsType = ...) -> Pattern[AnyStr]: ...
@overload
def compile(pattern: Pattern[AnyStr], flags: _FlagsType = ...) -> Pattern[AnyStr]: ...

# re.py
def compile(pattern, flags=0):
    "Compile a regular expression pattern, returning a Pattern object."
    return _compile(pattern, flags)
```

这里只截取了源码中的一段 compile 函数。从形式上看，存根文件与 C 语言中的头文件有相似之处，将函数声明与函数定义分文件存放，但与其将存根文件理解为函数声明文件，不如理解为函数接口（Interface）文件，接口的意义就是让用户在调用时可以清晰地查看函数的参数和返回值类型。这也是为什么 PEP 484 的作者之一 Jukka Lehtosalo 说可以将 `.pyi` 中的 i 理解为 Interface。

上述源文件中的 compile 函数，调用了私有的 \_compile 函数并返回一个 Pattern 对象，作用是将字符串处理（编译）成正则表达式模版。进一步 \_compile 的源码会发现，如果传入的 pattern 参数本来就是 Pattern 类型的，为了避免重复处理，方法会直接返回 pattern，如下面的代码所示。

```python
def _compile(pattern, flags):
    if isinstance(pattern, Pattern):
        if flags:
            raise ValueError(
                "cannot process flags argument with a compiled pattern")
        return pattern
    ...
```

这也解释了为什么存根文件中会存在两个 compile 函数声明，其中的第二个就是接收 Pattern 类型作为参数的。除了 compile 函数之外，re 存根文件中的大多数函数都有两个重载函数，原因就是它们实现时都调用了 \_compile 函数。事实上，为了防止用户多次调用 \_compile 引起不必要的开销，\_compile 也设置了缓存优化，这点留给读者自行阅读源码分析。

在最新的 PyCharm 2020.3 版本中，支持直接创建 Python stub 类型的 Python File，只需要存根文件与源文件同名，PyCharm 就会自动按照存根文件中指定的类型进行静态类型检查。并且，你也可以像 Typeshed 项目为存根文件分配单独的文件夹，具体操作详见 JetBrains 官网的 PyCharm 手册：[Python Stubs](https://www.jetbrains.com/help/pycharm/stubs.html)。

#### PyCharm 高效阅读源码

除了标注存根文件，PyCharm 还对子类父类方法重载进行了标注，分别用 `O↑` 表示这一行重载了父类方法，点击可以跳转到父类实现；`O↓` 表示这一行有子类重载，点击可以跳转到子类实现。其中 O 代表的是 Override 的含义。

比如我们阅读 Python 内置的列表 list 的源码，append 方法这一行既是重载自父类也有子类重载（存根文件中标注的）：

```python
class list(MutableSequence[_T], Generic[_T]):
    def append(self, __object: _T) -> None: ...
```

可以看到 list 多重继承自 MutableSequence 和 Generic，如果点击 append 左侧 `O↑`，就会跳转到父类 MutableSequence 的 append 实现处。如果点击 `O↓`，可以选择某个子类并进行跳转（list 存在多个子类）。这在阅读一个具有继承结构的源码时会有所帮助。

当然，如果想在 PyCharm 中高效阅读源码，需要结合快捷键来使用。这里列出一些 Mac OS 下的快捷键，Windows 下一般是将 Cmd 替换为 Ctrl，你也可以打开 PyCharm 设置自行查阅 Keymap 快捷键：

| 快捷键                      | 作用                   | PyCharm Keymap              |
| ------------------------ | -------------------- | --------------------------- |
| Cmd + U                  | 跳转到父类实现              | Go to Super Method          |
| Cmd + Alt + B/Left Click | 跳转到子类实现              | Go to Implementations       |
| Cmd + B/Left Click       | 跳转到定义处或调用处           | Go to Declaration or Usages |
| Cmd + \[                 | 跳转到鼠标停留的上一个位置        | Back                        |
| Cmd + ]                  | 跳转到鼠标停留的下一个位置        | Forward                     |
| Cmd + E                  | 跳转到最近浏览的文件           | Iterate Recent Files        |
| Cmd + Shift + O          | 以文件名查询并跳转            | Go to File                  |
| Cmd + O                  | 以类名查询并跳转             | Go to Class                 |
| Cmd + Alt + O            | 以符号查询并跳转，可以查询函数和全局变量 | Go to Symbol                |
| 双击 Shift                 | 整合了所有查询              |                             |
| Cmd + F                  | 搜索当前文件下内容            | Find                        |
| Cmd + Shift + F          | 搜索项目文件中的内容           | Find in Files               |

这些都是 PyCharm 中非常实用的快捷键，不管是阅读源码还是自己编码，熟悉这些快捷键有助于快速定位到某个文件，某个函数或是某个变量，从而提高我们的效率。

### 单元测试

我已经不止一次被强调单元测试的重要性，单元测试作为一个黑盒接受输入验证输出，可以有效的测试一个方法的健壮性。此外，我想尽量给这个学习系列带入些测试驱动的思想。所以以单元测试作为特性学习的开始，应当还算合理。一方面，熟练掌握一门语言其实是语言特性掌握的累积，为了验证一个特性而编写一个单元测试看来最适合不过了（当然可能不止需要一个单元测试）。另一方面，如果验证结果的时候还是使用一堆 print 方法，就会显得相当凌乱而且不那么专业，而通过运行测试时打印的一系列方法名，可以清楚这些模块涉及了哪些 Python 特性。

#### 使用 pytest 编写测试用例

选择 pytest 作为单元测试框架，是因为它简单实用。我个人不太欣赏 Python 自带的 unittest 模块的写法，测试类需要继承一个测试基类，并且到处充斥着 `self`。而 pytest 编写的测试用例只需要符合一定的命名规范，就会被框架自动检测到并运行。此外 pytest 还重写了 assert 关键字，打印信息也更加人性化。

**编写 pytest 测试用例需要符合如下规范**：

* 测试文件如果不指定，必须以 `test_` 开头或结尾；
* 测试类必须以以 `Test` 开头，且不能含有 `__init__` 构造函数；
* 测试函数必须以 `test_` 开头；
* 断言使用 Python 原生的 assert 关键字，pytest 框架没有提供特殊的断言方法。

需要注意的是，测试类不是必须的，在类之外的函数只要符合以 `test_` 开头的规范，也会被 pytest 测试框架检测到。同样，测试类中的测试方法也必须以 `test_` 开头。而非测试类（不以 `Test` 开头的类）中的 `test_` 方法也不会被执行。

pytest 不包含在 Python 标准库中，需要另行安装依赖。有两种方式运行 pytest 测试。**第一种**，在命令行中使用 `pytest` 命令，可以后接文件名指定待测文件，如果不指定，将测试当前文件夹下的所有符合命名规则的文件。下面这条命令可以避免生成 pytest_cache 测试缓存文件。

```bash
pytest -p no:cacheprovider
```

**第二种**，在 main 函数中运行 pytest，提供的接口是 `pytest.main()`，该方法接收一个参数数组。这样做的好处是可以在 PyCharm 等 IDE 中直接 run 或者 debug 调试，也可以方便地控制测试的粒度，譬如只跑某个测试方法或者某个测试类（命令行通过参数也可以限定）。除了 pytest，目前 PyCharm 2020 版本集成的测试工具还包括 原生的 unittest、Nosetests 以及 Twisted Trial。

```python
import pytest

class TestClass:
    def test_one(self):
        assert 1 + 1 == 2

if __name__ == "__main__":
    pytest.main(['-p', 'no:cacheprovider'])
```

如果测试均通过了，打印结果如下图所示，以 `.` 代表文件中成功通过的测试方法，右侧的百分比代表的是测试进度，即已跑完的测试占总测试比例。

```
============================= test session starts ==============================
platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /Users/s1mple/Projects/PycharmProjects/python-learning-lecture/lecture2
collected 4 items

test_example.py ...                                                      [ 75%]
vector_test.py .                                                         [100%]

============================== 4 passed in 0.01s ===============================
```

如果某个测试方法未通过（断言报错），pytest 会提示你具体的出错位置，方便定位问题。

```
=================================== FAILURES ===================================
____________________ TestVector.test_should_print_correctly ____________________

self = <vector_test.TestVector object at 0x110e15eb0>

    def test_should_print_correctly(self):
        v1 = Vector()
>       assert str(v1) == 'Vector(0,)'
E       AssertionError: assert 'Vector(0)' == 'Vector(0,)'
E         - Vector(0,)
E         ?         -
E         + Vector(0)
```

**关于测试用例命名**：尽管我的测试用例命名不严格遵循 TDD 中的 “Given-When-Then” 格式，但是通过 “should + 下划线”这种命名规范，也可以清晰的明白某个测试用例测试了什么功能。比如，看到 `test_should_add_two_vectors_with_add_operator()`，你可能能猜到这个测试用例测试的是加法运算符的重载。

## Lecture 2

### Python 是动态强类型语言

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

#### 强弱类型

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

### 鸭子类型

在面向对象的静态类型语言中，如果要实现一个带特定功能的序列类型，你可能会想到使用继承，以期能在添加特定功能的同时尽可能的重用代码。这符合面向对象的设计原则，但在 Python 中，继承却不是首选方案。

在 Python 这类动态类型语言中，有一种风格叫做**鸭子类型**（duck typing）。在这种风格中，一个对象有效的语义，不是由继承自特定的类或实现特定的接口决定的，而是由"**当前方法和属性的集合**"决定。这个概念最早来源于 James Whitcomb Riley 提出的“鸭子测试”，“鸭子测试”可以这样表述：“如果一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么它就可以被称为鸭子。”

在 Python 中创建功能完善的序列类型无需使用继承，只需实现符合序列协议的方法。那么，协议又是什么呢？在面向对象编程中，协议是非正式的接口，只在文档中定义，可以看作是约定俗成的惯例。例如，Python 的迭代器协议就包含 `__iter__` 和 `__next__` 两个方法，任何实现了 `__iter__` 和 `__next__` 方法的类，Python 解释器会将其视为迭代器，所有迭代器支持的操作，该类也会支持，比如使用 `next()` 方法和 `for` 循环。用鸭子类型来解释就是：这个类看起来像是迭代器，那它就是迭代器。

```python
>>> from collections.abc import Iterator
>>> class IterDuck:
...     def __iter__(self): return self
...     def __next__(self): return 1
... 
>>> i = IterDuck()
>>> issubclass(IterDuck, Iterator)
True
>>> isinstance(i, Iterator)
True
>>> next(i)
1
```

由于实现了迭代器协议，上面代码中的 IterDuck 类甚至不需要显式的继承 Iterator 类，Python 解释器就已经将它绑定为 Iterator 类的子类。

**在鸭子类型中，关注点在于对象的行为，即提供的方法，而不在于对象所属的类型。**

#### 序列协议

序列协议之所以要专门作为单独的一节，是因为序列在 Python 中尤为重要，Python 会特殊对待看起来像是序列的对象。序列协议包含 `__len__` 和 `__getitem__` 两个方法。任何类，只要实现了 `__len__` 和 `__getitem__` 方法，就可以被看作是一个序列，即使这一次 Python 解释器不再将其绑定为 Sequence 类的子类。

由于序列的特殊性，如果你知道类的具体应用场景，甚至只需要实现序列协议的一部分。下面的代码演示了一个只实现了 `__getitem__` 方法的类，对于序列操作的支持程度：

```python
>>> class SeqDuck:
...     def __getitem__(self, index):
...         return range(3)[index]
... 
>>> s = SeqDuck()
>>> s[2]  # __getitem__
2
>>> for i in s: print(i)  # __iter__
... 
0
1
2
>>> 2 in s  # __contains__
True
```

尽管只实现了 `__getitem__` 方法，但 SeqDuck 实例却可以使用 `for` 循环迭代以及 `in` 运算符。

即使没有 `__iter__` 方法，SeqDuck 实例依然是可迭代的对象，因为当发现存在 `__getitem__` 方法时，Python 会调用它，传入从 0 开始的整数索引，尝试迭代对象（这是一种后备机制）。同样的，即使没有 `__contains__` 方法，但 Python 足够智能，能够迭代 SeqDuck 实例检查有没有指定元素。

综上，鉴于序列协议的重要性，如果没有 `__iter__` 和 `__contains__` 方法，Python 会尝试调用 `__getitem__` 方法设法让迭代和 `in` 运算符可用。

### 特殊方法

想要更深入地理解鸭子类型，必须要了解 Python 中的特殊方法。前面我们提到的以双下划线开头和结尾的方法，比如 `__iter__`，就称为**特殊方法**（special methods ），或称为**魔法方法**（magic methods）。

Python 标准库和内置库包含了许多特殊方法，需要注意的是，永远不要自己命名一个新的特殊方法，因为你不知道下个 Python 版本会不会将其纳入到标准库中。我们需要做的，是重写现有的特殊方法，并且通常情况下，不需要显式的调用它们，应当使用更高层次的封装方法，如 `str()` 代替 `__str__()`，对特殊方法的调用应交由 Python 解释器进行。

Python 对于一些内置方法及运算符的调用，本质上就是调用底层的特殊方法。比如在使用 `len(x)` 方法时，实际上会去查找并调用 x 对象的 `__len__` 方法；在使用 `for` 循环时，会去查找并调用对象的 `__iter__` 方法，如果没有找到这个方法，那会去查找对象的 `__getitem__` 方法，正如我们之前所说的这是一种后备方案。

可以说，特殊方法是 Python 语言灵活的精髓所在，下面我们结合鸭子类型一章中的 SeqDuck 类与特殊方法，尝试还原 Python 解释器运行的逻辑。

```python
class SeqDuck:
    def __getitem__(self, pos):
        return range(3)[pos]
```

1. Python 解释器读入 SeqDuck 类，对所有双下划线开头结尾的特殊方法进行检索。
2. 检索到 `__getitem__` 方法，方法签名符合序列协议。
3. 当需要对 SeqDuck 实例进行循环迭代时，首先查找 `__iter__` 方法，未找到。
4. 执行 `__getitem__` 方法，传入从 0 开始的整数索引进行迭代直至索引越界终止循环。

该过程可以理解为 Python 解释器对 SeqDuck 类的功能进行了**运行时扩充**。显然这增强了 Python 语言的动态特性，但另一方面也解释了为什么 Python 运行效率较低。

下面我将对一些常用特殊方法进行介绍。

#### `__new__` & `__init__`

在 Java 和 C# 这些语言中，可以使用 `new` 关键字创建一个类的实例。Python 虽然没有 `new` 关键字，但提供了 `__new__` 特殊方法。在实例化一个 Python 类时，最先被调用的就是 `__new__` 方法。大多数情况下不需要我们重写 `__new__` 方法，Python 解释器会执行 object 中的 `__new__` 方法创建类实例。但如果要使用单例模式，那么 `__new__` 方法就会派上用场。

```python
>>> class Singleton:
...     _instance = None
...     def __new__(cls):
...         if cls._instance is None:
...         cls._instance = object.__new__(cls)
...         return cls._instance
... 
>>> s1 = Singleton()
>>> s2 = Singleton()
>>> s1 is s2  ## id(s1) == id(s2)
True
```

`__init__` 方法则类似于构造函数，如果需要对类中的属性赋初值，就可以在 `__init__` 中进行。在一个类的实例被创建的过程中，`__new__` 要先于 `__init__` 被执行，因为要先创建好实例才能进行初始化。`__new__` 方法的第一个参数必须是 `cls` 类自身，`__init__` 方法的第一个参数必须是 `self` 实例自身。

```python
>>> class Employee:
...     def __new__(cls):
...         print('__new__ magic method is called')
...         return super().__new__(cls)
...
...     def __init__(self):
...         print ("__init__ magic method is called")
...         self.name = 'Jack'
... 
>>> e = Employee()
__new__ magic method is called
__init__ magic method is called
>>> e.name
'Jack'
```

由于 Python 不支持方法重载，即同名方法只能存在一个，所以 Python 类只能有一个构造函数。如果需要定义和使用多个构造器，可以使用带默认参数的 `__init__` 方法，但这种方法实际使用还是有局限性。另一种方法则是使用带有 `@classmethod` 装饰器的类方法，可以像使用类的静态方法一样去调用它生成类的实例。

```python
class Person:
    def __init__(self, name, sex='MAlE'):
        self.name = name
        self.sex = sex

    @classmethod
    def male(cls, name):
        return cls(name)

    @classmethod
    def female(cls, name):
        return cls(name, 'FEMALE')

p1 = Person('Jack')
p2 = Person('Jane', 'FEMALE')
p3 = Person.female('Neo')
p4 = Person.male('Tony')
```

#### `__str__` & `__repr__`

> str() is used for creating output for end user while repr() is mainly used for debugging and development. repr’s goal is to be unambiguous and str’s is to be readable.

`__str__` 和 `__repr__` 都可以用来输出一个对象的字符串表示。使用 `str()` 时会调用 `__str__` 方法，使用 `repr()` 时则会调用 `__repr__` 方法。

`str()` 可以看作 string 的缩写，类似于 Java 中的 `toString()` 方法；`repr()` 则是 representation 的缩写。这两者的区别主要在于受众。`str()` 通常是输出给终端用户查看的，可读性更高。而 `repr()` 旨在机器可读的，所以更加 “official”，强调含义准确无异义。此外在 Python 控制台以及 Jupyter notebook 中，对象输出也是调用的 `__repr__` 方法。

```python
>>> x = list(("a", 1, True))
>>> x  # list.__repr__
['a', 1, True]
```

如果类没有定义 `__repr__` 方法，那么会调用 object 类的 `__repr__` 方法输出：

```python
>>> class A: ...
... 
>>> a = A()
>>> a  # object.__repr__
<__main__.A object at 0x104b69b50>
```

`__str__` 和 `__repr__` 也可以提供给 `print` 方法进行输出，如果只存在一个方法则调用该方法。如果两个方法都存在，则会优先调用 `__str__` 方法。

```python
>>> class Foo:
...     def __repr__(self):
...         return 'repr: Foo'
...     def __str__(self):
...         return 'str: Foo'
... 
>>> f = Foo()
>>> f
repr: Foo
>>> print(f)
str: Foo
```

#### `__call__`

在 Python 中，函数是一等公民。这意味着 Python 中的函数可以作为参数和返回值，并且可以在任何你想调用的时候都能调用它，这对于函数式编程具有重要意义。除此之外，Python 还提供了一个特殊方法 `__call__`，允许类的实例表现得与函数一致，可以对它们进行调用，以及作为参数传递。这在一些需要保存并经常更改状态的类中尤为有用。

下面的代码中，我定义了一个从 0 开始的递增器类，它保存了计数器状态，并在每次调用时计数加一：

```python
>>> class Incrementor:
...     def __init__(self):
...         self.counter = 0
...     def __call__(self):
...         self.counter += 1
...         return self.counter
... 
>>> inc = Incrementor()
>>> inc()
1
>>> inc()
2
```

允许将类的实例作为函数调用，如上面代码中的 `inc()`，本质上与 `inc.__call__()` 直接调用对象的方法并无区别，但它可以以一种更直观且优雅的方式来修改对象的状态。

并且 `__call__` 方法可以接收可变参数, 这意味着可以像定义任意函数一样定义类的 `__call__` 方法。当 `__call__` 方法接收一个函数作为参数时，那么这个类就可以作为一个函数装饰器。基于类的函数装饰器就是这么实现的。如下代码我在 func 函数上使用了类级别的函数装饰器 Deco，使得在执行函数前多打印一行信息。

```python
>>> class Deco:
...     def __init__(self, func):
...         self.func = func
...     def __call__(self, *args, **kwargs):
...         print('decorate...')
...         return self.func(*args, **kwargs)
... 
>>> @Deco
... def func(name):
...     print('execute function', name)
... 
>>> func('foo')
decorate...
execute function foo
>>>
```

实际上类级别的函数装饰器必须要实现 `__call__` 方法，因为本质上函数装饰器就是一个接收被装饰函数作为参数的高阶函数。有关装饰器可以详见装饰器一章。

#### `__add__` 与重载运算符

运算符重载这个语言特性一直备受争议，鉴于太多 C++ 程序员滥用这个特性，Java 之父 James Gosling 很干脆的决定不为 Java 提供运算符重载功能。但另一方面，正确的使用运算符重载确实能提高代码的可读性和灵活性。为此，Python 施加了一些限制，在灵活性、可用性和安全性之间做到了平衡。主要包括：

* 不能重载内置类型的运算符
* 不能新建运算符，只能重载现有的
* is、and、or 和 not 运算符不能重载（但位运算符 &、| 和 \~ 可以）

Python 中的运算符重载是通过重写特殊方法实现的。比如重载 “+” 加号运算符需要重写 `__add__`，重载比较运算符 “==” 需要重写 `__eq__` 方法。下面我将演示如何重载运算符来提高代码的可读性。

考虑一个平面向量，由 x，y 两个坐标构成。为了实现向量的加法（按位相加），重写了加号运算符，为了比较两个向量是否相等重写了比较运算符，为了在控制台方便验证结果重写了 `__repr__` 方法。完整的向量类代码如下：

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)
```

在控制台验证结果：

```python
>>> from vector import Vector
>>> v1 = Vector(1, 2)
>>> v2 = Vector(2, 3)
>>> v1 + v2
Vector(3, 5)
>>> v1 == v2
False
>>> v1 + v1 == Vector(2, 4)
True
```

可以看到完全没有必要为 Vector 类添加专门的 `add()` 和 `equals()` 方法，只需要重载现有运算符，并且代码可读性也显著提高了，直接对向量进行 "+" 相加更符合数学逻辑。另外值得一提的是，在 Python 2 中，在重载 `==` 的同时也要重载 `!=` 运算符即重写 `__ne__` 方法。而在 Python 3 中，这不再是必需的，因为默认情况下，`__ne__` 会委托给 `__eq__` 执行并对结果取反。[官方解释](https://docs.python.org/3/reference/datamodel.html)

下面列出一些常见可重载运算符。

**一元运算符**

| 运算符 |     特殊方法     | 备注                        |
| :-: | :----------: | ------------------------- |
|  -  |   `__neg__`  | 一元取负算术运算符                 |
|  +  |   `__pos__`  | 一元取正算术运算符                 |
|  \~ | `__invert__` | 对整数按位取反，定义为 \~x == -(x+1) |

**二元运算符**

|      运算符     |      特殊方法      |       就地方法      | 备注                   |
| :----------: | :------------: | :-------------: | -------------------- |
|       +      |    `__add__`   |    `__iadd__`   | 加法或拼接                |
|       -      |    `__sub__`   |    `__isub__`   | 减法                   |
|      \*      |    `__mul__`   |    `__imul__`   | 乘法或重复复制              |
|       /      |  `__truediv__` |  `__itruediv__` | 除法                   |
|      //      | `__floordiv__` | `__ifloordiv__` | 整除                   |
|       %      |    `__mod__`   |    `__imod__`   | 取模                   |
|   divmod()   |  `__divmod__`  |  `__idivmod__`  | 返回由整除的商和模数组成的元组      |
| \*\* 或 pow() |    `__pow__`   |    `__ipow__`   | 取幂                   |
|       @      |  `__matmul__`  |  `__imatmul__`  | 矩阵乘法(Python 3.5 新引入) |
|       &      |    `__and__`   |    `__iand__`   | 按位与                  |
|      \|      |    `__or__`    |    `__ior__`    | 按位或                  |
|       ^      |    `__xor__`   |    `__ixor__`   | 按位异或                 |
|      <<      |  `__lshift__`  |  `__ilshift__`  | 按位左移                 |
|      >>      |  `__rshift__`  |  `__irshift__`  | 按位右移                 |

注：就地方法是指就地修改左操作数，如 "+=" 运算符。

**比较运算符**

| 运算符 |   特殊方法   | 后备机制          |
| :-: | :------: | ------------- |
|  == | `__eq__` | 判断 id 是否相等    |
|  != | `__ne__` | 对 `__eq__` 取反 |
|  >  | `__gt__` | 抛出 TypeError  |
|  <  | `__lt__` | 抛出 TypeError  |
|  >= | `__ge__` | 抛出 TypeError  |
|  <= | `__le__` | 抛出 TypeError  |

注：后备机制是指特殊方法不存在或方法运行异常时采取的行为。

## Lecture 3

### 函数是一等公民

虽然《流畅的Python》作者一再强调 Python 不是一门函数式编程语言，但它的的确确具备了一些函数式编程的特性。其中的一个重要特性是：Python 将**函数作为一等公民**。这与 JavaScript、Scala 等语言一样，意味着在这类语言中：**函数与其他数据类型处于同等地位，函数可以定义在函数内部，也可以作为函数的参数和返回值**。基于这个特性，我们可以很容易的定义高阶函数。来看一个 JavaScript 的例子：

```javascript
const add = function(x) {
  return function(y) {
    return x + y
  }
}
```

这个函数将一个函数作为了返回值，很明显它是一个高阶函数，那么问题来了：这样定义有什么作用或者是好处呢？事实上，这段代码是 JavaScript 中的一个优雅的函数式编程库 [Ramda](https://ramdajs.com) 对于加法实现的基本思路（还需要可变参数以及参数个数判断）。最终我们可以这样去使用它：

```javascript
const R = require('ramda')
R.add(1, 2) // -> 3
const increment = R.add(1) // 返回一个函数
increment(2) // -> 3
R.add(1)(2) // -> 3
```

既可以像代码第二行一次性传入两个参数，也可以像代码第三、四行分两个阶段传入，这与代码第五行效果一致。我们将这种特性称为**函数柯里化（Currying）**，这样做的好处一是可以**代码重用**，就像特意将 `R.add(1)` 取名为 increment 一样，它可以单独地作为一个递增函数；二是可以实现**惰性求值**，只有当函数收集到了所有所需参数，才进行真正的计算并返回结果，这一点在许多流处理框架中有广泛使用。

Python 中的函数之所以可以作为一等公民，究其原因，是因为 Python 中的**一切皆是对象**，即 _Everything in Python is an object_。使用 `def` 关键字定义的任何函数，都是 `function` 类的一个实例。

```python
>>> def func():
...     pass
... 
>>> type(func)
<class 'function'>
```

既然函数是对象，那就可以持有属性，这也是为什么 Python 中函数可以持有外部定义的变量（也就是闭包问题）的根本原因。这一点与 Java 和 C++ 这类语言是有本质区别的。以 Java8 为例，虽然 Java8 提供了一些语法糖让我们得以编写所谓的“高阶函数”，但 Java 中的函数（方法）依然不能脱离类或者对象而存在：

```java
Arrays.asList(1, 2, 3, 4, 5)
        .stream()
        .filter(i -> i >= 3)
        .forEach(System.out::println);
```

上述代码第三行接收一个 Lambda 表达式作为参数，第四行接收一个方法引用，看上去函数可以作为参数传入。但实际上，Java 编译器会将它们转换为**函数接口（Functional Interfaces）**的具体实现，函数接口是 Java8 函数式编程引入的核心概念。例如上述代码中的 `System.out::println` 方法引用会被实例化为 Consumer 函数接口的具体实现，Consumer 是 Java8 提供的四类函数接口中的一类，称为消费者接口，它有一个 accept 抽象方法接受一个输入且返回值为空，编译器将会用 `System.out.println(t)` 重写这个方法。

```java
@FunctionalInterface
public interface Consumer<T> {
    void accept(T t);
    // ...
}    

// Consumer consumer = System.out::println;
// consumer.accept("hello");
```

所以在 Java8 中，看似函数可以作为参数传入，但实际上传入的依旧是类的实例。如果对 Java8 的函数式编程感兴趣可以参考这篇：[Java8 函数接口](https://s2mple.xyz/2018/11/16/Java8%20%E5%87%BD%E6%95%B0%E6%8E%A5%E5%8F%A3/)。

言归正传，既然已经清楚了 Python 中可以定义高阶函数，那么接下来就可以探讨一下 Python 怎么使用高阶函数实现装饰器的。但在这之前，不得不提及一下什么是闭包。

### 闭包

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

### 装饰器

装饰器，又称函数装饰器，本质上是一个**可调用对象**（实现了 `__call__` 方法），可以是一个函数或者一个类。它接受一个函数作为参数，即被装饰的函数，可能会对这个函数进行处理然后将它返回，或者替换为另一个函数或可调用对象。我们先来看一个简单样例：

```python
>>> def decorate(func):
...     print('running decorator...')
...     return func
... 
>>> @decorate
... def target():
...     print('running target...')
... 
running decorator...
>>> target()
running target...
```

上述代码定义了一个名为 decorate 的装饰器，然后通过 `@decorate` 标注在 target 函数上表明用它来装饰 target 函数。乍一看，这与 Java 中的注解语法是一样的，但其实两者作用是完全不同的。Java 中的注解只是元数据，不会对被修饰的对象做任何修改，必须通过运行时的反射（`getAnnotation` 方法）才能发挥它的作用。而在 Python 中，**装饰器的作用就是定义一个嵌套函数**。你可以理解为，通过装饰器装饰后，target 函数被重新定义为了如下形式：

```python
target = decorate(target)
```

但装饰器与这样直接定义还是有几点区别的。第一点，**装饰器是在被装饰的函数定义之后立即执行的**，这通常是在**导入时**（import），也就是 Python 加载模块时发生的。如果你足够细心，就会发现上述代码中的 `'running decorator...'` 是在 target 函数定义后就被立即打印了，并且调用 target 函数时也没有重复打印。也就是说，**函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行**。这突出了 Python 的导入时和运行时的区别。

第二点，函数装饰器既然要体现它的“装饰”语义，就需要接收一个函数作为参数然后返回一个函数，无论返回的函数是原封不动的原函数还是“装饰”后的函数。也就是说，**装饰器对于函数调用者是透明的**。那么，装饰器返回一个其他类型就没有意义。事实证明，如果返回了其他类型，代码运行将会报出 TypeError 错误（没有找到 `__call__` 方法）。而如果只是嵌套函数 `decorate(target)` 的写法是没有返回类型的限制的。

```python
def decorate(func):
    print('running decorator...')
    return 1

# TypeError: 'int' object is not callable
```

事实上，**大多数装饰器会在内部定义一个函数然后将其返回**，原封不动地返回被装饰的函数是没有多大用处的。接下来，我会为你展示一个稍微“实用”一点的例子 —— 定义一个 clock 计时器，记录被装饰函数的运行时间。在这个例子中，你将会看到闭包问题是如何在装饰器中体现的，以及如何定义并使用一个有参数的装饰器。

```python
def clock(unit=TimeUnit.SECONDS):  # ①
    def decorate(func):
        def clocked(*args, **kwargs):  # ②
            start = time.perf_counter()
            result = func(*args, **kwargs)  # ③
            end = time.perf_counter()
            arg_str = ', '.join(repr(arg) for arg in args)
            if unit == TimeUnit.SECONDS:
                print(f'running {func.__name__}({arg_str}): {end - start}s')
            else:
                print(f'running {func.__name__}({arg_str}): {(end - start) * 1000}ms')
            return result
        return clocked
    return decorate
```

首先，不要被上述代码的两层嵌套函数（共三层函数）吓到，你可能会有一个疑问：装饰器不是通常只有一层嵌套吗（定义一个内部函数然后将其返回），为什么这里会出现两层嵌套？实际上，这是一种**带参装饰器**的妥协，原因是**装饰器只能且必须接收一个函数作为参数**。在这三层函数中，最外层定义的 clock 函数是参数化装饰器**工厂函数**，内层的 decorate 函数才是真正的装饰器，clocked 函数则是包装了被装饰的函数（真正给被装饰函数附加功能）。

上述代码有几个需要注意的点，已经用带圈数字标注出来：

* ① 最外层的 clock 工厂函数接收一个名为 unit 的时间单位的参数，默认值为秒（这里采用枚举类型）；
* ② **如果被装饰的函数带参数，只需要把装饰器最内层函数跟被装饰函数的参数列表保持一致即可**。这里 clocked 函数接收任意个定位参数和仅限关键字参数，写成这样的目的是想体现 clock 计时器的泛用性，你可以在 ③ 处原封不动地将这些参数传给被装饰函数 func 调用；
* ③ func 实际上是定义在 clocked 外层的自由变量（作为 decorate 的参数传入），所以它已经被绑定到 clocked 的闭包中。

③ 处是被装饰函数真正执行的地方，上下两行使用计时器记录并统计了 func 函数运行前后的时间差值，在打印时根据传入 clock 的参数决定打印时间单位采用秒还是毫秒。我们来看看如何使用这个装饰器：

```python
>>> @clock()
... def sleep(secs):
...     time.sleep(secs)
... 
>>> @clock(unit=TimeUnit.SECONDS)
... def sleep_secs(secs):
...     time.sleep(secs)
... 
>>> @clock(unit=TimeUnit.MILL_SECONDS)
... def sleep_ms(ms):
...     time.sleep(ms / 1000)
... 
>>> sleep(0.1)
running sleep(0.1): 0.10221230299998751s
>>> sleep_secs(1)
running sleep_secs(1): 1.000441283999976s
>>> sleep_ms(100)
running sleep_ms(100): 103.84234799994374ms
```

首先应当注意第一个空参装饰器 `@clock()`，其中的 `()` 是不能省略的，它使用了 `TimeUnit.SECONDS` 作为默认参数，这是在 clock 定义处声明的。此外，clock 装饰器中的参数并不是和函数名绑定的，打印的时间单位完全取决于传入 clock 装饰器的参数。比如，也可以让 sleep_ms 按照秒的格式打印时间：

```python
>>> @clock(unit=TimeUnit.SECONDS)
... def sleep_ms(ms):
...     time.sleep(ms / 1000)
... 
>>> sleep_ms(100)
running sleep_ms(100): 0.10072612899966771s
```

#### 类装饰器

#### 延伸：面向切面编程

## Lecture 4

### 生成式表达式

### _和 \*_ 运算符
