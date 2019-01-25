import unittest
from marshmallow import ValidationError

from resteasycli.schema.auth import AuthSchema, AuthFileSchema


valid_file_datas = [{'version': 'v1.0', 'auth': {}}]
invalid_file_datas = [
    {'version': 'v1.0', 'auth': []},
    {'version': 'v1.0', 'auth': 'abc'},
    {'version': 'v1.0', 'auth': 123},
    {'version': 'v1.0', 'auth': None},
    {'version': 'v1.0'}
]

valid_datas = [
    {
        'type': 'token',
        'credentials': {'token_type': 'abc', 'token_hash': 'xyz'},
    },
    {
        'type': 'basic',
        'credentials': {'username': 'abc', 'password': 'xyz'}
    }
]

invalid_datas = [
    None,
    'abc',
    {},
    [valid_datas[0]],
    {'type': 'token'},
    {'credentials': {'username': 'abc', 'password': 'xyz'}},
    {
        'type': 'some_weird_type',
        'credentials': {'username': 'abc', 'password': 'xyz'}
    },
    {
        'type': 'basic',
        'credentials': {'weirdkey1': 'weirdvalue1', 'weirdkey2': 'weirdvalue2'}
    },
    {
        'type': 'basic',
        'credentials': {}
    },
    {
        'type': 'basic',
        'credentials': {'token_type': 'abc', 'token_hash': 'xyz'}
    },
    {
        'type': 'token',
        'credentials': {'username': 'abc', 'password': 'xyz'}
    }
]


class AuthFileSchemaTest(unittest.TestCase):

    schema = AuthFileSchema()

    def test_validation(self):
        for x in valid_file_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_file_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))

class AuthSchemaTest(unittest.TestCase):

    schema = AuthSchema()

    def test_validation(self):
        for x in valid_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))


if __name__ == "__main__":
    unittest.main()
