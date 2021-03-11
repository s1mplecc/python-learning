# PyCharm 高效阅读源码

除了标注存根文件，PyCharm 还对子类父类方法重载进行了标注，分别用 `O↑` 表示这一行重载了父类方法，点击可以跳转到父类实现；`O↓` 表示这一行有子类重载，点击可以跳转到子类实现。其中 O 代表的是 Override 的含义。

比如我们阅读 Python 内置的列表 list 的源码，append 方法这一行既是重载自父类也有子类重载（存根文件中标注的）：

```python
class list(MutableSequence[_T], Generic[_T]):
    def append(self, __object: _T) -> None: ...
```

可以看到 list 多重继承自 MutableSequence 和 Generic，如果点击 append 左侧 `O↑`，就会跳转到父类 MutableSequence 的 append 实现处。如果点击 `O↓`，可以选择某个子类并进行跳转（list 存在多个子类）。这在阅读一个具有继承结构的源码时会有所帮助。

当然，如果想在 PyCharm 中高效阅读源码，需要结合快捷键来使用。这里列出一些 Mac OS 下的快捷键，Windows 下一般是将 Cmd 替换为 Ctrl，你也可以打开 PyCharm 设置自行查阅 Keymap 快捷键：

| 快捷键 | 作用 | PyCharm Keymap |
| :--- | :--- | :--- |
| Cmd + U | 跳转到父类实现 | Go to Super Method |
| Cmd + Alt + B/Left Click | 跳转到子类实现 | Go to Implementations |
| Cmd + B/Left Click | 跳转到定义处或调用处 | Go to Declaration or Usages |
| Cmd + \[ | 跳转到鼠标停留的上一个位置 | Back |
| Cmd + \] | 跳转到鼠标停留的下一个位置 | Forward |
| Cmd + E | 跳转到最近浏览的文件 | Iterate Recent Files |
| Cmd + Shift + O | 以文件名查询并跳转 | Go to File |
| Cmd + O | 以类名查询并跳转 | Go to Class |
| Cmd + Alt + O | 以符号查询并跳转，可以查询函数和全局变量 | Go to Symbol |
| 双击 Shift | 整合了所有查询 |  |
| Cmd + F | 搜索当前文件下内容 | Find |
| Cmd + Shift + F | 搜索项目文件中的内容 | Find in Files |

这些都是 PyCharm 中非常实用的快捷键，不管是阅读源码还是自己编码，熟悉这些快捷键有助于快速定位到某个文件，某个函数或是某个变量，从而提高我们的效率。

