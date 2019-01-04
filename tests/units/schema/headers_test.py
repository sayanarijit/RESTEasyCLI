import unittest
from marshmallow import ValidationError

from resteasycli.schema.headers import HeadersSchema, HeadersFileSchema


valid_file_datas = [{'version': 'v1.0', 'headers': {}}]
invalid_file_datas = [
    {'version': 'v1.0', 'headers': []},
    {'version': 'v1.0', 'headers': 'abc'},
    {'version': 'v1.0', 'headers': 123},
    {'version': 'v1.0', 'headers': None},
    {'version': 'v1.0'}
]

valid_datas = [
    {'action': 'update', 'values': {'a': 'x', 'b': 'y', 'c': 'z'}},
    {'action': 'only', 'values': {}}
]

invalid_datas = [
    None,
    'abc',
    {},
    [valid_datas[0]],
    {'action': 'only'},
    {'values': {}},
    {'action': 'update', 'values': []},
    {'action': 'update', 'values': {1: 'x'}},
    {'action': 'update', 'values': {'x': 1}},
    {'action': 'some_weird_action', 'values': {'a': 'x', 'b': 'y', 'c': 'z'}},
]


class HeadersFileSchemaTest(unittest.TestCase):

    schema = HeadersFileSchema()

    def test_validation(self):
        for x in valid_file_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_file_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))

class HeadersSchemaTest(unittest.TestCase):

    schema = HeadersSchema()

    def test_validation(self):
        for x in valid_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))


if __name__ == "__main__":
    unittest.main()
