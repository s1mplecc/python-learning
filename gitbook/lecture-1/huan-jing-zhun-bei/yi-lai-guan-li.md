# 依赖管理

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

