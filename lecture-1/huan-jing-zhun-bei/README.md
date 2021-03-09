# 环境准备

### Python 版本

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

> **pip** - The Python Package Installer. You can use pip to install packages from the Python Package Index \(PyPI\) and other indexes.

[pip](https://pip.pypa.io/en/stable/) 是 Python 的包安装和管理工具，类似于 npm 之于 JavaScript。Python 3.x 以上的发行版本中都是自带 pip 的。在使用之前先确定 pip 的版本，Python3 中的 pip 是 pip3 的别名，但如果安装了 Python2 的 pip，那么在为 Python3 项目安装依赖时请使用 pip3 命令，因为这两个命令会将依赖安装在不同的目录下。

```bash
➜ pip --version
pip 20.3.3 from /usr/local/lib/python3.8/site-packages/pip (python 3.8)
```

常见的 pip 命令使用可以查阅官方文档，或者 `pip -h` 查阅帮助文档。与 JavaScript 的 package.json 一样，Python 也提供了统一管理依赖的配置文件 **requirements.txt**。文件中可以指定依赖的版本号，如果缺省则默认安装最新依赖。

```text
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

### 环境隔离

在 JavaScript 中，使用 npm 安装依赖会在当前目录下生成一个 node\_modules 文件夹，依赖会被安装在这个文件夹中。除非指定 `-g` 或 `--global` 参数，将会在全局环境中安装依赖，在 Mac OS 或 Linux 系统中一般会被安装到 `/usr/local/lib/node_modules` 目录下。这样做的好处是将全局环境与局部环境隔离，避免依赖冲突，尤其是两个项目依赖同一个库的不同版本时。

Python 中也有类似的问题，《Effective Python -- 编写高质量Python代码的59个有效方法》一书中的协作开发章节就提到：**使用虚拟环境隔离项目**。问题在于，通过 pip 命令安装的依赖是全局性的，这意味着这些安装好的模块可能会影响系统内的所有 Python 程序。全局依赖会被安装在特定 Python 版本的目录下，如 `/usr/local/lib/python3.8/site-packages`，对于使用 Python 3.8 的所有项目来说依赖是共享的。

为此，Python 提供了一种解决方案，类似于 JavaScript 的局部环境，隔离出一个单独的 Python 局部环境，这种方案的典型就是 venv。

**venv**

> **venv** \(for Python 3\) and **virtualenv** \(for Python 2\) allow you to manage separate package installations for different projects. If you are using Python 3.3 or newer, the venv module is the preferred way to create and manage virtual environments. venv is included in the Python standard library and requires no additional installation.

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

有了虚拟环境，我们就可以使用 `pip freeze` 命令和 requirements.txt 文件很方便的重现一套环境。此外，在使用 venv 时，应当尽量避免移动环境目录，包括重命名项目名称，因为所有的路径（包括 python3 命令所指向的路径），都以硬编码的形式写在了安装目录中，更改目录路径将导致环境失效。解决办法是修改 `bin/active` 脚本中的 VIRTUAL\_ENV 路径值，并重新激活。

```bash
# active
VIRTUAL_ENV="/Users/s1mple/Downloads/myproject/venv"
```

**Anaconda**

如果你觉得 pip + venv 的方式太过底层，也可以使用 Anaconda。Anaconda 是一个更高层次的包管理器和环境管理器，它依托于 conda 之上开发的，conda 可以理解为整合了 pip 和 venv 的功能，区别在于 conda 是跨平台和不限语言的（支持 R 语言）。PyCharm 也对 conda 提供了支持，可以直接通过 conda 创建虚拟环境。

Anaconda 的下载文件较大（500MB），不仅自带 Python 还附带了许多常用数据科学包，已经成为了数据科学方向百宝箱式的存在。Anaconda 也提供可视化界面。总的来说，对于不太熟悉底层操作的数据分析师来说，Anaconda 易于上手体验友好。但对于软件开发来说，Anaconda 显得过于臃肿，这也是我不选择使用它的原因。现如今的 Python 环境支持官方库已经做的很好，如果不是做数据科学方向的，建议使用原生的 pip + venv。

