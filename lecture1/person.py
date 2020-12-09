"""
测试继承抽象基类 & 注册虚拟子类
"""

from abc import *

# export methods & classes
__all__ = (
    'external_method',
    # '_internal_method',
    'Person', 'PI', 'RegisterP'
)


def external_method():
    print('external_method')


def _internal_method():
    print('_internal_method')


class Person(object):
    def __init__(self, name, age=None):
        self._name = name
        self._age = age if age else 0

    def print(self):
        print(f'Hi, I am {self._name}. {self._age} years old.')

    def can_work(self):
        return self._age >= 18

    @staticmethod
    def variable_parameters_method(s, *args, **kwargs):
        print(f's : {s}, a: {args}, args : {kwargs}')

    @staticmethod
    def _private_method():
        print('_private_method')

    @classmethod
    def from_string(cls, name, age):
        return Person(name, age)

    def abstract_method(self):
        """

        :return:
        """


class PI(ABC):
    @abstractmethod
    def abc(self):
        """

        :return:
        """


# @PI.register
class RegisterP:
    def print(self):
        print('RegisterP::print')

    def abc(self):
        print('RegisterP::abc')
