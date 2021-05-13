from collections import UserDict


class Dict(UserDict):
    def __setitem__(self, key, value):
        print('2rd be called')
        super().__setitem__(key, value * 2)


class SetOnceMappingMixin:
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        print('1st be called.')
        return super().__setitem__(key, value)


class SetOnceDefaultDict(SetOnceMappingMixin, Dict):
    ...


if __name__ == '__main__':
    d = SetOnceDefaultDict()
    d['a'] = 1  # set breakpoint
