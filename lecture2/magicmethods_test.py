class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


class TestMagicMethods:
    def test_should_new_singleton_instance_with_new_method(self):
        s1 = Singleton()
        s2 = Singleton()

        assert s1 is s2
