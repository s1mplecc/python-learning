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

* [Lecture 1](#lecture-1)
    * [环境准备](#%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87)
        * [Python 版本](#python-%E7%89%88%E6%9C%AC)
        * [依赖管理](#%E4%BE%9D%E8%B5%96%E7%AE%A1%E7%90%86)
        * [环境隔离](#%E7%8E%AF%E5%A2%83%E9%9A%94%E7%A6%BB)
    * [Python 编码规范](#python-%E7%BC%96%E7%A0%81%E8%A7%84%E8%8C%83)
        * [Python 之禅](#python-%E4%B9%8B%E7%A6%85)
        * [Python 风格指导](#python-%E9%A3%8E%E6%A0%BC%E6%8C%87%E5%AF%BC)
    * [如何阅读 Python 源码](#%E5%A6%82%E4%BD%95%E9%98%85%E8%AF%BB-python-%E6%BA%90%E7%A0%81)
        * [函数注解](#%E5%87%BD%E6%95%B0%E6%B3%A8%E8%A7%A3)
        * [类型提示](#%E7%B1%BB%E5%9E%8B%E6%8F%90%E7%A4%BA)
        * [\.pyi 存根文件](#pyi-%E5%AD%98%E6%A0%B9%E6%96%87%E4%BB%B6)
        * [PyCharm 高效阅读源码](#pycharm-%E9%AB%98%E6%95%88%E9%98%85%E8%AF%BB%E6%BA%90%E7%A0%81)
    * [单元测试](#%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95)
        * [使用 pytest 编写测试用例](#%E4%BD%BF%E7%94%A8-pytest-%E7%BC%96%E5%86%99%E6%B5%8B%E8%AF%95%E7%94%A8%E4%BE%8B)
* [Lecture 2](#lecture-2)
    * [Python 是动态强类型语言](#python-%E6%98%AF%E5%8A%A8%E6%80%81%E5%BC%BA%E7%B1%BB%E5%9E%8B%E8%AF%AD%E8%A8%80)
        * [强弱类型](#%E5%BC%BA%E5%BC%B1%E7%B1%BB%E5%9E%8B)
    * [鸭子类型](#%E9%B8%AD%E5%AD%90%E7%B1%BB%E5%9E%8B)
        * [序列协议](#%E5%BA%8F%E5%88%97%E5%8D%8F%E8%AE%AE)
    * [特殊方法](#%E7%89%B9%E6%AE%8A%E6%96%B9%E6%B3%95)
        * [\_\_new\_\_ &amp; \_\_init\_\_](#__new__--__init__)
        * [\_\_str\_\_ &amp; \_\_repr\_\_](#__str__--__repr__)
        * [\_\_call\_\_](#__call__)
        * [\_\_add\_\_ 与重载运算符](#__add__-%E4%B8%8E%E9%87%8D%E8%BD%BD%E8%BF%90%E7%AE%97%E7%AC%A6)
* [Lecture 3](#lecture-3)
    * [函数是一等公民](#%E5%87%BD%E6%95%B0%E6%98%AF%E4%B8%80%E7%AD%89%E5%85%AC%E6%B0%91)
    * [闭包](#%E9%97%AD%E5%8C%85)
    * [装饰器](#%E8%A3%85%E9%A5%B0%E5%99%A8)
        * [类装饰器](#%E7%B1%BB%E8%A3%85%E9%A5%B0%E5%99%A8)
        * [延伸：面向切面编程](#%E5%BB%B6%E4%BC%B8%E9%9D%A2%E5%90%91%E5%88%87%E9%9D%A2%E7%BC%96%E7%A8%8B)
* [Lecture 4](#lecture-4)
    * [生成式表达式](#%E7%94%9F%E6%88%90%E5%BC%8F%E8%A1%A8%E8%BE%BE%E5%BC%8F)
    * [\* 和 \*\* 运算符](#-%E5%92%8C--%E8%BF%90%E7%AE%97%E7%AC%A6)
