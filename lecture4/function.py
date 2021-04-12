import json


def default_argument(name, age=18):
    print(f'name: {name}, age: {age}')


def record(name, age=18, *phones, email=None, **other):
    print('name: ', name)
    print('age: ', age)
    print('phones: ', phones)
    print('email: ', email)
    print('other: ', other)


# terrible code, using "default=None" is better
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


'''
>>> def keyword_only(a, *, b, c=3): 
...     return a, b, c
... 
>>> keyword_only(1, b=2)
(1, 2, 3)
>>> keyword_only(1, b=2, c=4)
(1, 2, 4)
'''


def keyword_only(a, *, b, c=3):
    return a, b, c


'''
>>> C.foo
<function C.foo at 0x10d613f70>
>>> type(C.foo)
<class 'function'>
>>> c = C()
>>> c
<__main__.C object at 0x10b0a5820>
>>> c.foo
<bound method C.foo of <__main__.C object at 0x10b0a5820>>
>>> type(c.foo)
<class 'method'>
>>> C.bar
<bound method C.bar of <class '__main__.C'>>
>>> c.bar
<bound method C.bar of <class '__main__.C'>>
>>> c.foo(1)
1
>>> c.foo.__func__(c, 1)
1
>>> C.bar(1)
1
>>> C.bar.__func__(C, 1)
1
'''


class C:
    def foo(self, x):
        print(x)

    @classmethod
    def bar(cls, x):
        print(x)


if __name__ == '__main__':
    default_argument('Jack')
    default_argument('Jack', 20)
    default_argument('Jack', age=20)
    record('Jack', 20, 123456, 654321, email='abc@email.com', height=180, weight=90)
    record('Jack', 20, 123456, 654321, weight=90)
