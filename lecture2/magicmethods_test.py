class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


class Employee:
    def __new__(cls):
        print('__new__ magic method is called')
        return super().__new__(cls)

    def __init__(self):
        print('__init__ magic method is called')
        self.name = 'Jack'


class Person:
    def __init__(self, name, sex='MALE'):
        self.name = name
        self.sex = sex

    @classmethod
    def male(cls, name):
        return cls(name)

    @classmethod
    def female(cls, name):
        return cls(name, 'FEMALE')


class TestMagicMethods:
    def test_should_new_singleton_instance_with_new_method(self):
        s1 = Singleton()
        s2 = Singleton()

        assert s1 is s2

    def test_should_new_method_run_before_init_method(self):
        assert Employee().name == 'Jack'

    def test_multiple_constructors_with_class_method_and_default_arguments(self):
        p1 = Person('Jack')
        p2 = Person('Jane', 'FEMALE')
        p3 = Person.female('Neo')
        p4 = Person.male('Tony')

        assert p1.sex == 'MALE' and p1.name == 'Jack'
        assert p2.sex == 'FEMALE' and p2.name == 'Jane'
        assert p3.sex == 'FEMALE' and p3.name == 'Neo'
        assert p4.sex == 'MALE' and p4.name == 'Tony'
