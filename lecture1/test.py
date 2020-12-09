from person import *
import asyncio

if __name__ == '__main__':
    # Python不支持方法重载，但支持参数默认值
    a = Person('Xiao ming', 11)
    b = Person('Xiao bo')
    a.print()
    print(a.can_work())
    b.print()

    b.variable_parameters_method('wwww', 1, 2, 3, fish=1)

    # 测试方法命名下划线规范
    a._private_method()  # IDE会提示但不报错
    external_method()
    # _internal_method()  # 报错
    a.abstract_method()

    # 测试注册虚拟子类
    PI.register(RegisterP)
    rp = RegisterP()
    print(issubclass(RegisterP, PI))
    rp.abc()

    # 使用dir打印非特殊方法
    print(dir(asyncio))
    print([m for m in dir(asyncio.BaseProtocol) if '__' not in m])
