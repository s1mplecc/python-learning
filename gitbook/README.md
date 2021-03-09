在写该系列时我正在阅读《流畅的 Python》这本书，这本书作为 Python 进阶的必读书物确实名副其实，它不仅囊括了 Python 的诸多特性，包括一些 Python 独特的高级特性，更重要的是，它为我们展示了一种 Python 的设计理念，一种与我之前接触的 Java OOP 不尽相同的设计思想。在面向对象语言中，非常强调对象的类型，一切行为都是通过对象之间的相互协作完成的。Python 虽然也是一门面向对象语言，但它却将这种类型的限定模糊了，最为典型的就是 Python 中的“**鸭子类型**”：只要表现的像一个序列，就可以对它进行迭代操作。究其根本原因，是因为 Python 内置了许多特殊方法或称为魔法方法（magic methods），这种设计显然与 Java 纯面向对象截然不同。

总的来说，Python 是一门注重实用，专为程序员高效编码而生的语言，它有自己的设计风格，Python 程序员为这种风格取名为 “**Pythonic**”。我相信随着对这本书的深入阅读和更多 Python 的编码实践，我能够对这种风格以及 Python 的设计理念有一些更深的感悟。

当然，“光看不练假把式”，最开始的时候，我只是在命令行中去验证一些 Python 特性，随后我意识到这远远不够，为什么不将学习中的零碎知识点加以整理做成一个系列呢？于是，该系列诞生了。由于知识点的离散性，所以对 Lecture 的划分就显得有些随心所欲，我尽量在目录中将知识点的名称罗列出来。

代码已经托管到 Github 上，链接：https://github.com/s1mplecc/python-learning-lectures

本系列教程的工作环境：

- 系统版本：Mac OS 10.14
- 命令行工具：Terminal + Zsh
- 开发工具：PyCharm Professional 2020.3
- Python 版本：3.8.6

## 目录

* [Lecture 1](lecture-1/README.md)
    * [环境准备](lecture-1/huan-jing-zhun-bei/README.md)
        * [Python 版本](lecture-1/huan-jing-zhun-bei/python-ban-ben.md)
        * [依赖管理](lecture-1/huan-jing-zhun-bei/yi-lai-guan-li.md)
        * [环境隔离](lecture-1/huan-jing-zhun-bei/huan-jing-ge-li.md)
    * [Python 编码规范](lecture-1/python-bian-ma-gui-fan/README.md)
        * [Python 之禅](lecture-1/python-bian-ma-gui-fan/python-zhi-chan.md)
        * [Python 风格指导](lecture-1/python-bian-ma-gui-fan/python-feng-ge-zhi-dao.md)
    * [如何阅读 Python 源码](lecture-1/ru-he-yue-du-python-yuan-ma/README.md)
        * [函数注解](lecture-1/ru-he-yue-du-python-yuan-ma/han-shu-zhu-jie.md)
        * [类型提示](lecture-1/ru-he-yue-du-python-yuan-ma/lei-xing-ti-shi.md)
        * [.pyi 存根文件](lecture-1/ru-he-yue-du-python-yuan-ma/.pyi-cun-gen-wen-jian.md)
        * [PyCharm 高效阅读源码](lecture-1/ru-he-yue-du-python-yuan-ma/pycharm-gao-xiao-yue-du-yuan-ma.md)
    * [单元测试](lecture-1/dan-yuan-ce-shi/README.md)
        * [使用 pytest 编写测试用例](lecture-1/dan-yuan-ce-shi/shi-yong-pytest-bian-xie-ce-shi-yong-li.md)
* [Lecture 2](lecture-2/README.md)
    * [鸭子类型](lecture-2/ya-zi-lei-xing.md)
    * [特殊方法](lecture-2/te-shu-fang-fa.md)
    * [重载运算符](lecture-2/zhong-zai-yun-suan-fu.md)
    * [生成式表达式](lecture-2/sheng-cheng-shi-biao-da-shi.md)
    * [\* 和 \*\* 运算符](lecture-2/he-yun-suan-fu.md)
* [Lecture 3](lecture-3/README.md)
    * [函数是一等公民](lecture-3/han-shu-shi-yi-deng-gong-min.md)
    * [闭包](lecture-3/bi-bao.md)
    * [装饰器](lecture-3/zhuang-shi-qi/README.md)
        * [类装饰器](lecture-3/zhuang-shi-qi/lei-zhuang-shi-qi.md)
        * [延伸：面向切面编程](lecture-3/zhuang-shi-qi/yan-shen-mian-xiang-qie-mian-bian-cheng.md)
