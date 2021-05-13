class A:
    def speak(self):
        print('class A:', self)


class B(A):
    def speak(self):
        print('class B:', self)


class C(A):
    def speak(self):
        print('class C:', self)


class D(B, C):
    pass


if __name__ == '__main__':
    D().speak()
    print(D.__mro__)
