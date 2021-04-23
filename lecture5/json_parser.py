import json
from collections.abc import Mapping, MutableSequence


def json_loader(filename):
    with open(filename, 'r') as f:
        return json.load(f)


class JsonParser:
    def __new__(cls, arg):
        if isinstance(arg, Mapping):
            return super().__new__(cls)
        elif isinstance(arg, MutableSequence):
            return [cls(i) for i in arg]
        else:
            return arg

    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        return JsonParser(self._data[name])

    def __repr__(self):
        return str(self._data)


class TestJsonParser:
    def test_should_parse_json_and_use_dot_access_attribute(self):
        json_ = JsonParser(json_loader('cities.json'))
        assert json_.code == '200'
        assert json_.cities[0].citycode == 207
        assert json_.cities[0].ext.province == '河北省'

    def test_should_parse_array_json(self):
        json_ = JsonParser([{"code": "200"}, {"code": "404"}])
        assert json_[0].code == '200'
        assert json_[1].code == '404'
