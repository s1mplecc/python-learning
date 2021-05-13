from collections import UserDict


class DoubleDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value * 2)


class DoppelDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value * 2)


class TestSubclassingBuiltinsType:
    def test_should_subclass_builtins_type_cannot_override_setitem(self):
        d = DoubleDict(a=1)
        d['b'] = 2
        d.update(c=3)
        assert d['a'] == 1
        assert d['b'] == 4
        assert d['c'] == 3

    def test_should_subclass_collections_type_can_override_setitem(self):
        d = DoppelDict(a=1)
        d['b'] = 2
        d.update(c=3)
        assert d['a'] == 2
        assert d['b'] == 4
        assert d['c'] == 6
