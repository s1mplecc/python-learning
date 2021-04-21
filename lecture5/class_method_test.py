class Demo:
    def instance_method(*args):
        return args

    @classmethod
    def class_method(*args):
        return args

    @staticmethod
    def static_method(*args):
        return args


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def fromtuple(cls, arg):
        name, age, *rest = arg
        return cls(name, age)


class TestClassMethod:
    def test_should_instance_method_first_argument_is_class_instance(self):
        c = Demo()
        instance, arg = c.instance_method(1)
        assert arg == 1
        assert instance is c

    def test_should_class_method_first_argument_is_class(self):
        instance, arg = Demo.class_method(1)
        assert instance is Demo
        assert arg == 1

    def test_should_static_method_first_argument_is_args(self):
        arg1, arg2 = Demo.static_method(1, 2)
        assert arg1 == 1
        assert arg2 == 2
