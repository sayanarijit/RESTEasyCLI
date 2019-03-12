import unittest

from resteasycli.schema.workspace import WorkspaceFileSchema
from marshmallow import ValidationError

valid_file_datas = [{'version': 'v1.0'}]
invalid_file_datas = [
    None,
    '',
    {'sites': []},
    [{'version': 'v1.0'}],
    {'version': 1.0},
    {'version': '1.0'},
    {'version': 'v1.0.0'},
    {'version': 'v1'},
    {'version': None},
    {'version': ''},
    {'version': ['v1.0']},
]


class WorkspaceFileSchemaTest(unittest.TestCase):

    schema = WorkspaceFileSchema()

    def test_validation(self):
        for x in valid_file_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_file_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))


if __name__ == '__main__':
    unittest.main()
